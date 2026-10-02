const assert=require('node:assert/strict');const T=require('../dist/theory-engine.js');const close=(a,b)=>assert.ok(Math.abs(a-b)<1e-10,`${a} != ${b}`);
// Ramsey analytic limits and channel positivity, including interventions.
for(const phase of [0,45,90,180])for(const dephasing of [0,.04,.5,1])for(const intervention of ['none','flip','erase']){
 const r=T.run({phase,dephasing,intervention});assert.ok(r.maxDifference<1e-12);
 for(const a of r.rows){assert.ok(a.quantum>=0&&a.quantum<=1);assert.ok(a.purity>=.5-1e-12&&a.purity<=1+1e-12);assert.ok(a.coherence<=1+1e-12);close(a.purity,(1+a.coherence*a.coherence)/2);assert.ok(a.interval95[0]<=a.stochastic+1e-12&&a.interval95[1]>=a.stochastic-1e-12);}
}
let r=T.run({phase:90,dephasing:0});[1,.5,0,.5,1].forEach((v,i)=>close(r.rows[i].quantum,v));
r=T.run({phase:0,dephasing:0,intervention:'flip',at:2});close(r.rows[1].quantum,1);close(r.rows[2].quantum,0);
r=T.run({intervention:'erase',at:2});for(const a of r.rows.slice(2)){close(a.quantum,.5);close(a.coherence,0);close(a.purity,.5);}
assert.deepEqual(T.run({seed:92}),T.run({seed:92}));assert.notDeepEqual(T.run({seed:92}).rows.map(x=>x.stochastic),T.run({seed:93}).rows.map(x=>x.stochastic));
for(const p of [{steps:2},{steps:4,at:5},{seed:true},{shots:1},{phase:NaN},{dephasing:2},{intervention:'collapse'},{unknown:1}])assert.throws(()=>T.run(p));
console.log('Theory checks passed: Ramsey limits, oscillator equivalence, valid states, interventions, reproducible sampling, strict inputs.');
