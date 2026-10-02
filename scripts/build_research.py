from pathlib import Path
import json, re, html
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT
intro='''# Qualia Lab

## A general laboratory for experience, representation, and behavior

Consolidated reconstruction of iterations 1-4, extended from redness to five sensory domains. Prepared from the recovered conversation "Comparing Redness Qualia" and the user's subsequent request for a more general app.

## 1. Source status and preservation

The conversation was retrieved through both available pages: 18 turns, from the opening consciousness discussion through the request for one app and a master document. Appendix A preserves the text of every returned user and assistant message in chronological order, including short voice-transcription fragments and incomplete sentences. It is the recovered textual record, not a reconstruction of missing audio.

The older generated apps, README files, and PDFs were referenced by content markers, but the retrieval returned no attachments, artifact payloads, or usable download links. Consequently, this is a new implementation of the functionality described in the conversation. It is not a source-code merge, and pixel-for-pixel or algorithm-for-algorithm equivalence with those missing artifacts cannot be verified. Content-reference markers in the transcript are replaced by an explicit unavailable-artifact notice; no missing artifact is silently presented as recovered.

This README and the companion PDF contain the same research narrative and recovered transcript. The generalized sensory model, precise equations, training procedure, metrics, and interface are implementation choices of this consolidation. They should not be attributed to the earlier prototypes unless explicitly supported by the transcript.

## 2. Quick start

Open dist/index.html in a modern browser. The downloadable app requires no installation, build, API key, or backend. Keep engine.js, app.js, style.css, README.md, and Qualia-Lab-Research.pdf beside index.html. You may also use the hosted app. Computation runs in your browser; a hosted site's access controls are separate from the experiment.

The display fonts may be fetched from Google Fonts when online; system sans-serif fallbacks work offline. Experiments, training, search, and session export work offline. No microphone, camera, scent device, thermal device, or calibrated sensory hardware is used. Sound is an abstract input, not played audio; touch, taste, and smell are not physically delivered stimuli.

Start in Experiment studio. Choose Vision and the Red apple preset. Both transparent-model agents start identical, so their internal distance is zero. Change the preset to Red ball to vary object identity while preserving the initial color controls. Expand the input sections to manipulate lighting, texture, other signals, context, memory associations, and emotion. Expand either agent's History & interventions to change only that agent.

Use the five modality buttons to choose which categorical report is observed. All channels remain part of the common input; changing the selected report does not erase other modalities. Visit Learning & alignment to train the two networks. Visit Behavioral twins to search for equal report/action cases with large hidden-state differences. The Research notebook summarizes the evolution and links these documents.

Export session saves the full input, both agent settings, learned weights when present, memory traces, sequence log, and current derived data as JSON. Import validates a session before accepting it, restores its core experiment state, and invalidates alignment/search results for recomputation. Files stay on your device; the app does not automatically save on refresh. Export before closing if you want to preserve your work.

## 3. The original question: red apple versus red ball

The discussion began with a comparison between the redness of an apple and a ball. This asks several different questions at once: whether their reflected light is the same, whether an observer assigns the same color category, whether the surrounding experience is the same, and whether the felt character of redness itself is the same. The app separates these questions as far as a toy model can.

The user's central intuition was that the same light should produce the same redness. That became a controlled experiment: hold a color-related input fixed while varying object identity and the circumstances around it. In this implementation, apple and ball are numeric object codes, -1 and +1. They are not rendered physical objects or models of surface reflectance. Identical sliders therefore mean identical selected model inputs, not proof of physically identical light at a retina.

The early assistant described apples as deeper or waxier and balls as more uniform or synthetic. Those were illustrative possibilities, not necessary differences or measurements. A waxy ball and a uniform apple are possible. The scientifically useful move is to control texture, lighting, object identity, and associations independently instead of assuming those properties follow from an object name.

The next move was from two objects to two observers: if both say "red," are their experiences the same? Agreement on a word does not uniquely specify their internal state. It also does not establish that their experiences differ. The experiment explores this underdetermination through inspectable computational states, without claiming access to another subject's feeling.

## 4. Identical observers, randomization, and the operational boundary

The user proposed two beings identical in every respect, receiving the same stimulus. In a deterministic program, identical parameters, inputs, history, and memory lead to identical outputs and hidden states. This is a control and follows from the computational setup. Whether complete physical identity also fixes phenomenal experience is a further philosophical question, not something this code settles.

The conversation then introduced randomized histories and systematic additions and subtractions of experience. Randomization supplies varied conditions; it does not create subjectivity. A useful research program asks which changes affect reports, actions, memory, or future responses, and which do not affect the observables under test.

An early suggestion called an internal variable Q the agent's "red experience state." The later conversation corrected this: naming a variable qualia does not make it a measure of experience. This consolidation consistently calls such quantities internal representations. Qualia refers to felt or phenomenal character in the philosophical discussion; no numeric field in the app measures it.

The assistant's early use of "my red" in the transcript is conversational language, not evidence that an AI assistant has color experience. Its hypothetical 650 nm stimulus also does not describe this app's input: the app uses abstract normalized channels rather than a spectral or retinal model.

## 5. Hypotheses and what would count as evidence here

H1 - Complete-state identity: identical deterministic agents, with identical weights, gates, histories, sequence traces, and input, should yield identical hidden vectors and behavior. Nonzero differences in this control indicate a bug, a missing control, or an unrecorded difference.

H2 - Contextual modulation: changing context, association, emotion, sensory channels, or temporal history can change a representation even when the shared external stimulus stays fixed. Evidence consists of reproducible changes under a single controlled intervention. This is a statement about the implemented model.

H3 - Coarse behavioral underdetermination: different hidden vectors can produce the same reported category and the same binary action. Evidence is a reproducible candidate meeting the declared matching criterion. It does not show equality of all possible behavior.

H4 - Coordinate ambiguity: some raw differences can be removed by a mapping between hidden coordinate systems. Evidence is lower error on held-out paired stimuli after fitting a mapping on a separate calibration sample. Low error under a flexible linear mapping is limited evidence about transformability, not proof of equal geometry or consciousness.

H5 - History-dependent learning: under the same architecture, initialization, training budget, and target definitions, different training correlations can lead to different learned states. Repeat seeds and compare held-out performance before generalizing. The current app supports reproducible seeds but does not compute confidence intervals or a population-level conclusion automatically.

H6 - Ingredient sensitivity: removing an input group may make two representations converge or diverge. Compare each intervention against the same frozen baseline. This reveals sensitivity of this model under channel zeroing; it is not a causal finding about human consciousness.

## 6. Iteration history and preserved capabilities

Iteration 1 - Exploratory controls. The first prototype described two subjects and adjustable redness, saturation, illumination, shadow, context, prior memory, emotion, and influence from other senses. It offered identical agents, randomized B context with a fixed stimulus, and an inverted private color-label mapping. The consolidation preserves these as shared controls, separate agent settings, reset/randomization, and explicit report-label swapping.

Iteration 2 - Explicit processing and intervention. The pipeline became stimulus -> sensory processing -> context -> memory -> internal representation -> report/behavior. Users could subtract memory, context, senses, and emotion, randomize B's history, or invert B's internal color mapping. The consolidation preserves a transparent hand-authored model, per-agent gates, paired ablations, and a hidden-unit inversion with an optional compensating readout.

Iteration 3 - Learned representations. Eight-dimensional hidden states replaced a prescribed redness formula. The described experiments were identical histories, different histories with the same color categories, and inverted red/green training labels. Alignment was introduced to distinguish raw coordinate differences from other representational differences. The consolidation includes actual trained hidden weights, these three history protocols, and a calibration/held-out ridge-alignment experiment.

Iteration 4 - Automated search and temporal history. The described app searched 1,000-15,000 conditions for matching report/action with maximal internal divergence within the sample. It added immediately preceding experience and ablation of memory, context, other senses, and shape. The consolidation includes those sample sizes, deterministic search, a temporal state update, loading the winning case, and paired ablations, plus emotion ablation and a stricter probability-matching option.

Generalized edition - The user's follow-up requested a high-end app with a general scope. Vision, sound, touch, taste, and smell now use one engine, one pair of agents, and one experimental workflow. This is an extension made during consolidation, not a claim that all five domains existed in the unavailable original artifacts.

Iteration 5 remains a proposed research direction. The earlier conversation suggested comparing entire representational geometries. This app does not claim to implement that full research program: its alignment test is inherited from iteration 3. Geometry-wide analyses, richer behavior batteries, uncertainty estimates, and systematic repeated-seed studies remain future work.

## 7. Generalized experience model

Each experience contains 16 normalized channels: red/green signal; saturation; illumination; shadow; light angle; object identity; pitch; loudness; texture; temperature; taste; smell; context; prior association; emotion; and previous-state trace. Saturation, illumination, shadow, and loudness lie in [0,1]. The remaining channels lie in [-1,1]. These are chosen abstractions, not calibrated units.

Vision reports green / neutral / red. Sound reports low tone / quiet / high tone. Touch reports cool / neutral / warm. Taste reports bitter / neutral / sweet. Smell reports earthy / neutral / floral. These category axes are deliberately narrow and do not span all possible experiences in a modality. For example, the touch report concerns temperature while texture can influence the hidden state.

Agent history settings add clipped offsets to context, association, and emotion. A sensory gain scales the six nonvisual channels (pitch, loudness, texture, temperature, taste, smell), including the selected channel when the active domain is nonvisual. The nonvisual-senses gate zeros all six channels. It should not be interpreted as preserving the active nonvisual stimulus. Individual raw sliders provide more selective interventions.

The shared red/green channel is transformed using saturation, illumination, shadow, and angle: effective color = color × (0.25 + 0.75 saturation) × (0.45 + 0.55 illumination) × (1 - 0.55 shadow) × (1 - 0.15 |angle|), clipped to [-1,1]. This is a transparent toy formula, not color science or a spectral model. It makes contextual experiments legible while keeping the scientific boundary explicit.

The app distinguishes a raw shared input from the agent's processed input. Equal raw stimulus does not imply equal processed input when agent history or interventions differ. Sequence memories can also differ. All these differences should be disclosed when interpreting a comparison.

## 8. Transparent model and inversion controls

The hand-authored model produces eight tanh-bounded features combining effective color and context, object identity and texture, pitch and loudness, temperature and texture, taste and scent, context and emotion, association and temporal trace, and emotion and scent. These combinations are fixed by the programmer. They demonstrate mechanisms and controls; they do not discover the structure of experience.

Reports are read from these features through simple softmax heads. Approach/avoid is another softmax readout of an explicitly chosen valence combination. These output definitions are intentionally inspectable but arbitrary. The learned model uses the same output vocabulary with trained weights.

Three kinds of inversion must not be conflated. Report endpoint swapping changes the displayed categorical mapping and swaps endpoint probabilities in the active modality. Inverted red/green training labels instead changes B's supervised color targets during training. Hidden-unit inversion negates B's first hidden component at evaluation. None establishes an inverted phenomenal spectrum.

With Compensate the readout enabled, the readout reverses that hidden sign change before producing outputs. This gives a known same-behavior/different-coordinate control by construction. Turn compensation off to see whether the changed unit affects the report or action. In the learned model, the first hidden unit has no guaranteed color meaning, so its inversion is not called a learned redness inversion.

## 9. Learning implementation and reproducibility

Each agent is a 16-input, 8-hidden-unit tanh network. Five categorical heads each have three outputs, and one action head has two outputs, for 17 output logits. A second, 16-output tanh decoder reconstructs the input. All hidden weights, head weights, decoder weights, and biases are updated by stochastic gradient descent.

The objective is the sum of six categorical cross-entropies plus 0.1 times the sum of squared reconstruction errors. The implementation uses a fixed learning rate of 0.025, 700 examples per agent, and a selectable 12, 24, or 48 epochs. The same dataset is reused in a fixed order each epoch. There is no pretrained model, outside AI service, or hidden API call.

Canonical targets use simple thresholds: effective color, temperature, taste, and smell use boundaries at -0.22 and +0.22. Sound is quiet below loudness 0.12; otherwise the sign of pitch chooses low/high. The action target is approach when 0.5 emotion + 0.25 association + 0.15 context + 0.1 taste is nonnegative, otherwise avoid. These are imposed task rules, not discovered meanings.

Identical histories: the two networks begin with identical seeded parameters and see identical samples and targets in identical order. Exact equality is expected. Different associations: the same pseudorandom base draws are used, but B's context correlates negatively with color, association positively with pitch, emotion negatively with taste, and texture negatively with object code. The same target-generating rules apply to the transformed input. Thus action-label frequencies can change as a consequence of changed features; this is not a perfectly matched behavioral training distribution.

Inverted labels: B sees the same inputs, but the green/red color targets are swapped, leaving the middle category and other target rules unchanged. The separate UI report-label swap is not automatically applied. Treat the two interventions independently.

Training resets manual agent interventions and sequence memory, so the chosen protocol has a controlled starting point. Reset identical copies A's learned weights to B if learned models exist; it does not train both from scratch. Fresh common-distribution accuracy is measured on 300 examples for the currently selected domain with canonical labels. For inverted-label B, canonical color accuracy is expected to penalize the intentional mapping change. Training accuracy is not guaranteed and should be inspected.

The seeded generator, fixed sample order, and exported parameters support reproducibility within the same implementation. Floating-point rounding can vary slightly across browser engines. Record the seed, history, epochs, modality, model type, agent interventions, and temporal state with each result. Do not compare different app versions as if they had identical semantics.

## 10. Temporal memory and frozen comparisons

The Previous-state trace input is combined with a per-agent sequence memory before evaluation. Present experience records the current result and then updates each agent's memory: next memory = clip(0.65 × current memory + 0.35 × hidden unit 7). The preview then shows the current raw stimulus under the updated memory. The recorded sequence entry refers to the result before that update.

This update is a chosen, inspectable recurrence, not a trained recurrent network or a biological memory model. Unit 7 in the learned network has no guaranteed memory interpretation. Repeatedly presenting a stimulus can alter its subsequent state because the recurrence feeds back an internal component. Moving sliders alone does not advance the sequence.

Clear sequence resets both sequence traces and the displayed sequence log. It leaves the separate Prior association input and manual Memory association offsets in place. To remove all memory inputs, use the memory gate or memory ablation, which zeros association and previous-state channels.

Search and ablation freeze sequence memories. Search samples a shared previous-state input per candidate and adds each agent's fixed sequence trace. It does not mutate the session by presenting candidates. This makes candidate ranking comparable, while allowing differences in retained history to affect the results.

## 11. Metrics, alignment, and behavioral-twin search

Raw RMS distance is sqrt(mean((hA - hB)^2)) across eight hidden components. Its range is 0-2 for tanh states. Zero means coordinate equality in this model at this input. Cosine similarity measures orientation, not magnitude. If either vector is zero, the implementation returns zero by convention, and the cosine should not be treated as informative.

The coarse match criterion requires the same selected-domain report and the same approach/avoid action. The strict option additionally requires every probability in the selected report head and the approach probability to differ by at most 0.05. The other four report heads are not part of either criterion. Neither criterion establishes complete behavioral equivalence or equality over future sequences.

Search draws 1,000, 5,000, or 15,000 candidate experiences from the common synthetic generator with seed = session seed + 7103. Among matches it retains the case with the largest selected RMS metric. Raw ranking is coordinate-sensitive. Aligned ranking uses the current calibration map and may be selected only after alignment. The winner is a sample maximum, not a globally optimal or statistically certified maximum. No matches is a valid result.

Alignment uses 192 paired calibration inputs and 192 different evaluation inputs from a seeded common distribution. A ridge least-squares affine map fits B's eight components plus an intercept to A's eight components. Ridge regularization is 0.00001 on the normal-equation diagonal, including the intercept. Reported raw and aligned errors are square roots of mean per-example squared RMS errors on the held-out set. Calibration uses fresh synthetic previous-state inputs, without adding current sequence memory; using the map for a sequence-influenced search is therefore an extrapolation worth checking.

The map can rescale and shear, so it is not restricted to orthogonal coordinate changes and does not preserve distances in general. Low aligned error is evidence of predictability under this map on the tested distribution. High aligned error does not rule out nonlinear or other mappings. Neither result establishes phenomenal equivalence. Settings changes invalidate the map so stale calibrations are not silently reused.

Research on comparing neural representations motivates paying attention to invariances and the distribution used for comparisons. Kornblith et al. (2019), Similarity of Neural Network Representations Revisited, introduces CKA and discusses limitations of similarity measures. CKA is a future option here, not a metric implemented in this app. Source: https://proceedings.mlr.press/v97/kornblith19a.html

## 12. Ablation protocol

Run ablations evaluates the current shared raw input with the same two models and frozen memories. It then zeros memory (association and prior-state channels), context, the six nonvisual sensory channels, object shape, or emotion for both agents, one group at a time. An all-five-groups condition is also shown. The baseline has no additional zeros beyond the current manual gates.

Every result displays raw hidden RMS distance, whether the selected report/action still match, and change in distance from baseline. A negative delta means convergence in raw coordinates. A positive delta means divergence. Existing gates remain applied, so ablating an already-disabled group should have no extra effect. No retraining occurs.

Zero is an explicit neutralized code, not literal absence of a sensory apparatus. Such inputs may be outside a network's training distribution. Interactions can mean that separate ablation effects do not add to the combined effect. These limits matter particularly when claiming that a single ingredient explains a difference.

## 13. Suggested experiments

Experiment A - Identity control. Reset identical, keep all controls fixed, and compare both the report/action and all eight components. Repeat after training identical histories. Expected: zero raw distance. If you then give one agent different memories or gates, it is no longer a complete-state identity control.

Experiment B - Apple versus ball. Use the initial red apple, record/export, then use red ball with the same color controls. Compare the object-sensitive features. The preset restores default context and other input controls, so for a strict one-factor experiment after custom edits change only the Object slider instead of selecting a preset.

Experiment C - Context with stimulus fixed. Keep shared inputs fixed, change only B's context offset, and observe representation, report confidence, and action. Return the offset to baseline before testing B's emotion or association separately.

Experiment D - Known coordinate change. Reset identical, enable B's hidden-unit inversion, and keep compensation on. A nonzero raw distance with identical outputs is expected whenever the inverted component is nonzero. Alignment should substantially remove a consistent sign-remapping difference. This validates the coordinate caution; it is not discovery of private feelings.

Experiment E - Learned history. Train identical histories, record the control, then train different associations using the same seed and budget. Compare common-stimulus states, fresh accuracy, held-out alignment errors, and a behavioral-twin search. Repeat other seeds manually before making a broad claim.

Experiment F - Language mapping. Train inverted labels and examine red and green stimuli. Separate category disagreement induced by training from the UI's post-readout label swap. Try sound afterward to show that the training intervention specifically concerned vision labels.

Experiment G - Temporal dependence. Present a strongly emotional or memory-associated stimulus, then switch to a fixed test stimulus. Compare with the same test after Clear sequence. Export both sessions. Use memory ablation to test whether the difference depends on the retained trace.

Experiment H - Search and explain. Train different associations or change B's history; search 5,000 cases with coarse matching; inspect probability gap; try strict matching; load the winner; and run paired ablations. A useful report names the criterion, number of candidates, seed, rank metric, and any outputs that still differ.

Experiment I - Generalization across domains. Repeat a controlled comparison in sound, touch, taste, and smell. The selected report head changes; the common latent state can integrate all channels. Do not interpret successful model behavior as a psychophysical finding about those modalities.

## 14. Scientific boundaries and revised claims

The project can demonstrate properties of explicitly implemented functions: deterministic equality, sensitivity to context, learned task representations, coordinate dependence, temporal recurrence, and coarse output agreement under hidden-state variation. It cannot show whether these programs are conscious, whether two people have the same or different qualia, or which physical process is identical with experience.

The phrase "everything observable agrees" in the iteration-4 conversation was too broad for a report/action test. This app uses "matching selected report and action" and optionally tests a probability tolerance. Other outputs, interventions, or future stimuli can reveal differences. A matched pair on one trial is not a pair equivalent on all possible experiments.

The conversation's statement that physical identity forces a choice between identical experience and a nonphysical difference is a philosophical framing, not an empirical result. The simulator assumes deterministic computational dynamics. It does not test physicalism, dualism, functionalism, illusionism, or any complete theory of consciousness.

The distinction between explaining cognitive functions and explaining felt experience is developed in David Chalmers (1995), Facing Up to the Problem of Consciousness. It motivates this project's boundary between computational outcomes and phenomenal claims; it is not treated as a settled solution. Source: https://consc.net/papers/facing.html

Color experience cannot be reduced here to wavelength; the app has no spectra, cone fundamentals, retinal adaptation, calibrated display measurements, or realistic surface rendering. Its single red/green axis is especially limited. The other sensory axes are equally simplified. Statements about real perception require additional models and empirical evidence.

## 15. Future research, distinct from completed work

The proposed next step is to compare the geometry of complete representational spaces using many stimuli and carefully chosen invariances. Candidate methods include pairwise representational dissimilarity matrices, orthogonal Procrustes baselines, and linear CKA. A richer battery should compare all outputs, confidence, discrimination, generalization, memory, and future-sequence responses.

Use controlled transformations with known ground truth, multiple random seeds, matched training distributions, held-out histories, and uncertainty estimates. Predeclare matching criteria and report nonmatches as well as selected winners. Test how conclusions change when the alignment family changes. Only then consider more realistic sensory encoders or empirical human comparisons with appropriate methodology.

## 16. Files, maintenance, and practical limits

The app source is dist/index.html, dist/style.css, dist/engine.js, and dist/app.js. The engine contains seeded sampling, neural training, transparent features, forward evaluation, and affine alignment. The interface handles experiment state, asynchronous batch search, charts, ablations, temporal updates, and session export/import. The research documents are available at the project root and copied into dist for the download links.

The browser performs all work in memory. Training and search yield between small batches so the UI can show progress; the controls are locked while those jobs run. There is no automatic durable session storage, multi-user collaboration, large model training, or hardware stimulus delivery. Session import accepts at most 8 MB and validates core numeric dimensions and categories. A read-only WebMCP comparison tool is registered only where the browser supports document.modelContext.

The interface offers visual inspection of eight components rather than pretending a two-dimensional plot preserves the entire state. The history strip shows the last 20 steps, while the exported sequence retains the complete session log. Reset identical preserves the current raw stimulus and selected model type; Clear sequence affects only temporal history. Refresh starts a new default session.

## Appendix A. Recovered conversation transcript

This appendix preserves all returned message text in chronological order. Speech disfluencies, very short acknowledgments, and unfinished responses are retained. Generated-artifact placeholders are marked unavailable because the files were not returned. The scientific qualifications above apply to the early statements below; the transcript is an archival record, not an endorsement of every claim.
'''
intro = intro.replace('## Appendix A. Recovered conversation transcript', (ROOT/'research/monty-integration.md').read_text() + '\n\n## Appendix A. Recovered conversation transcript')
intro = intro.replace('## A general laboratory for experience, representation, and behavior', '## A general laboratory for experience, representation, and behavior\n\nLive app: https://qualialab.fueldeskpro.com\n\nRepository: https://github.com/merolaagi/qualialab\n\nThis record preserves the original iterations and adds the real Monty extension in section 17 and theory workbench in section 18. Original browser-only runtime descriptions apply to the first four panels; the new Sensorimotor lab runs on the Mac mini. See DEPLOYMENT.md for publishing and service management.')
intro = intro.replace('## Appendix A. Recovered conversation transcript', (ROOT/'research/theory-workbench.md').read_text() + '\n\n## Appendix A. Recovered conversation transcript')
record=json.loads((ROOT/'research/conversation.json').read_text())
parts=[intro]
for n,turn in enumerate(record['turns'],1):
    parts.append(f'\n### Turn {n}\n')
    for item in turn['items']:
        if item['type']=='userMessage':
            role='User'; text='\n'.join(c.get('text','') for c in item.get('content',[]) if c.get('type')=='text')
        elif item['type']=='agentMessage':role='Assistant';text=item.get('text','')
        else:continue
        text=re.sub(r':chatgpt-content-reference\{index="(\d+)"\}',r'[Generated artifact reference \1 - file unavailable in retrieval]',text)
        parts.append(f'\n**{role}**\n\n{text}\n')
parts.append('''\n## Appendix B. Consolidation request and generalization\n\nThe current request asked for one consolidated Qualia Lab app containing iterations 1-4, one comprehensive README, and one PDF preserving the evolution from the initial red apple versus red ball discussion. The subsequent steering asked to continue making a high-end, general version rather than limiting the intent to describing redness qualia. The generalized edition implements that direction through five abstract sensory domains while retaining the original redness case study.\n\nThis appendix summarizes the current instructions; Appendix A is the recovered source conversation.\n''')
md='\n'.join(parts)
(OUT/'README.md').write_text(md)
(OUT/'dist/README.md').write_text(md)
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyLab',fontName='Helvetica',fontSize=10,leading=15,textColor=colors.HexColor('#25364a'),spaceAfter=9))
styles.add(ParagraphStyle(name='H1Lab',fontName='Helvetica-Bold',fontSize=24,leading=30,textColor=colors.HexColor('#102439'),spaceBefore=12,spaceAfter=16))
styles.add(ParagraphStyle(name='H2Lab',fontName='Helvetica-Bold',fontSize=16,leading=21,textColor=colors.HexColor('#153d53'),spaceBefore=20,spaceAfter=11,keepWithNext=True))
styles.add(ParagraphStyle(name='H3Lab',fontName='Helvetica-Bold',fontSize=12,leading=17,textColor=colors.HexColor('#153d53'),spaceBefore=15,spaceAfter=8,keepWithNext=True))
def clean(t):
    t=t.replace('\u00a0',' ').replace('→',' -> ').replace('≠',' != ').replace('≤',' <= ').replace('×',' x ').replace('Δ','delta ').replace('−','-').replace('↔',' / ').replace('…','...')
    for c in ['—','–','‑']:t=t.replace(c,'-')
    t=t.replace('“','"').replace('”','"').replace('’',"'").replace('‘',"'")
    t=html.escape(t)
    t=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',t)
    t=re.sub(r'(?<!\*)\*([^*]+)\*',r'<i>\1</i>',t)
    t=re.sub(r'(https://[^\s<]+)',r'<link href="\1" color="#24687e">\1</link>',t)
    return t
story=[]
for block in re.split(r'\n\s*\n',md):
    block=block.strip()
    if not block:continue
    if block.startswith('# '):style=styles['H1Lab'];block=block[2:]
    elif block.startswith('## '):
        style=styles['H2Lab'];block=block[3:]
        if block.startswith('Appendix A'):story.append(PageBreak())
    elif block.startswith('### '):style=styles['H3Lab'];block=block[4:]
    else:style=styles['BodyLab']
    story.append(Paragraph(clean(block).replace('\n','<br/>'),style))
def page(canvas,doc):
    w,h=doc.pagesize
    canvas.setStrokeColor(colors.HexColor('#bed1dc'));canvas.line(48,h-37,w-48,h-37)
    canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#587084'))
    canvas.drawString(48,h-28,'QUALIA LAB  /  RESEARCH RECORD')
    canvas.drawRightString(w-48,h-28,'ITERATIONS 1-4 + MONTY + THEORY')
    canvas.drawString(48,28,'Reconstructed functionality · Recovered conversation preserved')
    canvas.drawRightString(w-48,28,str(doc.page))
pdf=OUT/'Qualia-Lab-Research.pdf'
SimpleDocTemplate(str(pdf),pagesize=(612,792),rightMargin=48,leftMargin=48,topMargin=52,bottomMargin=48,title='Qualia Lab - Research evolution and recovered conversation',author='Qualia Lab').build(story,onFirstPage=page,onLaterPages=page)
(OUT/'dist/Qualia-Lab-Research.pdf').write_bytes(pdf.read_bytes())
print(json.dumps({'turns':len(record['turns']),'words':len(md.split()),'pdf':str(pdf)}))
