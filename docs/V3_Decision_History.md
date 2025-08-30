# OSL V3 — Decision History

_Archive of all modifications evaluated through the Six-Gate Framework, documenting what was accepted, rejected, or modified and why._

> **Purpose:** Prevent re-litigation of past decisions and maintain institutional knowledge about OSL's evolution.

---

## Decision Template

```
**[Feature Name] ([Accepted/Rejected/Modified] [Version])**
- Proposed: [What was suggested and why]
- Gates Analysis:
  - Gate 1: [PASS/FAIL] - [Reasoning]
  - Gate 2: [PASS/FAIL] - [Reasoning]
  - Gate 3: [PASS/FAIL] - [Reasoning]
  - Gate 4: [PASS/FAIL] - [Reasoning]
  - Gate 5: [PASS/FAIL] - [Reasoning]
  - Gate 6: [PASS/FAIL] - [Reasoning]
- Decision: [Final decision and where documented]
- Lesson: [What this teaches about OSL design]
```

---

## Archived Decisions

### Version 3.1

**Retrieval-Informed Highlighting (Rejected v3.1)**
- Proposed: Highlight only content missed during retrieval to create diagnostic markers
- Gates Analysis:
  - Gate 1: PASS - Aligns with retrieval practice
  - Gate 2: FAIL - Redundant with free recall gap identification
  - Gate 3: FAIL - Requires reopening text mid-loop, breaks momentum
  - Gate 4: FAIL - Time better spent on next micro-loop
  - Gate 5: FAIL - Adds marking, color-coding, and export complexity
  - Gate 6: WEAK - No evidence this improves outcomes over standard retrieval
- Decision: Removed entirely with rationale documented in L1
- Lesson: Features that "feel" helpful but duplicate existing mechanisms should be rejected

**Coach Memory Infrastructure (Accepted v3.1)**
- Proposed: Structured JSON state files for AI continuity between sessions
- Gates Analysis:
  - Gate 1: PASS - Supports spacing, calibration, and adaptive governance
  - Gate 2: PASS - Unique signal: cross-session state tracking
  - Gate 3: PASS - Operates at session boundaries, no loop interruption
  - Gate 4: PASS - Enables better coaching without time cost to learner
  - Gate 5: PASS - Complexity hidden from learner, automated via scripts
  - Gate 6: PASS - Clear mechanism: consistent enforcement of governance rules
- Decision: Added to L3 with automation scripts
- Lesson: Backend complexity is acceptable if it enhances existing features without learner burden

### Version 3.2

**Pre-Diagnostic Quiz Removal (Modified v3.2)**
- Proposed: Remove 6-10 item baseline quiz mixing recall/application/transfer before reading
- Gates Analysis:
  - Gate 1: WEAK PASS - Aligns with calibration but premature
  - Gate 2: FAIL - Redundant with weekly calibration quiz
  - Gate 3: PASS - Happens before micro-loop
  - Gate 4: FAIL - Cannot meaningfully test transfer before reading; poor ROI
  - Gate 5: FAIL - Adds complexity for minimal value
  - Gate 6: MIXED - Pretesting research supports simple recall, not complex application pre-reading
- Decision: Replaced with optional 3-item recall probe (≤90s) for prerequisite activation only
- Lesson: Pretesting works but must match learner's knowledge state; complex assessment requires foundation

**Concept Map Timing (Modified v3.2)**
- Proposed: Move concept map from pre-diagnostic to weekly synthesis
- Gates Analysis:
  - Gate 1: PASS - Supports self-explanation and transfer
  - Gate 2: PASS - Unique structural understanding signal
  - Gate 3: PASS - No loop interruption either way
  - Gate 4: FAIL at pre-reading - Insufficient knowledge to map meaningfully
  - Gate 5: PASS - Simple 5-minute activity
  - Gate 6: PASS - Research shows concept mapping from memory after learning is most effective
- Decision: Moved to weekly synthesis with ≤5 minute time box
- Lesson: Timing matters - generative activities need sufficient knowledge base

**Heading Conversion Requirement (Modified v3.2)**
- Proposed: Make "convert all headings to questions" optional
- Gates Analysis:
  - Gate 1: PASS - Supports curiosity-driven questioning
  - Gate 2: PARTIAL - Some unique value but overlaps with curiosity questions
  - Gate 3: PASS - Happens before micro-loop
  - Gate 4: WEAK - Time could be better spent on actual reading
  - Gate 5: FAIL - Bureaucratic overhead when combined with 5 curiosity questions
  - Gate 6: WEAK - No specific research supporting universal heading conversion
- Decision: Changed to "Optionally convert key headings → guiding questions as needed"
- Lesson: Mandatory procedural steps without clear learning benefit create friction

**Interleaving Schedule Flexibility (Modified v3.2)**
- Proposed: Change from fixed "2×/week" to proportion-based "30-50% of sessions"
- Gates Analysis:
  - Gate 1: PASS - Supports interleaving principle
  - Gate 2: PASS - Unique mixing signal
  - Gate 3: PASS - Separate sessions
  - Gate 4: FAIL for fixed schedule - Doesn't adapt to reading frequency
  - Gate 5: FAIL for fixed schedule - Rigid requirement adds planning overhead
  - Gate 6: PASS - Research supports interleaving, not specific frequency
- Decision: Changed to "30-50% of sessions" with tuning range 20-60%
- Lesson: Principles should adapt to individual learning patterns, not impose rigid schedules

**Transfer Project Timing (Modified v3.2)**
- Proposed: Change from monthly to per book/major topic
- Gates Analysis:
  - Gate 1: PASS - Directly supports transfer principle
  - Gate 2: PASS - Unique application signal
  - Gate 3: PASS - Doesn't interrupt flow
  - Gate 4: WEAK for monthly - Arbitrary calendar vs natural learning boundaries
  - Gate 5: FAIL for monthly - Forces projects even when not ready
  - Gate 6: PASS - Transfer research supports application, not specific timing
- Decision: Changed to "per book/major topic" milestone-based
- Lesson: Align assessments with natural learning units, not arbitrary time periods

**Smart Notes Quantity Requirement (Modified v3.2)**
- Proposed: Remove "2-5 permanent notes" requirement
- Gates Analysis:
  - Gate 1: PASS - Supports self-explanation
  - Gate 2: PASS - Unique synthesis signal
  - Gate 3: PASS - End of session activity
  - Gate 4: PASS - High ROI for consolidation
  - Gate 5: FAIL for specific count - Artificial constraint on natural insight flow
  - Gate 6: WEAK for count - No research supporting specific note quantities
- Decision: Changed to "permanent notes for key insights" (quality over quantity)
- Lesson: Organic insight generation beats forced quotas

---

## Key Patterns from Decisions

### Common Rejection Reasons
1. **Redundancy** - Feature duplicates existing mechanism without unique value
2. **Momentum Breaking** - Requires reopening materials or context switching mid-flow
3. **Arbitrary Constraints** - Specific numbers/timing without research basis
4. **Premature Complexity** - Advanced techniques before foundation is built

### Common Acceptance Criteria
1. **Unique Learning Signal** - Provides information not captured elsewhere
2. **Natural Boundaries** - Aligns with learning milestones, not calendar
3. **Hidden Complexity** - Backend sophistication that doesn't burden learner
4. **Research-Backed** - Clear evidence or mechanistic reasoning

### Design Philosophy Emerging
- **Quality over quantity** in all generative activities
- **Flexibility over rigidity** in scheduling and requirements
- **Natural over artificial** boundaries and milestones
- **Evidence over intuition** for all design decisions

---

## Version 3.3 - AI Role Clarifications (Research-Grounded)

**AI-Generated Retrieval Questions (Accepted with Guardrails v3.3)**
- Proposed: AI generates 2-3 questions after learner's free recall to enhance testing effect
- Gates Analysis:
  - Gate 1: PASS - Directly supports retrieval practice principle
  - Gate 2: PASS - Adds corrective feedback signal not present in solo recall
  - Gate 3: PASS - Happens AFTER learner's retrieval, preserves effortful recall
  - Gate 4: PASS - High ROI: Testing effect + immediate feedback documented benefits
  - Gate 5: PASS - Simple addition to existing micro-loop
  - Gate 6: STRONG PASS - Roediger & Karpicke (2006): Testing effect; Hattie & Timperley (2007): Feedback impact
- Decision: ACCEPTED - AI generates questions AFTER learner completes free recall and Feynman explanation
- Guardrails: 
  - Questions target the material, not learner's recall quality
  - Tiered progression: recall → application → transfer
  - Must include corrective feedback with citations
- Lesson: AI enhancement is acceptable when it amplifies proven learning mechanisms without replacing learner effort

**AI-Generated Flashcards (Rejected for Auto-Generation v3.3)**
- Proposed: AI automatically creates flashcards from identified gaps
- Gates Analysis:
  - Gate 1: PARTIAL - Supports spacing but violates self-explanation
  - Gate 2: FAIL - Generation effect requires learner authorship
  - Gate 3: PASS - Happens at session boundaries
  - Gate 4: FAIL - Bypasses generation effect (Slamecka & Graf, 1978)
  - Gate 5: FAIL - Removes critical metacognitive decision: "What's worth remembering?"
  - Gate 6: STRONG FAIL - Generation effect research shows self-created > provided materials
- Decision: REJECTED for auto-generation; ACCEPTED for AI assistance only
- AI Limited To:
  - Formatting help (cloze syntax)
  - Citation verification
  - Flagging ambiguity
  - Suggesting refinements (learner must approve)
- Lesson: The act of deciding what becomes a flashcard IS the learning activity

**AI-Generated Weekly Quizzes (Accepted v3.3)**
- Proposed: AI generates 6-10 item weekly calibration quiz
- Gates Analysis:
  - Gate 1: PASS - Directly supports calibration principle
  - Gate 2: PASS - Provides external assessment for accuracy calibration
  - Gate 3: PASS - Weekly boundary, no loop interruption
  - Gate 4: PASS - Low-stakes quizzing improves retention (testing effect)
  - Gate 5: PASS - Reduces burden of quiz creation
  - Gate 6: STRONG PASS - Testing effect literature; AIG (Automatic Item Generation) research
- Decision: ACCEPTED for weekly calibration (6-10 items: 3 recall, 3-4 application, 2-3 transfer)
- Constraints:
  - Blueprint-based generation (not "gap"-based)
  - Rubric scoring with feedback
  - Items saved for reuse/refinement
- Lesson: AI quiz generation acceptable when serving calibration, not diagnostic purposes

**Pre-Reading Diagnostic (Modified to Minimal Probe v3.3)**
- Proposed: Keep full pre-diagnostic quiz with AI generation
- Gates Analysis:
  - Gate 1: WEAK - Activation helps but full quiz premature
  - Gate 2: FAIL - Weekly calibration provides this signal
  - Gate 3: PASS - Before reading
  - Gate 4: FAIL - Cannot test application/transfer before learning
  - Gate 5: FAIL - Overhead for minimal benefit
  - Gate 6: MIXED - Pretesting benefits exist but only for simple recall
- Decision: MODIFIED to optional ≤90s, 3-item recall probe for prerequisites only
- Lesson: Pretesting activation good; premature assessment counterproductive

---

## Research Citations Supporting v3.3 Decisions

1. **Testing Effect**: Roediger, H. L., & Karpicke, J. D. (2006). Test-enhanced learning: Taking memory tests improves long-term retention. *Psychological Science*, 17(3), 249-255.

2. **Feedback Impact**: Hattie, J., & Timperley, H. (2007). The power of feedback. *Review of Educational Research*, 77(1), 81-112.

3. **Generation Effect**: Slamecka, N. J., & Graf, P. (1978). The generation effect: Delineation of a phenomenon. *Journal of Experimental Psychology: Human Learning and Memory*, 4(6), 592-604.

4. **Effective Learning Techniques**: Dunlosky, J., Rawson, K. A., Marsh, E. J., Nathan, M. J., & Willingham, D. T. (2013). Improving students' learning with effective learning techniques. *Psychological Science in the Public Interest*, 14(1), 4-58.

5. **Automatic Item Generation**: Gierl, M. J., & Haladyna, T. M. (Eds.). (2012). *Automatic item generation: Theory and practice*. Routledge.

---

## Summary of Current AI Role Boundaries

| Activity | AI Role | Learner Role | Evidence |
|----------|---------|--------------|----------|
| **Retrieval Questions** | ✅ Generate after learner's recall | Complete free recall first | Testing effect research |
| **Flashcards** | ⚠️ Assist with format/citations only | Author all cards | Generation effect |
| **Weekly Quiz** | ✅ Generate and score | Take quiz, review feedback | Testing + calibration |
| **Pre-reading** | ✅ Optional 3-item probe only | Decide if needed | Activation research |
| **Permanent Notes** | ❌ No generation | Write all notes | Self-explanation |
| **Curiosity Questions** | ❌ No generation | Generate all questions | Curiosity principle |
| **Synthesis Essays** | ❌ No generation | Write all essays | Transfer principle |