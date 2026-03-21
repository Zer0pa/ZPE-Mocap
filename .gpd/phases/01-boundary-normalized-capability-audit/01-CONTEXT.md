# Phase 1 Context

## Decisions

- **Execution authority is locked to the inner repo**: `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap` outranks outer-workspace lineage.
- **GitHub and Comet are traceability only**: they can log work, but they do not close gates.
- **Local compute first**: Mac M1 Air and Red Magic 10 Pro+ via ADB are the default execution surfaces.
- **RunPod is gated**: do not escalate without an evidenced `IMP-COMPUTE` blocker and an explicit user ask.
- **Disk discipline is active**: monitor space and delete only large outputs that are irrelevant to this mocap workstream.
- **Receipt discipline is active**: every material work run must end with a short lane receipt under repo-local proof/log surfaces.

## Agent's Discretion

- Decide which local docs, scripts, and artifacts are the minimum needed to classify the Phase 1 blockers honestly.
- Prefer direct repo-local command evidence over historical prose.
- If a blocker is caused by path drift, dependency drift, or missing resources, classify it explicitly instead of smoothing it into a generic failure.

## Deferred Ideas

- Do not attempt commercialization closure in this phase.
- Do not ask for RunPod in this phase unless Phase 1 itself proves a real compute blocker.
- Do not spend time polishing docs that are not needed to support the phase result.
