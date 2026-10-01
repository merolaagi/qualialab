const assert=require('node:assert/strict');const Q=require('../dist/engine.js');
(async()=>{
const raw=Q.base(),a=Q.agent(),b=Q.agent();assert.equal(Q.compare(Q.evaluate(raw,a),Q.evaluate(raw,b)).distance,0);
b.invert=true;let x=Q.evaluate(raw,a),y=Q.evaluate(raw,b);assert.deepEqual(x.prob,y.prob);assert.equal(x.actionProbability,y.actionProbability);assert(Q.compare(x,y).distance>0);
let map=Q.alignment(null,[a,b],42,0);assert(map.aligned<.0001);assert(map.raw>.1);
const identical=await Q.trainPair({seed:42,history:'identical',epochs:12,samples:700});assert.deepEqual(identical.a,identical.b);
const different=await Q.trainPair({seed:42,history:'different',epochs:24,samples:700});assert.notDeepEqual(different.a,different.b);
const inverted=await Q.trainPair({seed:42,history:'inverted',epochs:24,samples:700});let acc=[0,0],r=Q.rng(9043),match=0,best=0;
for(let i=0;i<5000;i++){const raw=Q.sample(r);const A=Q.evaluate(raw,a,different.a),B=Q.evaluate(raw,a,different.b),c=Q.compare(A,B);assert(Number.isFinite(c.distance));if(c.same){match++;best=Math.max(best,c.distance);}if(i<300){const target=Q.labels[0][Q.targets(Q.effective(raw,a))[0]];acc[0]+=A.report===target;acc[1]+=B.report===target;}}
assert(match>0);assert(best>0);assert(acc[0]>200);assert(acc[1]>200);
const gate=Q.agent();gate.gates.memory=false;assert.deepEqual(Q.evaluate(raw,gate,different.a),Q.evaluate(raw,gate,different.a,0,['memory']));
const identityLearned=Q.alignment(identical,[a,a],42,0);assert.equal(identityLearned.raw,0);assert(identityLearned.aligned<.0001);
console.log(JSON.stringify({passed:true,identicalMaxDifference:0,compensatedInversion:{raw:map.raw,aligned:map.aligned,agreement:map.agreement},visionAccuracy:acc.map(n=>n/300),search:{cases:5000,matches:match,maximumRawRMS:best},invertedRedReports:[Q.evaluate(raw,a,inverted.a).report,Q.evaluate(raw,a,inverted.b).report]},null,2));
})();
