#!/usr/bin/env node
import { Command } from 'commander';
import chalk from 'chalk';
import ora from 'ora';
import * as checker from 'license-checker';
import { createObjectCsvWriter } from 'csv-writer';
import * as fs from 'fs';
import * as path from 'path';

const program = new Command();

program
  .name('agent-license-auditor')
  .description('Agent that audits all project dependencies for license compliance.')
  .version('1.0.0')
  .option('-d, --dir <path>', 'Directory to scan', '.')
  .option('-o, --out <path>', 'Output file path for the report', 'THIRD_PARTY_LICENSES.md')
  .option('-f, --format <format>', 'Report format (md, json, csv)', 'md')
  .option('-a, --allow <licenses>', 'Comma separated list of allowed licenses', '')
  .option('-b, --block <licenses>', 'Comma separated list of blocked licenses', 'GPL,AGPL')
  .option('--fail-on-blocked', 'Exit with code 1 if a blocked license is found', true)
  .parse(process.argv);

const options = program.opts();

function scanLicenses(targetDir: string): Promise<checker.ModuleInfos> {
    return new Promise((resolve, reject) => {
        checker.init({ start: targetDir }, (err, packages) => {
            if (err) reject(err);
            else resolve(packages);
        });
    });
}

function normalizeLicense(license: string | string[] | undefined): string {
    if (Array.isArray(license)) {
        return license.join(', ');
    }
    return license || 'UNKNOWN';
}

function checkBlocked(licenseStr: string, blockList: string[]): boolean {
    const lUpper = licenseStr.toUpperCase();
    return blockList.some(b => lUpper.includes(b.toUpperCase()));
}

async function run() {
    const spinner = ora('Scanning dependencies...').start();
    const targetDir = path.resolve(options.dir);
    
    try {
        const pkgs = await scanLicenses(targetDir);
        spinner.succeed(`Scanned ${Object.keys(pkgs).length} dependencies.`);
        
        const blockList = options.block ? options.block.split(',').map((s: string) => s.trim()).filter(Boolean) : [];
        const allowList = options.allow ? options.allow.split(',').map((s: string) => s.trim()).filter(Boolean) : [];
        
        let blockedCount = 0;
        let unknownCount = 0;
        
        const reportData: any[] = [];
        
        console.log(chalk.bold.hex('#EC4899')('\n--- 📜 License Audit Report ---\n'));
        
        for (const [pkgName, details] of Object.entries(pkgs)) {
            const license = normalizeLicense(details.licenses);
            let status = 'OK';
            let color = chalk.green;
            
            if (license === 'UNKNOWN' || license.includes('UNKNOWN')) {
                status = 'MISSING_LICENSE';
                color = chalk.yellow;
                unknownCount++;
            } else if (blockList.length > 0 && checkBlocked(license, blockList)) {
                status = 'BLOCKED_LICENSE';
                color = chalk.red;
                blockedCount++;
            } else if (allowList.length > 0 && !checkBlocked(license, allowList)) {
                status = 'NOT_ALLOWED_LICENSE';
                color = chalk.red;
                blockedCount++;
            }
            
            reportData.push({
                package: pkgName,
                license,
                status,
                repository: details.repository || 'N/A',
                publisher: details.publisher || 'N/A'
            });
            
            if (status !== 'OK') {
                console.log(`  - ${chalk.yellow(pkgName)}: ${color(status)} (${license})`);
            }
        }
        
        if (blockedCount === 0 && unknownCount === 0) {
            console.log(chalk.green('  ✅ All dependencies align with license policies (0 blocked or unknown licenses found).\n'));
        } else {
            console.log(`\n  ⚠️  Found ${chalk.yellow(unknownCount)} packages with unknown licenses.`);
            console.log(`  ⛔ Found ${chalk.red(blockedCount)} packages with blocked licenses.\n`);
        }
        
        // Output file generation
        const outPath = path.resolve(options.out);
        const format = options.format.toLowerCase();
        const generateSpinner = ora(`Generating ${format.toUpperCase()} report...`).start();
        
        if (format === 'json') {
            fs.writeFileSync(outPath, JSON.stringify(reportData, null, 2));
        } else if (format === 'csv') {
            const csvWriter = createObjectCsvWriter({
                path: outPath,
                header: [
                    { id: 'package', title: 'Package' },
                    { id: 'license', title: 'License' },
                    { id: 'status', title: 'Status' },
                    { id: 'repository', title: 'Repository' }
                ]
            });
            await csvWriter.writeRecords(reportData);
        } else {
            // Markdown
            let mdContent = '# Third-Party Licenses\n\nThis document describes the licenses of the third-party dependencies used in this project.\n\n';
            mdContent += '| Package | License | Status | Repository |\n|---|---|---|---|\n';
            reportData.forEach(r => {
                mdContent += `| ${r.package} | ${r.license} | ${r.status} | ${r.repository} |\n`;
            });
            fs.writeFileSync(outPath, mdContent);
        }
        
        generateSpinner.succeed(`Report saved to ${outPath}`);
        
        if (blockedCount > 0 && options.failOnBlocked) {
            console.error(chalk.red.bold('\nAudit failed due to blocked licenses! Exiting with code 1 (Pipeline Integration).'));
            process.exit(1);
        }

    } catch (err: any) {
        spinner.fail('Audit failed!');
        console.error(chalk.red(err.message));
        process.exit(1);
    }
}

run();
