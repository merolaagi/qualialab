import fs from 'node:fs';
import path from 'node:path';
import {spawn} from 'node:child_process';

export function validateMonty(input){
 if(!input||Array.isArray(input)||typeof input!=='object')throw Error('Expected an experiment object.');
 const p={modality:'touch',object:'sphere',history:'identical',steps:24,force:.5,noise:0,seed:42,ablation:'none',...input};
 if(Object.keys(input).some(k=>!['modality','object','history','steps','force','noise','seed','ablation'].includes(k)))throw Error('Unknown experiment field.');
 for(const [k,choices] of Object.entries({modality:['touch','vision','sound','taste','smell'],object:['sphere','ellipsoid','ripple'],history:['identical','biased','partial'],ablation:['none','features','location']}))if(!choices.includes(p[k]))throw Error('Invalid '+k);
 for(const [k,lo,hi] of [['steps',8,36],['seed',1,1000000]])if(!Number.isInteger(p[k])||p[k]<lo||p[k]>hi)throw Error('Invalid '+k);
 for(const [k,lo,hi] of [['force',.1,1],['noise',0,.2]])if(typeof p[k]!=='number'||!Number.isFinite(p[k])||p[k]<lo||p[k]>hi)throw Error('Invalid '+k);
 return p;
}

export function montyApi(root){
 let active=false,lastStarted=0;
 return async function handle(req,res){
  const headers={'Content-Type':'application/json','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'};
  const reply=(code,data)=>{if(!res.destroyed){res.writeHead(code,headers);res.end(JSON.stringify(data));}};
  if(req.method!=='POST'){reply(405,{error:'Use POST for a Monty experiment.'});return;}
  let body='';
  try{
   for await(const chunk of req){body+=chunk;if(Buffer.byteLength(body)>4096){reply(413,{error:'Request too large.'});return;}}
   const p=validateMonty(JSON.parse(body));
   if(active||Date.now()-lastStarted<1000){reply(429,{error:'The Monty lab is running an experiment. Try again shortly.'});return;}
   const cfgPath=path.join(root,'.runtime/monty.json');
   if(!fs.existsSync(cfgPath)){reply(503,{error:'Monty is not configured on this host.'});return;}
   const cfg=JSON.parse(fs.readFileSync(cfgPath,'utf8'));
   active=true;lastStarted=Date.now();
   let settled=false,out='',err='';
   const child=spawn(cfg.python,['-u',path.join(root,'backend/monty_bridge.py')],{cwd:root,env:{...process.env,MPLCONFIGDIR:path.join(root,'.runtime/mpl'),OMP_NUM_THREADS:'1',OPENBLAS_NUM_THREADS:'1'},stdio:['pipe','pipe','pipe']});
   const timer=setTimeout(()=>{child.kill('SIGKILL');finish(504,{error:'Monty exceeded the 90-second run limit.'});},90000);
   function finish(code,data){if(settled)return;settled=true;clearTimeout(timer);active=false;reply(code,data);}
   child.on('error',()=>finish(503,{error:'The Monty Python runtime could not start.'}));
   child.stdout.on('data',chunk=>{out+=chunk;if(out.length>2e6){child.kill('SIGKILL');finish(502,{error:'Unexpected Monty response size.'});}});
   child.stderr.on('data',chunk=>{err=(err+chunk).slice(-2000);});
   child.on('close',code=>{
    if(settled)return;
    try{const data=JSON.parse(out.trim());if(code!==0||!data.ok){console.error('Monty experiment:',err);finish(502,{error:'Monty could not complete this experiment. Please try a different condition.'});}else finish(200,data.result);}
    catch{console.error('Monty runtime:',err);finish(502,{error:'Monty returned an invalid response.'});}
   });
   child.stdin.on('error',()=>{});child.stdin.end(JSON.stringify(p)+'\n');
  }catch(error){reply(400,{error:error instanceof SyntaxError?'Invalid JSON.':error.message});}
 };
}
