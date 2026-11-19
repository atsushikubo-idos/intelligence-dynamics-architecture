# Test Instructions — English Research Preview v0.49

1. Open `simulator/index.html` in a modern browser (or serve `simulator/` with a local static server).
2. Check that the initial **Adaptive interaction** scenario contains **11 synthetic events**.
3. Advance one event; the time display must change from `0 / 11` to `1 / 11`.
4. Select `External observer (fallible)` and inspect the reference axes and rule values.
5. Click **Compare assumptions**. The compared events must be identical, and the output must say `causal_claim: false`.
6. Click **Run scoped checks**; expect **42 passed, 0 failed**.
7. Switch to both other presets and click **Run experiment**.
8. Click **Export audit JSON**; confirm it identifies the data as `synthetic: true` and states the limitations.

## Covered checks

Three synthetic presets × two feedback assumptions × six checks = 36 assertions. Six further checks cover deterministic identical-run control, same-event comparison, explicit absence of a causal claim, unknown Future Updateability, non-measured Path Closure, and the count of five updating units. **42 assertions total.**

The tests do not validate theory, predictions, accuracy against real data, security, full integration of earlier experimental panels, or accessibility compliance. See `browser_test_report.json` for an actual Chromium test capture.
