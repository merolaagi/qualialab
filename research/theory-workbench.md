## 18. Theory workbench: thought, selfhood and quantum proposals

This extension follows the user's questions about thoughts as a personal meshwork of representations and the place of quantum consciousness in that picture. It implements a controlled phase-memory comparison and an evidence guide. The broader thought-and-self architectures below remain proposed experiments. The historical transcript in Appendix A is unchanged; this section is a research synthesis and implementation record, not a verbatim transcript of subsequent messages.

### Separate the explanatory targets

Content is what a thought concerns. Format is how it is represented, for example imagery, language, bodily information or abstract relations. Experience is whether and how that thought is consciously present. A graph of associations describes potential relationships; an account of thought also requires temporal activity, selection, inhibition, learning and interactions with action.

Our working hypothesis is that ongoing thought involves evolving interactions between perception, remembered experience, goals, body-state variables and predictions of action consequences. Some contents may become available to several tasks; some may additionally be attributed to the agent. This is a functional research proposal, not an established sufficient condition for consciousness. Do not assume autobiographical identity or reflective self-awareness is necessary for all experience.

Personal history, bodily perspective, agency attribution and continuity over time are distinct research targets. Candidate modifying factors include learning, expectations, attention, goals, bodily needs, action feedback and temporal persistence. A variable named hunger does not demonstrate felt hunger. A self label is not a self-explanation.

Evidence motivating parts of this framework includes the dissociation of language from other thought capacities, associations between hippocampal activity and self-generated thought, and experimental changes in bodily perspective. These findings do not jointly prove our proposed architecture. Sources: https://doi.org/10.1038/s41586-024-07522-w ; https://doi.org/10.1038/s41467-024-48367-1 ; https://doi.org/10.1126/science.1142175

### Where quantum proposals fit

Distinguish physical implementation, information processing, personal perspective and phenomenal experience. Quantum biology concerns physical mechanisms; quantum brain-processing proposals ask whether specific quantum resources affect neural computation; quantum consciousness adds a claim connecting those mechanisms to experience. Quantum cognition often uses quantum probability as a mathematical description of judgment without asserting a quantum brain.

Orch OR proposes biologically orchestrated quantum processes in microtubules and a proposed objective-reduction mechanism associated with conscious moments. Fisher's nuclear-spin proposal explores a different possible route to quantum neural processing. Neither is implemented in this lab. Sources: https://pubmed.ncbi.nlm.nih.gov/24070914/ ; https://doi.org/10.1016/j.aop.2015.08.020

The protein-optics research cited in the app combines theoretical modeling with fluorescence measurements supporting collective optical effects. It does not demonstrate conscious quantum computation in a living brain. A rat microtubule-stabilizer experiment measured latency to loss of righting reflex under anesthesia; it did not selectively isolate a quantum mechanism, and the reflex is a proxy for consciousness. Sources: https://arxiv.org/abs/2302.01469 ; https://www.eneuro.org/content/11/8/ENEURO.0291-24.2024

Decoherence estimates depend on the proposed states, interactions and environment. Compare the assumptions of competing calculations rather than treating a generic warm-brain objection or a protein quantum effect as conclusive. Sources: https://doi.org/10.1103/PhysRevE.61.4194 ; https://doi.org/10.1103/PhysRevE.65.061901

Quantum probability models of question-order effects do not require physical quantum computation. Context dependence in behavior alone does not identify a quantum substrate. Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC4084470/

### Implemented experiment: phase memory and observational equivalence

Open 06 Theory workbench. The default comparison runs automatically in the browser. Choose a guided experiment, or adjust delay length, phase rotation, dephasing, sample count, seed and intervention step, then press Run comparison. Scrub the delay to inspect its state; Export experiment saves the executed protocol, all curves, pointwise intervals and model boundaries as JSON. Controls edited without running do not alter the displayed result; the executed protocol is printed above the plot. Invalid parameters show an error and preserve the previous result.

The quantum model is one qubit represented by a Bloch vector. Preparation is the plus state (x,y,z)=(1,0,0). Each abstract step rotates x and y about z by angle theta and multiplies both by (1-d). This is a valid phase-damping channel for 0 <= d <= 1; z remains zero. The density matrix has diagonal elements 1/2 and off-diagonal element (x - i y)/2. A final Hadamard followed by a computational-basis measurement gives probability P(0)=(1+x)/2. Every delay is a fresh preparation with a terminal readout, not a series of destructive measurements on one evolving state.

The classical oscillator evolves an independently calculated amplitude A and angle phi: A starts at 1 and is multiplied by (1-d) each step; phi starts at zero and increases by theta each step. Its readout is (1+A cos(phi))/2. The definitions imply exactly the same curve as the quantum model. Agreement is an intentional equivalence control and a mathematical consequence, not a discovery of quantum behavior in a brain. Both descriptions have two evolving real state variables and share the same schedule; there is no fitted model or resource-normalized quantum advantage benchmark.

The stochastic control uses the classical probability at each delay to generate seeded Bernoulli samples. It illustrates finite sampling, not an independently learned or dynamically different explanation. The default is 512 samples per delay; supported counts are 16 to 4096. Error bars are 95% pointwise Wilson intervals. They are not a simultaneous confidence band. Sampling RMSE is computed against the classical expected probabilities across all displayed delays, including the initial preparation. Repeated-seed population inference is not implemented.

The no-phase-memory baseline is an additional reference: it agrees at initial preparation and predicts 1/2 after immediately erasing transverse state information. It is a deliberately restricted baseline, not a fair test against all classical models. The matched oscillator is the stronger classical control.

A phase-flip intervention adds 180 degrees to the classical angle and negates the quantum transverse components after evolution at the selected step. Erasure sets the classical amplitude and both quantum transverse components to zero; later evolution cannot restore them in this model. Dephasing weakens fringe visibility. Purity is (1+x*x+y*y)/2 and normalized coherence is sqrt(x*x+y*y); neither is a measure of consciousness. No entanglement exists in this single-qubit model. The simulator runs on classical hardware, includes no objective-collapse physics, and has no calibrated biological timescale.

### Interpretations that the experiment permits

It demonstrates that the selected input-output behavior fails to distinguish these two physical descriptions. A finite-sampling difference is not evidence of a different exact prediction. Reproducing an interference-shaped curve in software does not establish a physical quantum mechanism, quantum necessity for consciousness, an explanation of qualia, or a connection to Monty's graph-learning states. No Monty-to-qubit coupling is implemented.

The source files are dist/theory-engine.js and dist/theory-ui.js. The offline standalone HTML embeds them. No backend, package installation, account, hardware or network connection is required for the comparison itself. External research links require internet access. The original app's session import/export covers its original agents; the workbench has its own full result export and does not import result files. Refresh restores defaults.

### Competing claims and how they could fail

Functional organization: a specified architecture accounts for a defined capacity. A matched alternative without the proposed mechanism reproducing the effect weakens claims of necessity. Removing a component and degrading all behavior is insufficient; seek selective effects, sham interventions and adequate resource controls.

Quantum contribution: identify a particular physical quantum state, measure its survival in relevant conditions, demonstrate coupling to neural processing and perturb it while controlling ordinary biochemical consequences. An equally predictive non-quantum mechanism undermines a claim that the observed effect uniquely identifies the quantum explanation.

Quantum necessity for experience: this stronger claim additionally needs a defensible connection from the proposed physical process to consciousness. Improved task performance or a correlation with an anesthetic proxy does not establish necessity. Some substrate claims may not be distinguishable by behavior alone; explicitly state the extra assumptions and physical measurements required.

### Proposed next experiment: thought and agency

Compare a sensory baseline, recurrent memory, shared access across tasks and self-prediction. These architectures are not implemented here and are not a ladder of increasing consciousness. Present an object, remove it, introduce a new task after a delay, and occasionally change the action-feedback relationship. Test retained information versus invention, transfer to a held-out task, attribution of self-caused versus external changes and confidence calibration.

Predeclare tasks and predictions. Match training, data and compute; include sham interventions and alternative architectures. Disrupt recurrence, communication or self-prediction separately, repeat independent seeds and report uncertainty and negative findings. A selective impairment of agency attribution with preserved recognition would support a functional dissociation, not prove subjective experience. Human correspondence would require separate empirical work.

Theory comparison should remain open. The COGITATE adversarial collaboration tested predictions of GNWT and IIT and challenged important claims from both. Theory-derived AI consciousness indicators offer provisional assessments rather than a validated consciousness percentage. Sources: https://pubmed.ncbi.nlm.nih.gov/40307561/ ; https://doi.org/10.1016/j.tics.2025.10.011

### Validation for this iteration

Automated tests check known Ramsey probabilities at quarter turns, oscillator equivalence across rotation/dephasing/intervention settings, valid state bounds, erasure and phase-flip limits, deterministic seeded sampling, seed variation and rejection of invalid protocols. Existing engine and Monty API validation still run. These checks establish correctness of the implemented toy protocol; they are not biological or consciousness validation.
