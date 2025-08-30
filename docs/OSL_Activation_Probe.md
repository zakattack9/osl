# OSL Activation Probe
_Minimal prerequisite activation, not assessment_

## What It Is: A 90-Second Memory Primer

The activation probe is an **optional** tool to wake up prior knowledge before reading. It is NOT a diagnostic quiz, pre-test, or assessment.

## Research Foundation

### Activation Effect (Not Testing Effect)
- **Purpose**: Prime relevant neural pathways
- **Mechanism**: Surface prerequisites to working memory
- **Duration**: ≤90 seconds total
- **Items**: Maximum 3 simple recalls
- **Timing**: ONLY before reading new material

### Why Minimal?
- You can't test what you haven't learned
- Complex questions before learning create confusion
- Simple activation enhances encoding
- More than 3 items becomes a test

## The Strict Limits

### Maximum 3 Items
```
Q1: What is [prerequisite concept]?
Q2: Define [foundational term].
Q3: Recall [previous chapter's key point].
```

### Only Simple Recall
✅ **Allowed:**
- Definitions
- Basic facts
- Previous chapter concepts
- Prerequisite knowledge

❌ **NOT Allowed:**
- Application questions
- Transfer questions  
- Scenarios
- Problem-solving
- Anything requiring reasoning

### Maximum 90 Seconds
- 30 seconds per question maximum
- No deep thinking required
- If you don't know, move on
- No scoring or grading

## When to Use (Optional)

### Good Candidates for Activation:
- Starting new chapter that builds on previous
- Returning after a break (>3 days)
- Technical material with prerequisites
- Connected topics in sequence

### When to Skip:
- Starting brand new topic
- No clear prerequisites
- Daily continuous reading
- Literature or narrative content

## Implementation

### CLI Command
```bash
osl probe --chapter 5
```

### Format
```json
{
  "type": "activation_probe",
  "duration_limit": 90,
  "items": [
    {
      "id": 1,
      "type": "simple_recall",
      "question": "What is deep work?",
      "target": "definition",
      "prerequisite_for": "Chapter 5: Advanced Techniques"
    },
    {
      "id": 2,
      "type": "simple_recall", 
      "question": "Name the four disciplines",
      "target": "list",
      "prerequisite_for": "Chapter 5: Implementation"
    },
    {
      "id": 3,
      "type": "simple_recall",
      "question": "What was the key point about attention residue?",
      "target": "concept",
      "prerequisite_for": "Chapter 5: Optimization"
    }
  ]
}
```

### User Experience
```
System: Quick activation probe (90 seconds max, optional)
        Skip with 'pass' or press Enter

Q1: What is deep work?
You: [30 seconds to answer or 'pass']

Q2: Name the four disciplines
You: [30 seconds to answer or 'pass']

Q3: What was the key point about attention residue?
You: [30 seconds to answer or 'pass']

System: Activation complete. Beginning Chapter 5.
        [No scoring, no feedback, just activation]
```

## What It's NOT

### NOT a Pre-Diagnostic Quiz
The V3 Decision History explicitly rejected full pre-diagnostic quizzes:
- Can't test application before learning
- Can't test transfer before foundation
- Creates false baseline

### NOT a Calibration Tool
- No confidence ratings
- No scoring
- No comparison to actual performance
- No metrics tracked

### NOT a Gate
- Always optional
- Can skip entirely
- No impact on session
- No governance implications

## Difference from Weekly Calibration

| Aspect | Activation Probe | Weekly Calibration |
|--------|-----------------|-------------------|
| Purpose | Prime memory | Test knowledge |
| Timing | Before reading | After week of learning |
| Items | 3 simple recalls | 6-10 mixed items |
| Duration | ≤90 seconds | 20-30 minutes |
| Types | Recall only | Recall + Application + Transfer |
| Scoring | None | Full rubric |
| Confidence | Not collected | Required |
| Feedback | None | Detailed |
| Required | Optional | Part of workflow |

## Common Misconceptions

### ❌ "Should test to establish baseline"
**Why wrong:** You need knowledge before you can test it. Baseline comes from first retrieval attempts AFTER reading.

### ❌ "Should be comprehensive preview"
**Why wrong:** Comprehensive preview is already part of OSL (Preview & Questioning phase). This is just memory activation.

### ❌ "AI should generate based on chapter content"
**Why wrong:** Probe targets prerequisites, not new content. Based on what you've already learned.

## Decision Tree

```
Starting new reading?
├─ First time with material?
│   └─ SKIP probe (no prerequisites)
├─ Building on previous chapter?
│   └─ OPTIONAL probe (3 items max)
├─ Returning after break?
│   └─ OPTIONAL probe (refresh memory)
└─ Continuous daily reading?
    └─ SKIP probe (memory active)
```

## Examples

### Good Activation Probe
```
Chapter: Deep Work Scheduling (Ch 5)
Prerequisites: Chapters 1-4 concepts

Q1: What is deep work? [definition from Ch 1]
Q2: Name one of the four disciplines [list from Ch 3]
Q3: What's attention residue? [concept from Ch 4]

Duration: 90 seconds total
Purpose: Activate prior knowledge
```

### Bad "Diagnostic Quiz" (Rejected)
```
❌ Q1: How would you implement deep work in a busy office?
   [Application - can't answer before learning how]

❌ Q2: Compare deep work to GTD methodology
   [Transfer - requires synthesis not yet done]

❌ Q3: Rate your confidence in deep work principles
   [Calibration - premature without knowledge]

❌ Duration: 10 minutes
❌ Purpose: Baseline assessment
```

## Implementation Notes

1. **Make it skippable**: Single key to bypass entirely
2. **No storage needed**: Don't track responses
3. **Time enforce**: Auto-advance after 30 seconds
4. **Keep it light**: This is a primer, not a test
5. **Clear labeling**: Never call it a quiz or diagnostic

## The Rule

**If in doubt, skip it.** The probe is a minor optimization. The real learning happens in the micro-loops with retrieval practice AFTER reading.

## Code Specification

```python
def activation_probe(chapter):
    """Optional 90-second prerequisite activation"""
    
    if not has_prerequisites(chapter):
        return None
        
    if user_declines():
        return None
    
    probe = {
        'items': get_simple_recalls(max=3),
        'time_limit': 90,
        'type': 'activation_only'
    }
    
    for item in probe['items']:
        response = get_user_response(timeout=30)
        # No scoring, no storage, just activation
        
    return "Activation complete"
    # No metrics, no feedback, move to reading
```

Remember: This is memory activation, not knowledge assessment. Keep it minimal, optional, and focused on prerequisites only.