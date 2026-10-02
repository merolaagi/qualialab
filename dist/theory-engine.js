/* Bloch-state simulator and independently evolved classical oscillator control. */
(function(root){
'use strict';
function validate(input={}){
 const p={steps:32,phase:45,dephasing:0.04,shots:512,seed:42,intervention:'none',at:12,...input};
 if(Object.keys(input).some(k=>!Object.hasOwn(p,k)||!['steps','phase','dephasing','shots','seed','intervention','at'].includes(k)))throw Error('Unknown parameter');
 for(const [k,lo,hi] of [['steps',4,80],['shots',16,4096],['seed',1,1000000],['at',1,80]])if(!Number.isInteger(p[k])||p[k]<lo||p[k]>hi)throw Error('Invalid '+k);
 for(const [k,lo,hi] of [['phase',0,180],['dephasing',0,1]])if(typeof p[k]!=='number'||!Number.isFinite(p[k])||p[k]<lo||p[k]>hi)throw Error('Invalid '+k);
 if(p.at>p.steps)throw Error('Intervention step must be within the experiment');
 if(!['none','flip','erase'].includes(p.intervention))throw Error('Invalid intervention');
 return p;
}
function rng(seed){let a=seed;return()=>{a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}
function wilson(k,n){const z=1.96,p=k/n,d=1+z*z/n,c=(p+z*z/(2*n))/d,h=z*Math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d;return[Math.max(0,c-h),Math.min(1,c+h)];}
function run(input){
 const p=validate(input),random=rng(p.seed),angle=p.phase*Math.PI/180,c=Math.cos(angle),s=Math.sin(angle),rows=[];
 let x=1,y=0,amplitude=1,theta=0;
 for(let step=0;step<=p.steps;step++){
  if(step){const nx=(1-p.dephasing)*(c*x-s*y);y=(1-p.dephasing)*(s*x+c*y);x=nx;amplitude*=1-p.dephasing;theta+=angle;
   if(step===p.at&&p.intervention==='flip'){x=-x;y=-y;theta+=Math.PI;}
   if(step===p.at&&p.intervention==='erase'){x=0;y=0;amplitude=0;}
  }
  const quantum=Math.max(0,Math.min(1,(1+x)/2)),classical=Math.max(0,Math.min(1,(1+amplitude*Math.cos(theta))/2));
  let count=0;for(let i=0;i<p.shots;i++)if(random()<classical)count++;
  rows.push({step,quantum,classical,stochastic:count/p.shots,interval95:wilson(count,p.shots),bloch:{x,y,z:0},coherence:Math.hypot(x,y),purity:(1+x*x+y*y)/2,noMemory:step===0?1:.5});
 }
 return {schema:'qualialab-theory-v1',protocol:p,rows,maxDifference:Math.max(...rows.map(r=>Math.abs(r.quantum-r.classical))),samplingRMSE:Math.sqrt(rows.reduce((v,r)=>v+(r.stochastic-r.classical)**2,0)/rows.length),interpretation:'The oscillator is analytically equivalent for this task. Sampling is from that same probability, not an independent quantum advantage. No brain or consciousness inference.',units:'Abstract steps; no mapping to biological seconds',quantumModel:'One qubit: prepare |+>, Rz phase rotation, phase-damping channel, final H and Z measurement on fresh preparations at each delay. No entanglement, collapse theory, or Monty coupling.'};
}
root.TheoryLab={run,validate,wilson};if(typeof module!=='undefined')module.exports=root.TheoryLab;
})(typeof globalThis!=='undefined'?globalThis:this);
