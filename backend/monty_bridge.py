"""Real Monty graph learning over explicitly synthetic feature-at-pose streams.

The environment/adapters are Qualia Lab code. State and EvidenceGraphLM are
imported unchanged from the pinned tbp.monty source. No tactile hardware or
phenomenal experience is simulated by the learning module itself.
"""
from __future__ import annotations

import contextlib
import copy
import json
import logging
import math
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
PIN = 'ed67dcbcacdded0418b59ff47667e59159116aa5'
sys.path[:0] = [str(ROOT / '.runtime/python-overlay'), str(ROOT / '.runtime/monty-source/src')]

import numpy as np
from tbp.monty.frameworks.models.states import State
from tbp.monty.frameworks.models.evidence_matching.learning_module import EvidenceGraphLM

logging.basicConfig(level=logging.ERROR)
OBJECTS = ('sphere', 'ellipsoid', 'ripple')
MODALITIES = ('touch', 'vision', 'sound', 'taste', 'smell')
FEATURES = {
    'touch': ('pressure', 'roughness', 'temperature'),
    'vision': ('luminance', 'redness', 'contrast'),
    'sound': ('frequency', 'amplitude', 'spectral_brightness'),
    'taste': ('sweetness', 'sourness', 'bitterness'),
    'smell': ('floral', 'woody', 'intensity'),
}

def validate(raw):
    if not isinstance(raw, dict) or set(raw) - {'modality', 'object', 'history', 'steps', 'force', 'noise', 'seed', 'ablation'}:
        raise ValueError('Unknown request field')
    p = dict(modality='touch', object='sphere', history='identical', steps=24, force=.5, noise=0., seed=42, ablation='none')
    p.update(raw)
    for field, choices in [('modality', MODALITIES), ('object', OBJECTS), ('history', ('identical', 'biased', 'partial')), ('ablation', ('none', 'features', 'location'))]:
        if p[field] not in choices:
            raise ValueError('Invalid ' + field)
    for field, low, high in [('steps', 8, 36), ('seed', 1, 1000000)]:
        if type(p[field]) is not int or not low <= p[field] <= high:
            raise ValueError('Invalid ' + field)
    for field, low, high in [('force', .1, 1.), ('noise', 0., .2)]:
        if type(p[field]) not in (int, float) or not math.isfinite(p[field]) or not low <= p[field] <= high:
            raise ValueError('Invalid ' + field)
    return p

def surface(name, theta):
    """Known synthetic contact geometry; dimensions in metres, not an image encoder."""
    if name in ('sphere', 'ellipsoid'):
        axes = np.array([.06, .06, .06]) if name == 'sphere' else np.array([.043, .043, .09])
        latitude = .3 * math.sin(2 * theta)
        unit = np.array([math.cos(latitude) * math.cos(theta), math.cos(latitude) * math.sin(theta), math.sin(latitude)])
        location = axes * unit
        normal = location / (axes ** 2)
    else:
        radius = .052 + .008 * math.cos(3 * theta)
        derivative = -.024 * math.sin(3 * theta)
        location = np.array([radius * math.cos(theta), radius * math.sin(theta), .018 * math.sin(2 * theta)])
        normal = np.array([radius * math.cos(theta) + derivative * math.sin(theta), radius * math.sin(theta) - derivative * math.cos(theta), 0.])
    normal /= np.linalg.norm(normal)
    tangent = np.cross(np.array([0., 0., 1.]), normal)
    tangent /= np.linalg.norm(tangent)
    return location, np.array([normal, tangent, np.cross(normal, tangent)])

def sample(name, modality, theta, force, rng, noise=0., bias=0., ablation='none'):
    location, frame = surface(name, theta)
    idx = OBJECTS.index(name)
    # Deliberately different front-end transfer functions. A common protocol does
    # not mean that the biological receptors or feature meanings are identical.
    if modality == 'touch':
        values = [force * (.9 - .18 * idx), .15 + .28 * idx + .08 * math.sin(5 * theta), .45 + .12 * idx]
    elif modality == 'vision':
        values = [.5 + .25 * math.cos(theta), .8 - .28 * idx, .18 + .26 * idx]
    elif modality == 'sound':
        values = [.2 + .28 * idx, force * (.55 + .15 * math.cos(theta)), .3 + .18 * idx]
    elif modality == 'taste':
        values = [.8 - .25 * idx, .18 + .24 * idx, .1 + .15 * idx + .05 * math.sin(theta)]
    else:
        values = [.75 - .22 * idx, .15 + .28 * idx, .5 + .12 * math.cos(theta)]
    values = np.clip(np.array(values) + bias + rng.normal(0, noise, 3), 0., 1.)
    if ablation == 'features':
        values[:] = 0
    if ablation == 'location':
        location = np.zeros(3)
    feature_dict = {key: float(value) for key, value in zip(FEATURES[modality], values)}
    return State(location=location,
                 morphological_features={'pose_vectors': frame, 'pose_fully_defined': True, 'on_object': 1},
                 non_morphological_features=feature_dict, confidence=1., use_state=True,
                 sender_id='patch', sender_type='SM')

def train(modality, history, seed):
    lm = EvidenceGraphLM(max_match_distance=.018,
                         tolerances={'patch': {k: .22 for k in FEATURES[modality]}},
                         feature_weights={'patch': {k: 1. for k in FEATURES[modality]}},
                         max_graph_size=.3, num_model_voxels_per_dim=50,
                         max_nodes_per_graph=128, gsg_class=None,
                         use_multithreading=False,
                         hypotheses_updater_args={'initial_possible_poses': [[0, 0, 0]]})
    lm.mode = 'train'
    rng = np.random.RandomState(seed)
    for name in OBJECTS:
        lm.pre_episode({'object': name, 'quat_rotation': [1., 0., 0., 0.]})
        angles = np.linspace(0, 2 * math.pi, 36, endpoint=False)
        if history == 'partial':
            angles = angles[:18]
        for theta in angles:
            observation = sample(name, modality, theta, .5, rng, bias=.22 if history == 'biased' else 0.)
            lm.exploratory_step([observation])
        lm.detected_object = name
        lm.detected_rotation_r = None
        lm.buffer.stats['detected_location_rel_body'] = lm.buffer.get_current_location(input_channel='first')
        lm.post_episode()
    return lm

def evidence(lm):
    ids, scores = lm.get_evidence_for_each_graph()
    scores = {str(key): float(val) for key, val in zip(ids, scores)}
    return {name: scores.get(name, 0.) for name in OBJECTS}

def run(raw):
    p = validate(raw)
    started = time.monotonic()
    a = train(p['modality'], 'identical', p['seed'])
    b = copy.deepcopy(a) if p['history'] == 'identical' else train(p['modality'], p['history'], p['seed'])
    models = [a, b]
    graph_nodes = [{name: lm.get_graph(name, 'patch').pos.tolist() for name in OBJECTS} for lm in models]
    for lm in models:
        lm.mode = 'eval'
        # The target label is deliberately not supplied to recognition.
        lm.pre_episode({'object': 'unlabeled', 'quat_rotation': [1., 0., 0., 0.]})
    rng = np.random.RandomState(p['seed'] + 109)
    trajectory = []
    for index, theta in enumerate(np.linspace(.037, 2 * math.pi + .037, p['steps'], endpoint=False)):
        observation = sample(p['object'], p['modality'], theta, p['force'], rng, noise=p['noise'], ablation=p['ablation'])
        outputs = []
        for lm in models:
            lm.add_lm_processing_to_buffer_stats(lm_processed=True)
            lm.matching_step([copy.deepcopy(observation)])
            scores = evidence(lm)
            mlh = lm.get_current_mlh()
            outputs.append({'hypothesis': str(mlh['graph_id']), 'evidence': scores,
                            'possibleMatches': list(lm.get_possible_matches()),
                            'hypothesisCount': int(sum(len(values) for values in lm.evidence.values()))})
        gap = float(np.sqrt(np.mean([(outputs[0]['evidence'][key] - outputs[1]['evidence'][key]) ** 2 for key in OBJECTS])))
        trajectory.append({'step': index + 1, 'location': observation.location.tolist(),
                           'poseVectors': observation.get_pose_vectors().tolist(),
                           'features': observation.non_morphological_features, 'agents': outputs,
                           'evidenceRMS': gap, 'sameHypothesis': outputs[0]['hypothesis'] == outputs[1]['hypothesis']})
    return {'engine': 'tbp.monty EvidenceGraphLM', 'sourceCommit': PIN, 'sourceRepository': 'https://github.com/merolaagi/tbp.monty',
            'inputKind': 'synthetic feature-at-pose observations; no tactile hardware',
            'protocol': p, 'objects': list(OBJECTS), 'features': list(FEATURES[p['modality']]),
            'trainingNodes': graph_nodes, 'trajectory': trajectory, 'elapsedSeconds': round(time.monotonic() - started, 3),
            'boundaries': ['Evidence scores are not probabilities or measures of qualia.',
                           'Idealized geometry and sensor pose are supplied; movement is a scripted scan, not Monty motor planning.',
                           'Sound, taste, and smell use experimental synthetic adapters, not validated biological models.',
                           'Each run retrains small object graphs. No session data or trained graphs persist between requests.']}

if __name__ == '__main__':
    for line in sys.stdin:
        try:
            with contextlib.redirect_stdout(sys.stderr):
                result = run(json.loads(line))
            print(json.dumps({'ok': True, 'result': result}, allow_nan=False), flush=True)
        except Exception as error:
            logging.exception('Monty experiment failed')
            print(json.dumps({'ok': False, 'error': str(error)}), flush=True)
