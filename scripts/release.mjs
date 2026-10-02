import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..'),runtime=path.join(root,'.runtime');
function run(cmd,args,quiet=false){const p=spawnSync(cmd,args,{cwd:root,encoding:'utf8',stdio:quiet?'pipe':'inherit'});if(p.status!==0)throw Error(`${cmd} failed${quiet?': '+p.stderr:''}`);return p.stdout?.trim();}
function switchRelease(target){const temp=path.join(runtime,`current-${process.pid}`);fs.symlinkSync(target,temp);fs.renameSync(temp,path.join(runtime,'current'));}
const mode=process.argv[2]||'deploy';
if(mode==='rollback'){
 const previous=path.join(runtime,'previous');if(!fs.existsSync(previous))throw Error('No previous release exists');
 const target=fs.realpathSync(previous),current=fs.realpathSync(path.join(runtime,'current'));switchRelease(target);fs.unlinkSync(previous);fs.symlinkSync(current,previous);console.log('Rolled back to '+path.basename(target));process.exit(0);
}
if(!['deploy','publish','sync'].includes(mode))throw Error('Use deploy, publish, sync, or rollback');
if(mode==='sync'){
 if(run('git',['status','--porcelain'],true))throw Error('Local changes exist. Commit them before syncing.');
 run('git',['pull','--ff-only','origin','main']);
}
run(process.execPath,['--check','server.mjs']);run(process.execPath,['--check','dist/app.js']);run(process.execPath,['--check','dist/engine.js']);
run(process.execPath,['tests/engine.test.cjs']);run(process.execPath,['tests/monty-api.test.mjs']);run(process.execPath,['--check','dist/monty.js']);run(process.execPath,['--check','backend/monty-api.mjs']);
run(process.execPath,['tests/theory.test.cjs']);run(process.execPath,['--check','dist/theory-ui.js']);
if(mode==='publish'){
 run(process.execPath,['scripts/build.mjs']);
 const message=process.argv.slice(3).join(' ').trim();if(!message)throw Error('Provide a descriptive iteration message.');
 run('git',['add','--','dist','README.md','Qualia-Lab-Research.pdf','VALIDATION.json','package.json','server.mjs','scripts','tests','research','backend','DEPLOYMENT.md','AGENTS.md','.gitignore','.github']);
 if(run('git',['status','--porcelain'],true))run('git',['commit','-m',message]);
}
if(run('git',['status','--porcelain'],true))throw Error('Deployment requires a clean, committed project.');
if(mode==='publish')run('git',['push','origin','main']);
const commit=run('git',['rev-parse','HEAD'],true),version=JSON.parse(fs.readFileSync(path.join(root,'package.json'),'utf8')).version;
const release=path.join(runtime,'releases',commit);
if(!fs.existsSync(release)){
 const temp=path.join(runtime,'releases',`.staging-${process.pid}`);fs.mkdirSync(path.dirname(temp),{recursive:true});
 fs.cpSync(path.join(root,'dist'),temp,{recursive:true});
 for(const f of ['index.html','app.js','engine.js','style.css','README.md','Qualia-Lab-Research.pdf'])if(!fs.statSync(path.join(temp,f)).size)throw Error('Missing asset '+f);
 fs.writeFileSync(path.join(temp,'release.json'),JSON.stringify({commit,version,createdAt:new Date().toISOString()},null,2));fs.renameSync(temp,release);
}
const current=path.join(runtime,'current'),previous=path.join(runtime,'previous');
if(fs.existsSync(current)){
 const old=fs.realpathSync(current);if(old!==release){if(fs.existsSync(previous))fs.unlinkSync(previous);fs.symlinkSync(old,previous);}
}
switchRelease(release);
console.log(`Activated ${commit}. Existing app server reads the new release automatically.`);
console.log('Verify /healthz and the browser. Server or service configuration changes require a service restart.');
