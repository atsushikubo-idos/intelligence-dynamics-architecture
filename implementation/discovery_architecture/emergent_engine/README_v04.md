# IDOS Discovery Architecture — Composed Dynamic Cycle v0.4

## Purpose / scope
An incremental extension of v0.3. No changes to Reference v1.1/v1.2. An external model (when configured) may propose a *new arithmetic observation metric* without the experimenter specifying the desired formula. The engine checks the formula without executing model-supplied code, explicitly reviews the reference-frame transition, recomputes measurements, changes the eligible intervention set, executes a sandbox action, and feeds the resulting world state and history into the next cycle.

## Four acceptance conditions
1. Candidate proposal: supported in `LiveComposedSource` via an external API, **not live-tested here**. Replay is synthetic, with predetermined fixture candidates.
2. Measurement update: generated expression is parsed through a minimal safe arithmetic grammar over `wealth`, `energy`, `output`, `capacity`. The measured objective changes at runtime. Does **not** create new physical sensors.
3. Intervention update: eligible interventions change with the new frame, but stay within a static, approved sandbox action registry. No dynamic executable actions or permission escalation.
4. Cycle: intervention effects modify the actual sandbox world, read anew on subsequent iterations; tested 3 cycles. Historical records and old-frame measurements are retained.

## Files
- `composed_cycle.py`: safe metric grammar and measurement/authorization/action loop.
- `live_composed.py`: optional real AI candidate provider; requires `OPENAI_API_KEY`. Generates declarative proposals, never executes arbitrary code.
- `run_v04.py`: fixture replay or live-mode driver.
- `test_composed_cycle.py`: new 5 tests; plus 5 tests carried forward from v0.3.
- `engine.py`, `dynamic_cycle.py`, `reference_transition.py`, `discovery_architecture.py`: copied dependencies from v0.3, unmodified.
- `replay_results.json`: **synthetic replay**, NOT a real AI result.

## Run locally
```bash
cd emergent_engine
python -m unittest test_composed_cycle test_dynamic_cycle -v
python run_v04.py --mode replay --cycles 3 --approve-sandbox --out replay_results.json
# For real AI proposals, configure an API key in your own secure environment:
export OPENAI_API_KEY='...'
python run_v04.py --mode live --model gpt-4.1-mini --cycles 3 --approve-sandbox --out live_results.json
```

The flag `--approve-sandbox` authorizes *only* changes inside the local simulation; it does not approve external actions. When omitted, frame transitions remain pending and are not applied. The external API may require a different supported model name or parameters.

## Limitations and safeguards
- A new metric can be just a recombination of existing information; semantic novelty is NOT established.
- There is no independent verification that a novel metric better explains the world, nor an effect-size / causal claim.
- Real AI inputs are bounded to simulation state and history. A prompt specifying a concept like `energy` as an answer is deliberately avoided, though variable names are visible to the model.
- Authorized actions, sensors, and simulation dynamics remain pre-established. This is an experiment platform, not open-world invention.
- For real-world experiments: hold out evaluation cases, establish baseline comparisons, log model/version/time and raw outputs, use explicit approval gates, and avoid self-grading discoveries.
