## 19. Orch OR explorer: a conditional timescale test

The user requested using Roger Penrose and Stuart Hameroff's Orchestrated Objective Reduction theory. This extension implements its proposed characteristic relation tau approximately equals hbar / E_G as an assumption explorer. It does not claim to implement the complete theory, generate conscious moments, or validate the proposal. The new panel is 07 Orch OR explorer; the preceding single-qubit workbench remains a separate experiment.

### What comes from the theory

Penrose and Hameroff propose that biologically orchestrated quantum processes involving neuronal microtubules undergo a gravity-related objective reduction associated with conscious moments. The proposed inverse relation connects gravitational self-energy to a characteristic reduction time. E_G refers to the gravitational self-energy of the difference between alternative branch mass distributions, not the electrical energy of a neuron, a stimulus intensity, or simply the total rest energy of some tubulin. Source: https://pubmed.ncbi.nlm.nih.gov/24070914/

The relation alone does not specify a complete dynamical collapse law, a biological orchestration mechanism, a particular conscious content, or a generally applicable outcome-selection algorithm. This software does not implement Penrose's proposed non-computability. Sampling random numbers or assigning a conscious label to an event would not supply those missing elements.

### Implemented calculator and controls

Direct mode takes an assumed total E_G in joules through its base-ten logarithm. The illustrative default log energy of -32 means 1e-32 J, giving tau = 0.01054571817 seconds. The constant used is hbar = 1.054571817e-34 joule-seconds. This is a rounded physical constant, not a fitted parameter. No default is represented as a measured brain value.

Additive mode assumes E_G = N times e_G. N is an effective contribution count, entered as log10(N); e_G is an assumed energy per contribution, entered as log10(joules). This neglects cross terms and requires an appropriate independent-contribution geometry. It is not a general scaling law for coherent assemblies, nor a determination of the number of superposed tubulin molecules. Do not interchange N and N squared scaling without an explicit mass-distribution calculation. Effective counts may be continuous for sensitivity analysis.

The independently supplied coherence lifetime is in seconds, entered as log10(seconds). The ratio shown is coherence lifetime divided by tau. A ratio below one places the assumed coherence lifetime before the proposed characteristic OR timescale. A ratio at or above one meets only this conditional timescale comparison. It does not establish that the state exists, is biologically realizable, or is conscious. Real decoherence is not necessarily a sharp cutoff; this comparison is not an event simulation or a probability of successful objective reduction.

The chosen target is in milliseconds, converted to seconds before calculating required E_G = hbar / target time. A 25 ms target requires about 4.2183e-33 J in this convention. The default target is illustrative; it is not an established duration of conscious experience. The app also shows the algebraically required effective contribution count for the assumed per-contribution energy, with that assumption printed alongside the result even in direct mode.

The plot sweeps E_G from 1e-50 to 1e-20 J and shows the corresponding characteristic timescale. Both axes are logarithmic, with horizontal references for assumed coherence lifetime and chosen target. A selected energy outside the plot range retains its numerical result and displays an explicit off-scale notice. The curve is generated from the equation, not fitted to experimental or biological data.

Change assumptions and press Calculate timescale. Export assumptions saves the executed parameters, constants, derived quantities, complete sweep, and interpretation boundaries. Editing controls alone does not update the executed result. Invalid inputs retain the previous result and display an error. Refresh restores defaults. Export is specific to this explorer; it is not integrated with the original studio's session import.

### What is deliberately not inferred

No spatial mass distribution, tubulin displacement, density smoothing, environmental coupling or measured coherence lifetime is inferred. No quantum state is evolved and no collapse event or outcome is generated. There is no physical quantum hardware, gravity simulation, consciousness metric, biological neural model, or coupling to Monty's internal states. This is a classical numerical calculation of the consequences of supplied assumptions.

Calculating E_G for a realistic microtubule proposal would require explicit alternative geometries, constituent masses, displacement scales and a well-defined mass-density convention. The next biophysical step is to specify and justify those quantities, then compare sensitivity across plausible alternatives, not tune them until a desired conscious timescale appears.

### Constraints and falsifiability

Radiation searches constrain particular dynamical Diosi-Penrose models and parameter choices. The 2020 underground experiment and the 2022 analysis of implications for Orch OR are relevant constraints, not a universal refutation or validation of every version of Penrose's proposal. The calculator does not apply a numerical experimental exclusion region because its supplied E_G and coherence time do not specify the full model needed to translate those bounds. Sources: https://doi.org/10.1038/s41567-020-1008-4 ; https://pubmed.ncbi.nlm.nih.gov/35617922/

A substantive test should specify a physical state, measure its coherence under relevant conditions, establish coupling to neural processing and distinguish the predicted mass-displacement dependence from ordinary biochemical and environmental effects. Evidence that a drug changes microtubule function or an anesthetic response does not uniquely identify objective reduction. Even verification of a collapse mechanism would still require an account connecting that mechanism to particular perceptions, thoughts and selfhood.

### Validation and implementation

Source files are dist/orch-engine.js and dist/orch-ui.js, embedded into the served page and standalone download by the build script. Tests verify SI-unit conversion, the default numerical result, inverse energy-time scaling, direct versus additive agreement, monotonic sweeps, finite positive limits and rejection of invalid inputs. These are numerical correctness checks, not evidence for biological or phenomenal claims.
