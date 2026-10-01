import assert from 'node:assert/strict';
import {validateMonty} from '../backend/monty-api.mjs';
assert.equal(validateMonty({}).modality,'touch');
for(const modality of ['touch','vision','sound','taste','smell'])assert.equal(validateMonty({modality}).modality,modality);
for(const value of [null,[],{modality:'other'},{steps:10000},{steps:12.5},{seed:true},{noise:NaN},{force:0},{command:'anything'}])assert.throws(()=>validateMonty(value));
console.log('Monty API protocol validation passed. Real Python integration is tested separately on the Mac.');
