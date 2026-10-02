/* Conditional Penrose OR timescale calculator. No collapse dynamics or consciousness model. */
(function(root){
'use strict';const HBAR=1.054571817e-34;
function run(input={}){
 if(!input||Array.isArray(input)||typeof input!=='object')throw Error('Expected parameters');
 const p={mode:'direct',energyLog:-32,unitLog:-42,countLog:10,coherenceLog:-3,targetMs:25,...input};
 const ranges={energyLog:[-50,-20],unitLog:[-55,-30],countLog:[0,20],coherenceLog:[-15,1],targetMs:[.1,1000]};
 for(const k of Object.keys(input))if(!['mode',...Object.keys(ranges)].includes(k))throw Error('Unknown parameter');
 if(!['direct','additive'].includes(p.mode))throw Error('Invalid energy model');
 for(const [k,[lo,hi]]of Object.entries(ranges))if(typeof p[k]!=='number'||!Number.isFinite(p[k])||p[k]<lo||p[k]>hi)throw Error('Invalid '+k);
 const unitEnergy=10**p.unitLog,count=10**p.countLog,energy=p.mode==='direct'?10**p.energyLog:unitEnergy*count;
 const tau=HBAR/energy,coherenceTime=10**p.coherenceLog,targetTime=p.targetMs/1000,targetEnergy=HBAR/targetTime;
 const sweep=Array.from({length:61},(_,i)=>{const energyLog=-50+i*.5;return{energyLog,energy:10**energyLog,tau:HBAR/10**energyLog};});
 return{schema:'qualialab-orch-timescale-v1',protocol:p,hbarJs:HBAR,energyJ:energy,tauSeconds:tau,coherenceSeconds:coherenceTime,ratio:coherenceTime/tau,targetSeconds:targetTime,targetEnergyJ:targetEnergy,requiredEffectiveUnits:targetEnergy/unitEnergy,sweep,assumptions:['tau = hbar / E_G is a hypothesized characteristic timescale, not a deterministic event schedule.','E_G is the gravitational self-energy of the difference between branch mass distributions, not electrical energy or ordinary stimulus strength.','Additive E_G = N e_G neglects cross terms and requires an assumed independent-contribution geometry. N is not a measured tubulin count.','Coherence lifetime is a user assumption, not inferred from this energy.','No state evolution, objective reduction event, outcome selection, biological orchestration, or consciousness measure is implemented.']};
}
root.OrchLab={run,HBAR};if(typeof module!=='undefined')module.exports=root.OrchLab;
})(typeof globalThis!=='undefined'?globalThis:this);
