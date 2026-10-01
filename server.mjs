import http from 'node:http';
import {montyApi} from './backend/monty-api.mjs';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const root=path.dirname(fileURLToPath(import.meta.url));
const runtime=path.join(root,'.runtime');
const handleMonty=montyApi(root);
const config=JSON.parse(fs.readFileSync(path.join(runtime,'config.json'),'utf8'));
if(!Number.isInteger(config.port)||config.port<1024||config.port>65535)throw Error('Invalid configured port');
const allowed=new Map([
 ['/','index.html'],['/index.html','index.html'],['/app.js','app.js'],['/engine.js','engine.js'],
 ['/style.css','style.css'],['/monty.js','monty.js'],['/README.md','README.md'],['/Qualia-Lab-Research.pdf','Qualia-Lab-Research.pdf'],
 ['/Qualia-Lab.html','Qualia-Lab.html']
]);
const mime={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.md':'text/markdown; charset=utf-8','.pdf':'application/pdf'};
const server=http.createServer((req,res)=>{
 if(req.url?.split('?')[0]==='/api/monty/run'){void handleMonty(req,res);return;}
 const headers={'X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer','X-Frame-Options':'SAMEORIGIN','Cache-Control':'no-store','Permissions-Policy':'camera=(), microphone=(), geolocation=()'};
 if(!['GET','HEAD'].includes(req.method)){res.writeHead(405,{...headers,Allow:'GET, HEAD'});res.end();return;}
 let pathname;try{pathname=new URL(req.url,'http://localhost').pathname;}catch{res.writeHead(400,headers);res.end();return;}
 try{
  // Resolve once per request so an atomic release switch cannot mix a path's metadata and body.
  const release=fs.realpathSync(path.join(runtime,'current'));
  const manifest=JSON.parse(fs.readFileSync(path.join(release,'release.json'),'utf8'));
  if(pathname==='/healthz'){
   const body=JSON.stringify({status:'ok',app:'qualialab',commit:manifest.commit,version:manifest.version});
   res.writeHead(200,{...headers,'Content-Type':'application/json','Content-Length':Buffer.byteLength(body)});res.end(req.method==='HEAD'?undefined:body);return;
  }
  const filename=allowed.get(pathname);
  if(!filename){res.writeHead(404,{...headers,'Content-Type':'text/plain'});res.end(req.method==='HEAD'?undefined:'Not found');return;}
  const file=path.join(release,filename),stat=fs.statSync(file);
  res.writeHead(200,{...headers,'Content-Type':mime[path.extname(file)]||'application/octet-stream','Content-Length':stat.size});
  if(req.method==='HEAD'){res.end();return;}
  const stream=fs.createReadStream(file);stream.on('error',()=>res.destroy());stream.pipe(res);
 }catch(error){console.error('Serve error:',error.message);if(!res.headersSent)res.writeHead(503,headers);res.end('Release unavailable');}
});
server.on('error',error=>{console.error(`Qualia Lab cannot bind 127.0.0.1:${config.port}: ${error.code}. No other service was stopped.`);process.exit(1);});
server.listen(config.port,'127.0.0.1',()=>console.log(`Qualia Lab listening at http://127.0.0.1:${config.port}`));
for(const signal of ['SIGINT','SIGTERM'])process.on(signal,()=>server.close(()=>process.exit(0)));
