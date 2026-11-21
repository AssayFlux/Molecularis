# Kinetics Runtime

Status: Python v1 local MSDE reference integration.

A caller constructs an immutable `ReactionNetworkDocument`, ingests it as a content-addressed MSDE artifact, and executes a registered capability through a Rulebook. Loading verifies media type, schema identity, artifact digest and metadata. The service does not dynamically load code from artifacts.

Operations: `validate`, `simulate`, `michaelis_menten`, and `fit_michaelis_menten`. Network operations require one artifact; standalone curve operations accept parameters only. The simulation operation requires positive `duration` and `step_size`, an integer-multiple horizon and bounded `max_steps`. The platform budget further caps candidate steps and artifact bytes.

Execution is in-process and synchronous. It is deterministic for identical inputs and Python numerical behavior, but has no preemptive cancellation or OS isolation. Production deployment requires a separately sandboxed worker and explicit CPU/memory limits. No external scientific executable is required.
