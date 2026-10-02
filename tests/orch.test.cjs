const assert=require('node:assert/strict');const O=require('../dist/orch-engine.js');const close=(a,b)=>assert.ok(Math.abs(a-b)/Math.max(Math.abs(b),1e-100)<1e-12);
const a=O.run();close(a.tauSeconds,.01054571817);close(a.targetEnergyJ,4.218287268e-33);close(a.ratio,1e-3/a.tauSeconds);
close(O.run({energyLog:-31}).tauSeconds,a.tauSeconds/10);
close(O.run({mode:'additive',unitLog:-42,countLog:10}).tauSeconds,a.tauSeconds);
for(const mode of ['direct','additive'])for(const energyLog of [-50,-20])for(const countLog of [0,20]){const r=O.run({mode,energyLog,countLog});assert.ok(Number.isFinite(r.tauSeconds)&&r.tauSeconds>0);assert.ok(r.sweep.every(x=>x.tau>0));for(let i=1;i<r.sweep.length;i++)assert.ok(r.sweep[i].tau<r.sweep[i-1].tau);}
for(const p of [null,[],{mode:'brain'},{targetMs:0},{countLog:21},{energyLog:NaN},{coherenceLog:true},{unitLog:-100},{consciousness:1}])assert.throws(()=>O.run(p));
console.log('Orch timescale checks passed: SI units, inverse scaling, additive equivalence, limits, input validation.');
