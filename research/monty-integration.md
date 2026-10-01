## 17. Monty integration: a shared sensorimotor protocol

This extension responds to the request: "can we also integrate tbp.monty to actually have the touch sensation incorporated, and use the same sensory modality technique for all other stimuli as well, because brain processes any stimuli in the same way".

We operationalize the request as learning from touch-related observations and using a common representation interface across sensory modalities. Incorporating touch data is different from producing tactile feelings. A common computational principle is also different from the claim that all biological sensory systems process input identically. This project tests the former without assuming the latter.

The initial consolidated lab remains available unchanged in its original four panels. A fifth panel, Sensorimotor lab, now runs real tbp.monty graph learning on the Mac mini. The original browser-only experiments remain usable offline. This new experiment needs the hosted app and its configured Python runtime; its result is not a browser simulation of Monty.

### What is imported, and what is custom

The integration imports Monty's unmodified State and EvidenceGraphLM classes from the user's merolaagi/tbp.monty fork at commit ed67dcbcacdded0418b59ff47667e59159116aa5. State implements feature-at-pose messages. EvidenceGraphLM learns object models and accumulates evidence about object and pose hypotheses. If this backend is unavailable, the interface reports a failure; it never substitutes the original toy network and calls it Monty.

The surface environment, prescribed scan path, feature generation, two-agent experiment orchestration, API, and browser interface are new Qualia Lab code. No Habitat or TACTO simulator is used. No physical tactile sensor, skin mechanics, force-feedback device, microphone, camera, taste sensor, or scent sensor is connected. Thus this is a genuine Monty integration with synthetic observations, not hardware integration or a physical haptics system.

Source code: https://github.com/merolaagi/tbp.monty/tree/ed67dcbcacdded0418b59ff47667e59159116aa5

Monty's cortical messaging protocol is designed to let sensor and learning modules exchange features with locations and orientations. Its architecture motivates the shared interface used here. It does not validate our invented sensory encoders. Reference: https://docs.thousandbrains.org/docs/cortical-messaging-protocol

Monty's application criteria emphasize sensorimotor information and warn that it is not simply a drop-in learner for arbitrary static data. Our scan supplies spatial information explicitly. Reference: https://docs.thousandbrains.org/docs/application-criteria

### The five adapters

Touch supplies normalized pressure, roughness, and temperature at contact locations. A dimensionless drive parameter affects pressure. The geometric path lies on an analytical sphere, ellipsoid, or radially rippled surface; sensor orientation is supplied from the analytical geometry. This is not a validated contact-force or thermoreceptor model.

Vision supplies synthetic luminance, redness, and contrast. Sound supplies normalized frequency, amplitude, and spectral brightness, with drive affecting amplitude. Taste supplies sweetness, sourness, and bitterness. Smell supplies floral, woody, and intensity features. Each front end has a different explicit transfer function while sending the same structural message type to the same learning algorithm.

All feature values are dimensionless and clipped to [0,1]. There are no hertz, pascals, degrees Celsius, chemical concentrations, or spectral measurements behind these numbers. Sound, taste, and smell reuse virtual spatial poses from the test environment. Whether a realistic sensor for those modalities can provide appropriate spatial information is a research question; the adapter does not solve localization.

Selecting a modality runs separate A/B learning modules for that modality. This version does not combine all five simultaneously, implement native lateral voting between them, or establish cross-modal recognition transfer. It supplies a common implementation path so those future experiments can be designed explicitly.

### Learning and test protocol

Agent A learns all three named objects from 36 noiseless contacts per object, using baseline drive 0.5. Agent B either receives identical training, receives the same locations with each feature increased by 0.22 and clipped, or receives only the first half of the training surface. Object labels supervise graph names during training. The inference target is unlabeled; the true test object is used only to generate the test stream and is not given to the matcher as its object label.

The user selects 12, 24, or 36 test contacts, a modality, object, B history, drive, feature noise, seed, and optional intervention. The test scan has an angular offset of 0.037 radians from the training scan, so it is not a literal replay of those positions. This is still a small, highly structured synthetic recognition task, not a benchmark of real-world generalization.

Both agents receive independent copies of the same test observation. The module sees the actual State location, orientation, on-object marker, and selected features. The same EvidenceGraphLM settings are used across the modalities: maximum spatial match distance 0.018 m, per-feature tolerance 0.22, feature weight 1, a 0.3 m graph extent, 50 voxels per dimension, and at most 128 nodes per graph. A single zero-angle initial rotation prior is supplied. Arbitrary-orientation recognition is not evaluated by this protocol.

The scan is prescribed by Qualia Lab. Although location changes provide sensorimotor information, Monty does not choose the movement in this version; no Monty motor policy or goal-state generator is active. Calling this fully autonomous active touch would overstate the integration.

### Results and interpretation

The display exposes the most-likely object, candidate object set, number of pose/location hypotheses, learned node count, and maximum evidence per named object after every contact. Evidence is unnormalized and may be negative. The chart uses solid lines for A and dashed lines for B. These are neither class probabilities nor measures of consciousness.

Evidence RMS difference compares A and B across the same three named object scores. It is not the original lab's eight-dimensional hidden-state RMS, and there is no assertion that the two measures share a meaningful scale. Matching most-likely objects does not imply matching full evidence, pose hypotheses, or future behavior.

Export full experiment saves the protocol, pinned source revision, graph-node locations, every test location and orientation, sensory features, hypothesis counts, candidate sets, evidence traces, and boundary statements. The browser's replay slider inspects those returned values; it does not regenerate the experiment while scrubbing.

Use sensor sample in studio maps selected feature values into the old 16-channel toy experiment. For example, touch roughness and temperature become texture and temperature inputs. This is an explicit convenience bridge. It does not transform Monty's graph state into the original network's hidden units, and pressure is not represented as a new original-network channel.

### Interventions and controls

The identical-history control should produce exactly equal evidence traces. Biased-feature training tests whether changing the learned sensory associations alters evidence under the same test stream. Partial exploration tests the effect of incomplete graph coverage. These are within-model comparisons.

Zero sensory features removes the three non-morphological feature values at test time while keeping the supplied locations and frames. Freeze reported location gives every test observation the same zero location while keeping the varying frames and features. It tests the contribution of translational information, not the complete removal of pose or embodiment. Neither intervention retrains the object graphs, and both can be outside the training distribution.

Noise is independent zero-mean Gaussian perturbation of the three feature channels before clipping. It is not pose noise or a biological noise model. The seed determines these draws. Contact/acoustic drive affects only the explicitly defined touch and sound features; changing it for vision, taste, or smell has no effect by design.

### Runtime and reproducibility

The existing local Monty Python environment is reused without modifying its installed packages. Missing pure-Python dependencies are installed in a project-local overlay. The tested core runtime uses Python 3.8, NumPy 1.23.5, and Torch 1.11.0; it differs from the fork's full recommended dependency versions. Successful integration checks apply to this graph-learning path only, not the optional simulators or every upstream feature.

The public API accepts only the bounded experiment parameters. It runs one experiment process at a time, limits requests to 4 KB and responses to 2 MB, and stops a run after 90 seconds. The UI can receive a busy response when another visitor is running an experiment. Each request trains fresh graphs; there is no upload endpoint or durable server-side experiment memory. The original offline app and session export still operate independently.

For future iterations, preserve the same GitHub repository and domain. Computational tests run before publication; the real Monty integration suite runs on a configured Mac. Backend code changes require restarting the Qualia Lab server in addition to switching the static release. The setup and test commands are documented in backend/README.md and DEPLOYMENT.md.

### Next experiments

A useful next step is actual calibrated tactile data with measured sensor pose, or a separately validated contact simulator. Add a real sensor adapter only after specifying units, calibration, sampling times, missing-data behavior, and pose estimation. For multisensory studies, define which quantities are genuinely shared across modalities and which are not, then test transfer and voting on held-out objects and trajectories.

The neuroscience motivation remains a hypothesis about reusable cortical computation. It is not evidence that touch, vision, sound, taste, and smell are identical, nor that any trained model has subjective sensations.
