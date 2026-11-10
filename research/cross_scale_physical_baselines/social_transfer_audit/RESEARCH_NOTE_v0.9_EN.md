# IDOS Cross-Scale Connection Mechanism Audit v0.9

## Scope and research question

This is a **synthetic social transition experiment**, created after the separate, physical hydrogen calculations (electronic structure, dissociation, nuclear dynamics, finite oscillator baths). It asks whether a relationship's *formation, persistence, interruption and reopening* require distinguishable observations. It does **not** derive a social law from quantum chemistry. There is no energy conservation assumption for human or AI relations.

**Hypothesis H1 (testable in this stipulated model):** connection at time *t* is insufficient to predict connection after the mediator departs; retained verified/authorized transfer matters.

**H2:** a declared veto blocks connection, even if a mediator is available.

**H3:** an external interruption can break a currently active relation without deleting a previously certified, reusable route; reopening can then occur with fresh consent.

**Negative control:** an independent Boolean baseline using exactly the same context should make identical initial-formation predictions. A favorable difference against that baseline would indicate a bug, not a discovery.

## Explicit inputs

Two actors A/B each provide declared consent. A third party has `mediator_present`, `mediation_verified` and `transfer_authorized` flags. The actors may already share a direct protocol. `certified_bridge` is a historical state set only after the explicitly verified and authorized transfer. `external_disruption` interrupts active connection, without automatically revoking the certificate. Consent withdrawal **does** revoke it by design. These are modelling stipulations and do not authenticate consent, prove semantic fidelity, or demonstrate learning of new protocols.

## State and transition equations

Let \(c_A,c_B,m,v,d,t,h,s\) respectively be both consent declarations, mediator availability, declared verification, direct protocol, transfer authorization, retained certification, and an external shock, with Boolean operations.

\[
q_t = c_A \land c_B, \qquad
r_t = d \lor (m\land v) \lor h_t.
\]

\[
\mathrm{Connected}_{t+1}=q_t\land r_t\land \neg s_t.
\]

\[
h_{t+1}=\begin{cases}
0 & \neg q_t\\
h_t\lor(m\land v\land t) & q_t.
\end{cases}
\]

A connection is *formed* if it becomes active from an inactive state; *maintained* if it stays active; *interrupted* if a shock removes it; *reopened* if it later becomes active again. A certified route is one artificial way of making the relationship less dependent on the mediator. These equations are not novel mathematics.

## Protocol

1. Exhaustively enumerate 64 combinations of six Boolean inputs (`a_consents`, `b_consents`, `mediator_present`, `mediation_verified`, `shared_direct_protocol`, `transfer_authorized`). Initial states are disconnected and un-certified.
2. Compare an independently written direct-Boolean baseline with the transition implementation on all 64 inputs.
3. Take the initial active-connection subset. Run the same counterfactual intervention on every member: mediator unavailable, no direct protocol, no fresh mediation, continuing consent.
4. Predict the post-departure connection using (a) present connection only and (b) present connection plus historical certificate. Compute exact empirical conditional entropy and Bayes-optimal Brier score over this **uniform enumeration design**.
5. Exercise revocation, disruption, continued consent and re-opening. Tests enforce prior evidence-ID retention and ensure refusal is not overridden by a third party.

## Reproduced findings

See `results_v09.json`, produced by the exact code in this folder. Ten of 64 initial conditions permit connection. After the fixed mediator departure intervention, two of these ten stay connected. For that selected artificial 10-case distribution, the current-connected bit yields conditional entropy **0.721928 bit** and Bayes-optimal Brier **0.16**. Adding the transfer-certificate bit gives both **0**. Independent full-context Boolean comparator agrees on **64/64** initial cases. These are exact frequencies of this selected artificial enumeration, **not sampled population probabilities**.

## What is established versus not established

**Established within this model:** history-dependent persistence, explicit refusal, conditional mediator effect, post-shock reopening, and loss of predictive information when a transition-relevant history bit is discarded.

**Not established:** that physical molecular mechanisms carry over to social systems; that `certified_bridge` is learned from data; that third-party translation is meaningful; empirical consent or agency; new generative mechanisms; statistical generalization; an IDOS predictive advantage over full-information or standard state-space baselines; real-world mutual understanding. Data-driven discovery and out-of-sample comparison remain separate unsolved tasks.

## Link to existing IDOS modules (proposed, not implemented)

- `Social Connection Architecture`: connection is a declared state, not evidence that participants mutually understood one another.
- `Connection Boundary / Continuity`: mapping candidate for consent / holding / refusal / post-shock reopening / provenance. No existing files are modified; this package deliberately does **not** claim an imported dependency or an integrated runtime bridge.
- `CFV/MU`: the `mediation_verified` flag is caller-attested; it is **not** measured Cross-Frame Verifiability. The certificate and next-step recomputation are **not** measured Mutual Updateability.
- `Future Updateability`: a robust empirical test requires unseen external changes, budgeted adaptation, comparative baselines and retention of genuine participant choice.

## Reproduction

From this folder, using Python 3.10+ with no third-party dependencies:

```bash
python -m unittest -v test_connection_mechanism_v09.py
python connection_mechanism_v09.py > results_v09.json
```

The repository root does not receive a separate README. Place this directory under `research/cross_scale_physical_baselines/`. Do not overwrite earlier physical baseline experiments.
