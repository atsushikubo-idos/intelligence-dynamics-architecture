# CASE_POOL_FREEZE_v0.1

## Status

Frozen Candidate Pool for the `What IDOS Makes Visible` five-case pilot.

Freeze date: **2026-10-03**

This document freezes the candidate pools and the mechanical selection procedure before substantive IDOS analysis of the selected cases.

---

## 1. Purpose

The purpose of this freeze is to reduce confirmation-driven case selection.

The five-case pilot is structured across the following regime gradient:

$$
Present\ Normal
\rightarrow Present\ Edge
\rightarrow Transition
\rightarrow Agentic/Multi\text{-}Agent
\rightarrow Future\ Regime\ Proxy
$$

The regime structure is theory-defined, but the specific case within each regime is selected mechanically from a frozen candidate pool.

$$
Theory\ defines\ the\ regime
$$

$$
Sampling\ selects\ the\ case
$$

---

## 2. Selection Rule

Each regime contains exactly five candidates, numbered 1–5.

For regime `V00X`, the seed is:

```text
WHAT_IDOS_MAKES_VISIBLE_v0.1|V00X|2026-10-03
```

The SHA-256 digest is interpreted as a hexadecimal integer.

The raw zero-based index is:

$$
i = SHA256(seed)\bmod 5
$$

The selected one-based candidate number is:

$$
Candidate = i + 1
$$

No selected case may be replaced merely because IDOS performs weakly, conventional analysis performs strongly, or the case produces an inconvenient result.

---

## 3. Computational Correction Before Freeze

A preliminary conversational selection was stated before the arithmetic was independently recomputed. That preliminary selection contained indexing inconsistencies and is **not** treated as frozen.

This document is the authoritative freeze. It explicitly distinguishes the zero-based modulo result from the one-based candidate number and records the reproducible SHA-256 calculation.

---

## 4. Frozen Candidate Pools and Mechanical Selection

### V001 — Present Normal

1. Experimental Evidence on the Productivity Effects of Generative Artificial Intelligence
2. Generative AI at Work
3. GitHub Copilot — Impact of AI on Developer Productivity
4. Navigating the Jagged Technological Frontier — BCG / GPT-4
5. Microsoft Security Copilot — randomized / controlled productivity study **← SELECTED**

Selection record:

```text
seed: WHAT_IDOS_MAKES_VISIBLE_v0.1|V001|2026-10-03
SHA-256: 0794ece354eff8ca618854083f6db33cfbd35ad567bc55b2d946ad9e431f87c5
raw index (mod 5): 4
selected candidate number: 5
```

Frozen selection: **Microsoft Security Copilot — randomized / controlled productivity study**

---

### V002 — Present Edge

1. Algorithmic Management in Logistics
2. Amazon Fulfillment Robotics / DeepFleet **← SELECTED**
3. Tesla Full Self-Driving (Supervised)
4. Uber Marketplace Matching / Reinforcement Learning
5. Waymo Autonomous Driving / Fleet Response

Selection record:

```text
seed: WHAT_IDOS_MAKES_VISIBLE_v0.1|V002|2026-10-03
SHA-256: 654824c0cbfd920dc2417ab172fee9687ed33b772ec40a7bc7b0305424326580
raw index (mod 5): 1
selected candidate number: 2
```

Frozen selection: **Amazon Fulfillment Robotics / DeepFleet**

---

### V003 — Transition

1. Amazon Proteus — Human-to-Robot Natural-Language Delegation **← SELECTED**
2. ChatGPT Agent / Operator — From Advice to Execution
3. Healthcare Algorithmic Management
4. Tesla Full Self-Driving (Supervised) — Driver-to-Supervisor Transition
5. Waymo Fleet Response — Driver-to-Remote Context Provider

Selection record:

```text
seed: WHAT_IDOS_MAKES_VISIBLE_v0.1|V003|2026-10-03
SHA-256: 3c7e0a8ea8058bb18f5bfc9166b160c7b25eeaea2db220b6ae426436f221ebe8
raw index (mod 5): 0
selected candidate number: 1
```

Frozen selection: **Amazon Proteus — Human-to-Robot Natural-Language Delegation**

---

### V004 — Agentic / Multi-Agent

1. Anthropic Multi-Agent Research System **← SELECTED**
2. Microsoft AutoGen Multi-Agent Conversation
3. OpenAI Multi-Agent Orchestration
4. U.S. 2010 Flash Crash / Algorithmic Trading Interaction
5. Amazon DeepFleet Robot-Fleet Coordination

Selection record:

```text
seed: WHAT_IDOS_MAKES_VISIBLE_v0.1|V004|2026-10-03
SHA-256: 357df7e761e3db9b291d00d5a7e4b999c8e48f50082f4f462d041ef068fed393
raw index (mod 5): 0
selected candidate number: 1
```

Frozen selection: **Anthropic Multi-Agent Research System**

---

### V005 — Future Regime Proxy

1. Google DeepMind AI Co-Scientist
2. Sakana AI Scientist-v2
3. Generative Agents — Smallville
4. Project Sid — Many-Agent AI Society **← SELECTED**
5. Stanford Virtual Lab

Selection record:

```text
seed: WHAT_IDOS_MAKES_VISIBLE_v0.1|V005|2026-10-03
SHA-256: 4fb0d03be5213a8bb404287a4a1db41536bb6fac810f7724cb10808f7d7226f2
raw index (mod 5): 3
selected candidate number: 4
```

Frozen selection: **Project Sid — Many-Agent AI Society**

---

## 5. Frozen Five-Case Pilot

- **V001 — Present Normal:** Microsoft Security Copilot — randomized / controlled productivity study
- **V002 — Present Edge:** Amazon Fulfillment Robotics / DeepFleet
- **V003 — Transition:** Amazon Proteus — Human-to-Robot Natural-Language Delegation
- **V004 — Agentic / Multi-Agent:** Anthropic Multi-Agent Research System
- **V005 — Future Regime Proxy:** Project Sid — Many-Agent AI Society

The resulting regime sequence is therefore:

$$
AI\ Support
\rightarrow AI\text{-}Embedded\ Infrastructure
\rightarrow Human/Robot\ Delegation\ Transition
\rightarrow Multi\text{-}Agent\ Coordination
\rightarrow Many\text{-}Agent\ Society\ Proxy
$$

---

## 6. Replacement Rule

A selected case may be replaced only for procedural reasons, including:

- materially insufficient public evidence;
- inaccessible primary or high-quality secondary sources;
- mistaken regime classification discovered before substantive IDOS analysis;
- material factual error in candidate identification;
- duplication that prevents the intended regime distinction.

Any replacement must be documented before analysis and must use a pre-specified replacement rule rather than discretionary substitution.

Weak IDOS performance is **not** a valid replacement reason.

---

## 7. Interpretation Constraint

This pilot is not a statistically representative sample of all Human–AI systems.

It is a structured exploratory regime test designed to examine:

$$
Under\ what\ structural\ conditions\ does\ IDOS\ add\ visibility?
$$

The analysis must therefore avoid claims about population prevalence or universal effect size.

---

## 8. Next Step

After this freeze, the five selected cases should be analyzed without changing the pool:

$$
Raw\ Reconstruction
\rightarrow Conventional\ Analysis
\rightarrow IDOS\ Analysis
\rightarrow Incremental\ Visibility
\rightarrow Necessity\ Test
$$

The first analysis case is:

**V001 — Microsoft Security Copilot — randomized / controlled productivity study**
