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