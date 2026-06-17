# PCOS: Personal Cognitive Operating System
# Design Specification v1.0
# Date: 2026-06-17

---

## 1. Vision

Build a long-term cognitive system that thinks like the user — understanding identity, values, decision patterns, and world model — to discover opportunities, form strategies, and evolve through experience.

**Core Principles:**
- Identity First → World Model → Strategy → Decision → Planning → Execution → Reflection → Learning
- Everything is a Belief (not a Fact)
- Mixed Thinking: Fast (intuitive) + Slow (analytical) with meta-cognitive switching
- Evolution is first-class: Identity and World Model change over time

---

## 2. Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Meta-Cognition                           │
│            (Fast/Slow switching · Confidence assessment)     │
├─────────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────────┐  │
│  │                Identity Core                          │  │
│  │   (Values · Preferences · Decision Patterns)          │  │
│  └────────────────────────┬──────────────────────────────┘  │
│                           ▼                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                World Model                            │  │
│  │   (Beliefs · Entities · Relations · Confidence)        │  │
│  └────────────────────────┬──────────────────────────────┘  │
│                           ▼                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Decision Engine (BDI)                     │  │
│  │   Beliefs ← World Model                               │  │
│  │   Desires ← Identity Core                             │  │
│  │   Intentions ← Strategy Engine                        │  │
│  └────────────────────────┬──────────────────────────────┘  │
│                           ▼                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │        Strategy → Plan → Execute → Reflect            │  │
│  └────────────────────────┬──────────────────────────────┘  │
│                           ▼                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Evolution Cycle                           │  │
│  │   Experience → Pattern Recognition → Belief Update    │  │
│  │   → Identity Evolution                                │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**Selected Approach:** BDI + Evolution Cycle (Option C)
- Natural handling of circular dependencies (identity evolves through experience)
- Mixed decision style via Meta-Cognition layer
- Cognitive science grounding (Belief-Desire-Intention model)

---

## 3. Identity Core

### Design Philosophy
Identity is not a static profile. It's a living belief graph with multiple layers, conflicts, and evolution.

### Layer Structure (MVP)

| Layer | Content | Update Frequency |
|-------|---------|------------------|
| Core Values | Declared values, no weights | Rare (evolution events) |
| Current Focus | Primary/secondary domains | Monthly |
| Known Preferences | Direction + system-inferred confidence | Weekly |
| Decision Log | Raw decision records | Every decision |

### Key Design Decisions
1. **No weights on values in MVP** — Binary "core" vs "non-core" is more honest than false-precision weights
2. **Preference confidence is system-inferred** — Not user-declared. Derived from behavioral consistency.
3. **Decision Log is the most important data structure** — Raw material for World Model, Strategy, Learning, Evolution

### Version Roadmap
- **MVP:** Core values, focus, preferences, decision log
- **V2:** Value weights (inferred), discovered decision patterns, drift tracking
- **V3:** Cognitive bias detection, role priority, evolution trends, external feedback

### Schema: `pcos/identity.yaml`

---

## 4. World Model

### Design Philosophy
Everything is a Belief, not a Fact. We are often wrong, the world changes, our understanding is incomplete. The system must model uncertainty explicitly.

### Entity Types (Focused: Business + Startup + Technology)

| Entity | Purpose |
|--------|---------|
| Market | Market/segment with size, growth, dynamics |
| Competitor | Company/product competing in same space |
| Opportunity | Potential business opportunity |
| Technology | Technology trend or capability |
| Resource | Available resource (money, time, skill, network) |
| CustomerSegment | Customer group with needs and behaviors |

### Relation Types
- Competition: `competes_with`, `serves_same_market`
- Opportunity: `enables`, `requires`, `targets`
- Risk: `threatens`, `depends_on`
- Learning: `similar_to`, `learned_from`

### Confidence System

| Source | Base Confidence |
|--------|----------------|
| User direct observation | 0.85 |
| User experience | 0.75 |
| External data | 0.70 |
| User assumption | 0.50 |
| System inference | 0.40 |
| Analogy | 0.35 |

**Time Decay:** Half-life = 90 days. Confidence decays without re-validation.

### Version Roadmap
- **MVP:** 6 entity types, 9 relation types, basic confidence + decay
- **V2:** Case studies, trend signals, causal inference, scenario analysis
- **V3:** Autonomous opportunity discovery, cognitive mapping, counterfactual reasoning, cross-domain insights

### Schema: `pcos/world_model.yaml`

---

## 5. Strategy Engine

### Design Philosophy
Strategy ≠ Plan. Strategy answers "Where to play, how to win". Plan answers "How to execute".

### Strategy Formation Process
1. Frame strategic question
2. Generate strategic options (from Decision Engine)
3. Evaluate each option against criteria
4. Recommend direction with reasoning
5. User confirms

### Output Structure
- **Direction:** One-sentence strategic direction
- **Success Criteria:** 2-7 metrics with leading indicators
- **Resource Allocation:** Percentage-based, must sum to 100%
- **Timeline:** Phased with exit criteria
- **Stop Loss:** Conditions to abandon, always requires user confirmation
- **Milestones:** Checkpoints with success metrics

### Revision Triggers
- Stop loss condition met
- Milestone missed by >50% of timeframe
- World Model belief with high impact updated
- New opportunity with higher alignment score

### Schema: `pcos/strategy_engine.yaml`

---

## 6. Decision Engine

### BDI Integration

| Component | Source | Updates When |
|-----------|--------|--------------|
| Beliefs | World Model | New info, contradiction, decay |
| Desires | Identity Core | Identity evolution, value change |
| Intentions | Strategy Engine | Strategy formation, revision |

### Thinking Modes

**Fast Thinking:**
- Triggers: complexity=low, risk=low, coverage>0.7, has_pattern=true
- Process: pattern_match → analogy → generate (1-2 options) → quick_check → recommend
- Max 2 options, no reasoning chain required

**Slow Thinking:**
- Triggers: complexity=high/novel, risk=high, coverage<0.5, has_contradictions
- Process: frame → generate (3+ options) → evaluate → scenario → assumptions → blind_spots → recommend
- Min 3 options, reasoning chain + scenario analysis required

**Switching Formula:**
```
slow_score = complexity×0.30 + risk×0.25 + (1-coverage)×0.20 + (1-pattern)×0.15 + (1-reversibility)×0.10

< 0.3  → FAST
0.3-0.6 → FAST with escalation monitor
> 0.6  → SLOW
```

### Option Evaluation Criteria

| Criterion | Weight | Source |
|-----------|--------|--------|
| Value Alignment | 0.30 | Identity Core |
| Belief Support | 0.25 | World Model confidence |
| Resource Feasibility | 0.20 | Resources + constraints |
| Risk Acceptability | 0.15 | Risk assessment + risk tolerance |
| Learning Potential | 0.10 | Blind spots addressed |

### Error Recovery

| Severity | Trigger | Action | Return State |
|----------|---------|--------|--------------|
| Minor | Task retryable | retry/skip | EXECUTE |
| Major | Plan affected | analyze | PLANNING |
| Critical | Assumption invalidated | analyze | STRATEGY |
| Catastrophic | Goal invalid | analyze | ASSESSMENT |

### Schema: `pcos/decision_engine.yaml`

---

## 7. System State Machine

### Main Flow
```
IDLE → INTAKE → CONTEXT LOAD → ASSESSMENT → [FAST|SLOW] THINKING
→ STRATEGY → PLANNING → EXECUTE → REFLECT → LEARN → [EVOLVE] → IDLE
```

### Recovery Paths
- REJECT → CLARIFICATION (max 3 rounds) → INTAKE / DECOMPOSE / ABANDON
- EXECUTE failure → PLANNING / STRATEGY / ASSESSMENT (by severity)

### Update Triggers

| Update Type | Triggers |
|-------------|----------|
| Identity Update | Major surprise, 3+ new patterns, user declaration, external contradiction |
| World Model Update | Outcome contradicts prediction, assumption invalidated, new info, decay |
| Learning Update | Every reflection, pattern repetition, prediction accuracy/failure |

### System Lifecycle

| Phase | Duration | Characteristics |
|-------|----------|-----------------|
| BIRTH | Day 1 | Identity interview, empty World Model |
| INFANCY | Weeks 1-4 | High-frequency learning, frequent clarification |
| GROWTH | Months 1-3 | First patterns discovered, proactive insights begin |
| MATURITY | Months 3-12 | Reliable predictions, bias detection, first identity evolution |
| EVOLUTION | Month 12+ | Cross-domain insights, counterfactual reasoning |

---

## 8. Event Flow

Detailed trace: `pcos/event_flow_trace.md`

### Summary: User Goal → System Response

1. **INTAKE:** Classify intent, extract entities, assess ambiguity
2. **CLARIFICATION:** (if needed) Ask clarifying questions, max 3 rounds
3. **CONTEXT LOAD:** Load Identity + World Model + History
4. **ASSESSMENT:** Evaluate complexity, risk, coverage, alignment → choose Fast/Slow
5. **THINKING:** Generate options, evaluate, recommend
6. **STRATEGY:** Form direction, success criteria, resource allocation, stop loss
7. **PLANNING:** Break into tasks with dependencies
8. **EXECUTE:** Run tasks, track progress, handle blockers
9. **REFLECT:** Compare outcome vs expectations, identify surprises
10. **LEARN:** Update beliefs, extract patterns, check identity signals
11. **EVOLVE:** (if significant) Update Identity and World Model
12. **IDLE:** Return to waiting state

---

## 9. File Structure

```
pcos/
├── identity.yaml              # Identity Core schema (MVP)
├── world_model.yaml           # World Model schema (MVP)
├── strategy_engine.yaml       # Strategy Engine schema
├── decision_engine.yaml       # Decision Engine schema
└── event_flow_trace.md        # Complete event flow example

docs/superpowers/specs/
└── 2026-06-17-pcos-design.md  # This document
```

---

## 10. Open Questions

1. **External Data Integration:** How to ingest market data, news, signals? (V2)
2. **Multi-modal Input:** Beyond text — voice, images, documents?
3. **Privacy:** How to protect sensitive identity and decision data?
4. **Scaling:** Can this work for teams, not just individuals?
5. **Evaluation:** How to measure if the system is actually getting better?

---

## 11. Success Criteria (MVP)

- [ ] User can initialize Identity Core through structured interview
- [ ] System can classify goals and route to Fast/Slow thinking
- [ ] System can generate and evaluate strategic options
- [ ] System can form strategy with success criteria and stop loss
- [ ] System can track execution and reflect on outcomes
- [ ] System can update World Model beliefs from experience
- [ ] System can detect and surface contradictions
- [ ] Complete event flow works end-to-end for one goal lifecycle
