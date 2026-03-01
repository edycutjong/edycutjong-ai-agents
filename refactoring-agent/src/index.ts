import { RefactoringAgent } from './agent';

async function main() {
    const args = process.argv.slice(2);
    if (args.length !== 3) {
        console.error('Usage: npm start <owner> <repo> <path>');
        process.exit(1);
    }

    const [owner, repo, path] = args;
    const agent = new RefactoringAgent();
    await agent.run(owner, repo, path);
}

main().catch(console.error);
