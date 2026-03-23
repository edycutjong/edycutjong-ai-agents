#!/usr/bin/env node
import { Command } from 'commander';
import chalk from 'chalk';
import ora from 'ora';
import * as child_process from 'child_process';
import * as util from 'util';
import * as fs from 'fs';
import * as path from 'path';

const exec = util.promisify(child_process.exec);
const program = new Command();

program
  .name('agent-dependency-updater')
  .description('Autonomous agent that scans npm projects for outdated dependencies, updates them one by one, and runs tests.')
  .version('1.0.0')
  .option('-d, --dir <path>', 'Directory to run in', '.')
  .option('-t, --test <command>', 'Test command to run', 'npm test')
  .option('-m, --mode <mode>', 'Target update mode: latest, minor, patch', 'latest')
  .option('-i, --ignore <packages>', 'Comma separated list of packages to ignore', '')
  .option('-b, --batch', 'Run in batch mode for monorepos (disables prompts)')
  .parse(process.argv);

const options = program.opts();

async function run() {
  const targetDir = path.resolve(options.dir);
  const pkgPath = path.join(targetDir, 'package.json');
  const lockPath = path.join(targetDir, 'package-lock.json');
  
  if (!fs.existsSync(pkgPath)) {
    console.error(chalk.red(`Error: package.json not found in ${targetDir}`));
    process.exit(1);
  }

  // Use ncu to get updates
  const ncu = require('npm-check-updates');
  const spinner = ora('Scanning for outdated dependencies...').start();
  
  try {
    const upgrades = await ncu({
      packageFile: pkgPath,
      target: options.mode,
      reject: options.ignore ? options.ignore.split(',') : []
    });
    
    const packagesToUpdate = Object.keys(upgrades);
    if (packagesToUpdate.length === 0) {
      spinner.succeed('All dependencies are up to date!');
      return;
    }
    
    spinner.info(`Found ${packagesToUpdate.length} outdated dependencies:`);
    packagesToUpdate.forEach(p => console.log(`  - ${chalk.yellow(p)} -> ${chalk.green(upgrades[p])}`));
    
    // Backup package tracking
    let successCount = 0;
    let failCount = 0;
    const report: any[] = [];
    
    for (const pkg of packagesToUpdate) {
       console.log(chalk.bold.hex('#EC4899')(`\n🔄 Updating ${pkg} to ${upgrades[pkg]}...`));
       const backupPkg = fs.readFileSync(pkgPath, 'utf-8');
       const backupLock = fs.existsSync(lockPath) ? fs.readFileSync(lockPath, 'utf-8') : null;
       
       const updateSpinner = ora(`Installing ${pkg}@${upgrades[pkg]}...`).start();
       
       try {
           await exec(`npm install ${pkg}@${upgrades[pkg]}`, { cwd: targetDir });
           updateSpinner.succeed(`Installed ${pkg}@${upgrades[pkg]}.`);
           
           const testSpinner = ora(`Running tests: "${options.test}"...`).start();
           try {
               await exec(options.test, { cwd: targetDir });
               testSpinner.succeed(`Tests passed for ${pkg}.`);
               successCount++;
               report.push({ package: pkg, status: 'Success', version: upgrades[pkg] });
           } catch(testErr: any) {
               testSpinner.fail(`Tests failed for ${pkg} after update.`);
               console.log(chalk.dim(testErr.stdout || testErr.message));
               
               const rollbackSpinner = ora(`Rolling back ${pkg}...`).start();
               fs.writeFileSync(pkgPath, backupPkg);
               if (backupLock) fs.writeFileSync(lockPath, backupLock);
               await exec(`npm install`, { cwd: targetDir });
               rollbackSpinner.info(`Rolled back ${pkg} to previous version.`);
               failCount++;
               report.push({ package: pkg, status: 'Failed', version: 'Rolled back' });
           }
       } catch (installErr: any) {
           updateSpinner.fail(`Failed to install ${pkg}.`);
           fs.writeFileSync(pkgPath, backupPkg);
           if (backupLock) fs.writeFileSync(lockPath, backupLock);
           await exec(`npm install`, { cwd: targetDir });
           failCount++;
           report.push({ package: pkg, status: 'Install Error', version: 'Rolled back' });
       }
    }

    console.log(chalk.bold.hex('#EC4899')('\n--- 📊 Dependency Update Report ---\n'));
    console.log(chalk.green(`✅ Successfully updated: ${successCount}`));
    console.log(chalk.red(`❌ Failed updates (rolled back): ${failCount}\n`));
    
    report.forEach(r => {
      const color = r.status === 'Success' ? chalk.green : chalk.red;
      console.log(`  - ${chalk.yellow(r.package)}: ${color(r.status)} (${r.version})`);
    });

  } catch (err: any) {
    spinner.fail('Error checking dependencies');
    console.error(chalk.red(err.message));
  }
}

run();
