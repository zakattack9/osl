# OSL Flashcard Philosophy
_Generation Effect: Why learner authorship is non-negotiable_

## Core Principle: You Create, You Remember

The act of deciding what becomes a flashcard and writing it yourself IS the learning activity. This is not a convenience issue - it's a fundamental learning mechanism.

## Research Foundation

### Generation Effect (Slamecka & Graf, 1978)
- Information you generate is remembered 50% better than information provided to you
- The cognitive effort of creation strengthens memory encoding
- Personal relevance amplifies retention

### Metacognition in Learning
- Deciding "what's worth remembering" exercises judgment
- Identifying your own knowledge gaps builds self-awareness
- Personal wording matches your mental models

## The Flashcard Pipeline

### Step 1: Learner Identifies Gap
**During micro-loop, you notice:**
```
"I couldn't recall the 4-hour limit for deep work"
"I mixed up deep work and flow state"
"I forgot the specific example about Darwin"
```

**This identification is learning** - you're building metacognitive awareness.

### Step 2: Learner Decides Importance
**You ask yourself:**
- Will I need this specific fact?
- Is this a key principle or just detail?
- Does this connect to other concepts?

**Only YOU can make this decision** based on your goals.

### Step 3: Learner Writes Content
**You create in your words:**
```
FRONT: "What's the biological limit for deep work per day?"
BACK: "4 hours (some can extend to 5 with training)"

Why YOUR wording matters:
- Matches your mental model
- Uses your vocabulary
- Connects to your examples
```

### Step 4: AI Assists ONLY with Format
**AI can help with:**
- Cloze syntax: `{{c1::4 hours}}`
- Citation format: `(Newport, 2016, p.47)`
- Ambiguity check: "Is '4' clear or should you specify '4 hours'?"
- Card count: "You've created 5/8 for this session"

**AI CANNOT:**
- Suggest what should become a card
- Write the question or answer
- Decide importance
- Generate cards from "gaps"

## Common Misconceptions

### ❌ "AI should create cards from my failed recalls"
**Why this breaks learning:**
- Removes decision-making (metacognition)
- Bypasses generation effect
- Creates cards you don't own mentally
- Fills deck with AI priorities, not yours

### ❌ "AI should write better questions than mine"
**Why your "worse" questions are better:**
- They match YOUR confusion points
- Use YOUR mental language
- Target YOUR specific gaps
- You'll recognize them during review

### ❌ "AI should optimize my cards"
**Why optimization can hurt:**
- "Perfect" cards may not match your thinking
- Standardization removes personal hooks
- Your "mistakes" often aid memory

## Implementation Guidelines

### What Learner Must Do
```python
# Learner's cognitive work (cannot be automated)
def create_flashcard(learner_brain):
    gap = learner_brain.identify_what_was_missed()
    importance = learner_brain.decide_if_worth_remembering()
    
    if importance > threshold:
        question = learner_brain.formulate_question()
        answer = learner_brain.write_answer()
        return Flashcard(question, answer, source)
    return None
```

### What AI Can Do
```python
# AI's assistance work (formatting only)
def assist_flashcard(learner_card):
    formatted = add_cloze_syntax(learner_card)
    citation = verify_source_format(learner_card.source)
    clarity = check_ambiguity(learner_card)
    
    return {
        'formatted': formatted,
        'citation': citation,
        'suggestions': clarity  # Learner decides to use or not
    }
```

## Quality Indicators

### Good Learner-Authored Card
✅ Addresses specific personal confusion
✅ Written in your natural language
✅ Includes your memory hooks
✅ You decided it was important
✅ You can explain why you made it

### Bad AI-Generated Card
❌ Covers "important" topics you didn't miss
❌ Uses textbook language
❌ No personal relevance
❌ You don't remember making it
❌ Feels foreign during review

## The 8-Card Limit

**Why only 8 per session?**
- Forces prioritization (metacognition)
- Prevents card flood
- Each card gets attention
- Quality over quantity

**When limit is reached:**
- System blocks more cards
- You must decide what's MOST important
- Remaining gaps become tomorrow's priority
- This decision IS learning

## Tracking Authenticity

Every card stores:
```json
{
  "learner_authored": true,
  "content_hash": "sha256:abc123...",  // Proves your exact words
  "from_gap": "4-hour limit",          // Your identified miss
  "ai_assisted": false,                 // Only formatting help
  "generation_timestamp": "2025-01-29T10:30:00Z"
}
```

## Common Scenarios

### Scenario 1: "I want to remember the 4-hour thing"
✅ **Correct Process:**
```
You: "I want to make a card about the 4-hour limit"
System: "Go ahead and write your question"
You: "What's the max daily deep work?"
System: "Now write your answer"
You: "4 hours"
System: "Card created with your content. Adding source: p.47"
```

### Scenario 2: System identifies pattern
❌ **Incorrect Process:**
```
System: "I noticed you missed these 5 concepts. Should I create cards?"
```

✅ **Correct Process:**
```
System: "You identified these gaps: [list]. Which do YOU want to card?"
You: "The first and third one"
System: "Write your question for the first gap"
```

## Special Cases

### Lists and Definitions
Even "simple" cards need your authorship:
- Your mental groupings
- Your ordering
- Your mnemonics

### Application Cards
Especially important for you to write:
- Your scenarios
- Your contexts  
- Your examples

### Image Cards
You choose what to photograph/diagram
You write what it represents
You decide the question angle

## Red Flags for Review

If you find yourself thinking during review:
- "I don't remember making this card"
- "This doesn't sound like me"
- "Why did I think this was important?"

Then the generation effect was bypassed.

## The Paradox

**Your "imperfect" cards that you struggle to write are MORE valuable than "perfect" cards an AI could generate.**

The struggle IS the learning.
The authorship IS the ownership.
The decision IS the metacognition.

## Implementation Checklist

Before creating any card, verify:
- [ ] Learner identified the gap
- [ ] Learner decided it's worth remembering
- [ ] Learner wrote the question
- [ ] Learner wrote the answer
- [ ] AI only helped with formatting
- [ ] Card count is within limit (≤8)
- [ ] Content is stored verbatim with hash

## Remember

When you bypass the generation effect to save time, you're not saving time - you're destroying the very mechanism that makes flashcards work. The inefficiency IS the feature.