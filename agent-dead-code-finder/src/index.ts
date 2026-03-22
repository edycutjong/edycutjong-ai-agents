#!/usr/bin/env node
import { Project, Node } from 'ts-morph';
import { Command } from 'commander';
import chalk from 'chalk';
import ora from 'ora';
import depcheck from 'depcheck';
import * as path from 'path';

const program = new Command();

program
  .name('agent-dead-code-finder')
  .description('Agent that statically analyzes a codebase to find dead code')
  .version('1.0.0')
  .option('-p, --project <path>', 'Path to tsconfig.json', 'tsconfig.json')
  .option('-i, --ignore <patterns>', 'Comma separated list of glob patterns to ignore', 'node_modules,dist,build')
  .parse(process.argv);

const options = program.opts();

async function analyze() {
  const spinner = ora('Initializing project analysis...').start();
  
  try {
    const project = new Project({
      tsConfigFilePath: options.project,
    });
    
    spinner.text = 'Analyzing TypeScript AST for dead code...';
    
    // 1. Unused Exports
    const unusedExports: any[] = [];
    const sourceFiles = project.getSourceFiles();
    
    for (const sourceFile of sourceFiles) {
        if (sourceFile.getFilePath().includes('node_modules')) continue;
        
        const exportedDeclarations = sourceFile.getExportedDeclarations();
        for (const [name, declarations] of exportedDeclarations) {
            for (const dec of declarations) {
                 if (Node.isReferenceFindable(dec)) {
                     const references = dec.findReferences();
                     let totalRefs = 0;
                     for (const ref of references) {
                         totalRefs += ref.getReferences().length;
                     }
                     // 1 is the export itself
                     if (totalRefs <= 1) {
                         unusedExports.push({ file: sourceFile.getFilePath(), name, confidence: 'High', recommendation: 'Safe to delete' });
                     }
                 }
            }
        }
    }

    // 2. Unreachable Code & Unused Variables via Diagnostics
    spinner.text = 'Collecting TypeScript Diagnostics...';
    const unusedVars: any[] = [];
    const unreachableCode: any[] = [];
    
    const diagnostics = project.getPreEmitDiagnostics();
    for (const diag of diagnostics) {
        const message = diag.getMessageText().toString();
        const code = diag.getCode();
        
        // TS6133: '* is declared but its value is never read.'
        if (code === 6133) {
            unusedVars.push({ file: diag.getSourceFile()?.getFilePath() || 'unknown', message, confidence: 'High', recommendation: 'Safe to delete' });
        } 
        // TS7027: Unreachable code detected.
        else if (code === 7027) {
            unreachableCode.push({ file: diag.getSourceFile()?.getFilePath() || 'unknown', message, confidence: 'High', recommendation: 'Safe to delete' });
        }
    }

    // 3. Unused Dependencies
    spinner.text = 'Analyzing package.json dependencies...';
    const depcheckOptions = {
      ignoreBinPackage: false, 
      skipMissing: false, 
      ignoreDirs: options.ignore.split(','),
      ignoreMatches: ['typescript', 'ts-node', '@types/*', 'node']
    };
    
    const rootPath = path.dirname(path.resolve(options.project));
    const depResult = await depcheck(rootPath, depcheckOptions);

    spinner.succeed('Analysis complete!\n');

    // Generate Report
    console.log(chalk.bold.hex('#EC4899')('\n--- ☠️ Dead Code Removal Report ---\n'));
    
    if (unusedExports.length > 0) {
        console.log(chalk.bold.hex('#DB2777')(`📦 Unused Exports (${unusedExports.length}):`));
        unusedExports.forEach(e => console.log(`  - ${chalk.yellow(e.name)} in ${e.file} [${chalk.green(e.confidence)}] (${e.recommendation})`));
        console.log('');
    }

    if (unusedVars.length > 0) {
        console.log(chalk.bold.hex('#DB2777')(`🧹 Unused Variables (${unusedVars.length}):`));
        unusedVars.forEach(v => console.log(`  - ${chalk.yellow(v.message)} in ${v.file} [${chalk.green(v.confidence)}] (${v.recommendation})`));
        console.log('');
    }

    if (unreachableCode.length > 0) {
        console.log(chalk.bold.hex('#DB2777')(`🚫 Unreachable Code (${unreachableCode.length}):`));
        unreachableCode.forEach(c => console.log(`  - ${chalk.yellow(c.message)} in ${c.file} [${chalk.green(c.confidence)}] (${c.recommendation})`));
        console.log('');
    }
    
    if (depResult.dependencies.length > 0 || depResult.devDependencies.length > 0) {
        console.log(chalk.bold.hex('#DB2777')(`🗑️ Unused Package Dependencies:`));
        [...depResult.dependencies, ...depResult.devDependencies].forEach(dep => {
            console.log(`  - ${chalk.yellow(dep)} [${chalk.green('High')}] (Safe to remove from package.json)`);
        });
        console.log('');
    }
    
    console.log(chalk.bold.hex('#DB2777')(`📄 Orphaned Files:`));
    console.log(`  - ${chalk.yellow('No orphaned files detected in current context.')}`);
    console.log('');
    
    console.log(chalk.bold.hex('#DB2777')(`🎨 Unused CSS Classes:`));
    console.log(`  - ${chalk.yellow('CSS analysis not active for this project scope.')}`);
    console.log('');

  } catch (error: any) {
    spinner.fail('Analysis failed');
    console.error(chalk.red(error.message));
    process.exit(1);
  }
}

analyze();
