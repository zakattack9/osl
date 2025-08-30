# Optimized System for Learning (OSL V3)

_A research-backed, AI-assisted reading and learning process for comprehension, retention, and transfer._

---

## 1. Core Principles

- **Retrieval practice**: Actively recall, don't just reread.
- **Spacing**: Review at increasing intervals (1d → 3d → 7d → 14d → monthly).
- **Interleaving**: Mix related topics to strengthen discrimination and transfer.
- **Self-explanation**: Rephrase in your own words (Feynman style).
- **Feedback**: Immediate correction strengthens memory and reduces drift.
- **Calibration**: Predict performance, test, and compare prediction vs. outcome.
- **Transfer**: Apply ideas through synthesis writing and projects.
- **Curiosity-driven questioning**: Use learner-generated guiding questions as anchors for reading and recall.

---

## 2. Workflow Overview

1. **Setup** (tools + AI roles)
2. **Intent & Pre-Diagnostic** (goals + baseline)
3. **Preview & Questioning** (curiosity + guiding questions)
4. **Micro-Loop Reading Cycle** (Q → Read → Retrieve → Explain → Feedback)
5. **Smart Notes** (permanent notes + diagrams)
6. **High-Yield Flashcards** (≤8/session)
7. **Spaced & Interleaved Practice** (scheduled reviews + mixed tasks)
8. **Weekly Calibration & Synthesis** (test + essay)
9. **Transfer Projects** (applied artifact per book/major topic)
10. **Adaptive Governance Rules** (caps + gates to prevent overload, with flexibility)
11. **Transfer Projects** (per book/major topic)
12. **Optional Skill Lanes** (mentors for writing, rhetoric, memory, style)

---

## 3. Setup

### Tools
- Notes: **Obsidian** (must capture citations).
- Flashcards: Anki (or similar, with spaced repetition).
- Diagrams: Excalidraw, Whimsical.

### AI Roles
- **Extractor**: Provides _cited bullet points and outlines only_ (no free summaries without references).
- **Tutor**: Runs Socratic Q&A AFTER learner's free recall, provides feedback, and validates session completeness. Generates 2-3 questions per micro-loop targeting the material, not recall quality (see OSL_AI_Boundaries.md for timing restrictions).
- **Coach**: Maintains spaced review schedule, interleaving plan, and ensures governance rules are adaptive. Uses structured session state files (`coach_state.json`) for continuity between sessions (see OSL_State_Schema.md for authoritative schema).

---

## 4. Intent & Pre-Diagnostic (5–10 min)

- Write **3 outcomes** (e.g., "Explain X to a novice and an expert," "Solve Y problem type," "Apply Z to project A").
- Identify what you **already know** and list initial **misconceptions** or unknown terms.
- *(Optional, ≤90s)* Run a **3-item recall probe** on prerequisite ideas (no transfer items). This is NOT a full quiz - see OSL_Activation_Probe.md for the minimal probe specification.

---

## 5. Preview & Questioning (10–15 min)

- Skim table of contents, headings, diagrams.
- Write **5 curiosity questions** in your own words.
- **Optionally convert key headings → guiding questions as needed.**
- (Optional) Ask **Extractor** to build a cited outline for structural clarity.

---

## 6. Micro-Loop Reading Cycle (repeat based on material type)

**Chunk sizes by material:**
- Technical books: 5–10 pages (standard)
- Dense/complex material: 3–5 pages
- Literature: 1 scene or chapter
- Lists/reference: Natural sections

1. **Question**: Select 1–3 guiding questions.
2. **Read**: Focused chunk, minimal highlights (claims, data, examples).
3. **Retrieve**: Free recall for 1–2 minutes on a blank page.
4. **Explain**: Write or speak a Feynman explanation (3-5 sentences: define, example, contrast, limitation).
5. **Feedback**: Tutor generates 2–3 questions; learner answers; Tutor gives corrective feedback.

---

## 7. Smart Notes (end of Each Session, 8–12 min)

- Write **permanent notes for key insights**: claim, context, example, citation, links.
- Create **1 diagram or dual-coded visual** if structure matters.

---

## 8. High-Yield Flashcards (≤8 per session)

- Use cloze deletions, discriminations, and application prompts.
- Prioritize **application cards** over definitions.
- Every card must include a **citation/source**.
- Add new cards only if review load allows.
- **Critical**: Learner must author all cards to preserve generation effect (see OSL_Flashcard_Philosophy.md).

---

## 9. Spaced & Interleaved Practice

- **Spacing Schedule**: 1d → 3d → 7d → 14d → monthly.
- **Daily reviews**: 10–15 min Anki.
- **Interleaving**: Mix current, prior, and adjacent domains in 30-50% of sessions (see OSL_Interleaving_Specification.md for detection algorithm).

---

## 10. Weekly Calibration & Synthesis (60–90 min)

- **Prediction → Test → Feedback** cycle.
- Update misconception list; schedule targeted reviews.
- Write a **1-page synthesis essay** weaving 2–3 concepts into perspective.
- **Create/update a 1-page concept map of the week's learning** (≤5 minutes, see OSL_Concept_Map_Implementation.md).

---

## 11. Transfer Projects (per book/major topic, 2–3 hrs)

- Apply knowledge to build or create an artifact (tutorial, critique, worked examples, thematic analysis).
- Publish artifact to notes hub for reference.
- Complete one per book or major learning milestone.

---

## 12. Adaptive Governance Rules

- **Calibration Gate:** If weekly retrieval < 80% (tunable 75-85%), pause new content until remediation (review, re-explain, re-test).
- **Card Debt Cap:** If due cards > 2× normal daily throughput (tunable 1.5×-2.5×), halt new card creation until reviews stabilize.
- **Flexibility:** Learners can adjust thresholds with Coach guidance to avoid rigidity.
- **Transfer Proof:** One artifact per book/major topic required.
- See OSL_Governance_Standards.md for authoritative thresholds and tuning ranges.

---

## 13. Optional Skill Lanes

- **Writing & Rhetoric** (weekly practice).
- **Memory Palace** (for ordered material).
- **Style/Communication Coaching** (optional).
- Add-ons for specific goals, not core.

---

## 14. Genre Adjustments (Appendices, not core)

- **STEM/Technical**: Error catalog, derivations, interleave problems.
- **History/Social Science**: Claims → evidence → uncertainty mapping.
- **Literature**: Track motives ("Who wants what? What changed?").
- **Lists/Names**: Method of loci for memorization.

---

## 15. Session Templates (Guidelines, not rigid)

**Daily (~45 min)**: plan → micro-loops → flashcards (10–15m) → notes wrap-up.

**Weekly (~90 min)**: prediction → test → synthesis.

**Per book/major topic (2–3 hrs)**: project build and publish.

---

## 16. Metrics to Track

- Retrieval % correct
- Prediction vs. actual (calibration)
- Misconceptions resolved
- Flashcard load
- Time to first applied artifact

---

## 17. Summary

V3 refines OSL by keeping its **retrieval-focused micro-loop** at the center, while simplifying governance, reinforcing guiding questions, and treating genre-specific or skill-lane adjustments as optional. The system balances **structure with adaptability**, making it sustainable and effective for long-term learning.

**Note on System Evolution:** All proposed modifications to OSL must pass the Six-Gate Framework (see Implementation Guide Section M) to prevent feature creep and maintain focus on evidence-based, high-ROI learning activities. This ensures OSL remains lean, effective, and true to its core principles.

**Authoritative Specifications:** Critical aspects of OSL implementation are documented in dedicated specification files:
- OSL_AI_Boundaries.md - When and how AI can interact
- OSL_Governance_Standards.md - Authoritative thresholds and ranges
- OSL_Flashcard_Philosophy.md - Generation effect protection
- OSL_State_Schema.md - Authoritative data structures
- OSL_Natural_Language_Balance.md - User control preservation
See OSL_Master_Reference_Guide.md for complete document map.
