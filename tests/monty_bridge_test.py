"""Integration checks against the actual pinned Monty implementation."""
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'backend'))
from monty_bridge import MODALITIES, run, validate, EvidenceGraphLM

assert '.runtime/monty-source' in sys.modules[EvidenceGraphLM.__module__].__file__
summary = {}
for modality in MODALITIES:
    result = run({'modality': modality, 'steps': 12})
    assert len(result['trajectory']) == 12
    assert all(t['evidenceRMS'] == 0 for t in result['trajectory'])
    assert all(t['sameHypothesis'] for t in result['trajectory'])
    assert result['trajectory'][-1]['agents'][0]['hypothesis'] == 'sphere'
    assert all(len(points) > 10 for points in result['trainingNodes'][0].values())
    json.dumps(result, allow_nan=False)
    summary[modality] = result['trajectory'][-1]['agents'][0]['hypothesis']
biased = run({'modality': 'touch', 'history': 'biased', 'steps': 12})
assert max(t['evidenceRMS'] for t in biased['trajectory']) > .1
partial = run({'modality': 'touch', 'history': 'partial', 'steps': 12})
assert sum(map(len, partial['trainingNodes'][1].values())) < sum(map(len, partial['trainingNodes'][0].values()))
for ablation in ['features', 'location']:
    data = run({'modality': 'touch', 'ablation': ablation, 'steps': 12})
    assert len(data['trajectory']) == 12
    json.dumps(data, allow_nan=False)
for invalid in [{'steps': 100000}, {'modality': 'unknown'}, {'seed': True}, {'noise': float('nan')}, {'path': '/etc/passwd'}]:
    try:
        validate(invalid)
        raise AssertionError('Invalid request accepted')
    except ValueError:
        pass
print(json.dumps({'passed': True, 'realMonty': EvidenceGraphLM.__name__, 'modalityIdentityControls': summary,
                  'biasedTouchMaxEvidenceRMS': max(t['evidenceRMS'] for t in biased['trajectory']),
                  'partialHistory': 'fewer graph nodes', 'ablations': ['features', 'location']}))
