import { Octokit } from '@octokit/rest';
import OpenAI from 'openai';
import * as config from 'dotenv';
config.config();

export class RefactoringAgent {
    private openai: OpenAI;
    private octokit: Octokit;
    private dryRun: boolean;

    constructor() {
        this.openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
        this.octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });
        this.dryRun = process.env.DRY_RUN === 'true';
    }

    private log(message: string) {
        console.log(`[ReAgent] ${new Date().toISOString()} - ${message}`);
    }

    private async sleep(ms: number) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async run(owner: string, repo: string, path: string) {
        this.log(`Starting refactoring agent for ${owner}/${repo} at ${path}`);

        // 1. Fetch file content
        let content: string;
        let sha: string;
        try {
            const { data } = await this.octokit.repos.getContent({ owner, repo, path });
            if (Array.isArray(data) || data.type !== 'file') {
                this.log(`Path ${path} is not a valid file.`);
                return;
            }
            content = Buffer.from((data as any).content, 'base64').toString('utf8');
            sha = data.sha;
        } catch (e: any) {
            this.log(`Failed to fetch file: ${e.message}`);
            return;
        }

        // 2. Identify smells and refactor
        this.log(`Analyzing ${path} for code smells...`);
        let refactoredCode: string;
        let explanation: string;
        try {
            const response = await this.openai.chat.completions.create({
                model: 'gpt-4o',
                messages: [
                    { role: 'system', content: 'You are an expert software engineer. Identify code smells and return a JSON object with two fields: "explanation" (string) describing the issues and "refactoredCode" (string) containing the fully refactored, complete file content without markdown code block formatting.' },
                    { role: 'user', content }
                ],
                response_format: { type: 'json_object' }
            });
            const resultStr = response.choices[0].message.content || '{}';
            const result = JSON.parse(resultStr);
            refactoredCode = result.refactoredCode;
            explanation = result.explanation;

            if (!refactoredCode || refactoredCode === content) {
                this.log(`No refactoring needed for ${path}.`);
                return;
            }
        } catch (e: any) {
            if (e.status === 429) {
                this.log('Rate limit hit, retrying after sleep...');
                await this.sleep(5000);
                return this.run(owner, repo, path);
            }
            this.log(`AI generation failed: ${e.message}`);
            return;
        }

        // 3. Create PR
        if (this.dryRun) {
            this.log(`[DRY RUN] Would have created PR for ${path}.`);
            this.log(`Explanation:\n${explanation}`);
            return;
        }

        try {
            this.log('Creating a pull request with refactored code...');

            // Setup branch
            const defaultBranch = (await this.octokit.repos.get({ owner, repo })).data.default_branch;
            const refData = await this.octokit.git.getRef({ owner, repo, ref: `heads/${defaultBranch}` });

            const branchName = `refactor/${path.replace(/[^a-zA-Z0-9]/g, '-')}-${Date.now()}`;
            await this.octokit.git.createRef({
                owner,
                repo,
                ref: `refs/heads/${branchName}`,
                sha: refData.data.object.sha
            });

            // Commit changes
            await this.octokit.repos.createOrUpdateFileContents({
                owner,
                repo,
                path,
                message: `refactor: optimize ${path}`,
                content: Buffer.from(refactoredCode).toString('base64'),
                sha,
                branch: branchName
            });

            // Create PR
            const pr = await this.octokit.pulls.create({
                owner,
                repo,
                title: `Refactor ${path} to reduce code smells`,
                body: `### AI Refactoring\n\n${explanation}`,
                head: branchName,
                base: defaultBranch
            });

            this.log(`Successfully created PR: ${pr.data.html_url}`);
        } catch (e: any) {
            this.log(`Failed to create PR: ${e.message}`);
        }
    }
}
