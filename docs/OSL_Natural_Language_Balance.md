# OSL Natural Language Balance
_Thin AI layer with explicit confirmations and learner control_

## Core Principle: AI Translates, Never Decides

The AI acts as an **interpreter**, not a decision-maker. Every interpretation is shown, confirmed, and reversible.

## The Three-Layer Model

### Layer 1: Direct CLI (Full Control)
```bash
osl session start --book "Deep Work"
osl flashcard create --front "Q" --back "A"
osl microloop complete --pages 45-50
```
**User knows exactly what will happen**

### Layer 2: Slash Commands (Structured Natural)
```
/osl-session start
/osl-review
```
**Thin wrapper, minimal interpretation**

### Layer 3: Natural Language (Interpreted)
```
"Let's start reading Deep Work"
"I want to review my cards"
```
**AI interprets, but shows translation**

## Implementation Pattern

### Every Natural Language Input Gets:

1. **Interpretation Display**
```
You: "I'm done with chapter 3"

System: I understand you want to end a reading session.
        I'll run: osl session end --chapter 3
        
        Proceed? [Y/n]
```

2. **Explicit Confirmation for State Changes**
```
You: "Make a card about the 4-hour thing"

System: I'll help you create a flashcard.
        First, YOU write the question:
        
You: "What's the daily limit for deep work?"

System: Now YOU write the answer:

You: "4 hours"

System: Creating flashcard with YOUR content:
        FRONT: "What's the daily limit for deep work?"
        BACK: "4 hours"
        SOURCE: Will add page reference
        
        Confirm? [Y/n]
```

3. **Clear Fallback Path**
```
You: "Do the thing with the cards"

System: I'm not sure what you want to do. Options:
        1. Create a new flashcard (/osl-flashcard create)
        2. Review due cards (/osl-review)
        3. See today's card count (/osl-status cards)
        
        Or type the exact command you want.
```

## Interpretation Rules

### What AI Can Interpret

✅ **Session Management:**
- "Start" → `osl session start`
- "Done reading" → `osl session end`
- "How am I doing?" → `osl metrics report`

✅ **Navigation:**
- "Review cards" → `osl review start`
- "Weekly synthesis" → `osl synthesis week`
- "Check governance" → `osl governance status`

✅ **Simple Actions:**
- "Pause" → `osl session pause`
- "Resume" → `osl session resume`
- "Help" → `osl help`

### What AI Cannot Interpret

❌ **Learning Content:**
- Cannot interpret what should become a flashcard
- Cannot interpret importance of concepts
- Cannot interpret connections between ideas

❌ **Subjective Judgments:**
- Cannot interpret quality of recall
- Cannot interpret completeness
- Cannot interpret understanding level

❌ **Complex Decisions:**
- Cannot choose between multiple valid options
- Cannot decide governance adjustments
- Cannot prioritize learning material

## Verbatim Preservation With Context

### Every Learning Input Stored Exactly
```json
{
  "user_input": {
    "raw": "I want to remember that deep work maxes out at 4hrs",
    "timestamp": "2025-01-29T10:30:00Z",
    "hash": "sha256:abc123..."
  },
  "ai_interpretation": {
    "intent": "create_flashcard",
    "extracted": {
      "topic": "deep work limit",
      "detail": "4 hours maximum"
    },
    "confidence": 0.85
  },
  "command_generated": "osl flashcard create",
  "user_confirmed": true,
  "execution_result": "success"
}
```

## Confirmation Patterns

### Type 1: Information Queries (No Confirmation)
```
You: "How many cards do I have due?"
System: You have 47 cards due for review.
        [Direct query, no state change]
```

### Type 2: State Changes (Always Confirm)
```
You: "Start a session"
System: Starting session for 'Deep Work' (your active book)
        This will: 
        - Start timer
        - Check governance gates
        - Create session record
        
        Proceed? [Y/n]
```

### Type 3: Learning Activities (Show Process)
```
You: "Let's do a micro-loop"
System: Starting micro-loop process:
        1. First, you'll do free recall (2 min)
        2. Then Feynman explanation (2 min)
        3. Then I'll ask 2-3 questions
        4. Finally, you create cards from gaps
        
        Ready to start recall? [Y/n]
```

## Error Recovery

### Misinterpretation
```
You: "Check my stuff"
System: I interpreted 'check my stuff' as review cards.
        Did you mean:
        a) Review flashcards (/osl-review)
        b) Check session status (/osl-status)
        c) View metrics (/osl-metrics)
        d) Something else (please specify)
```

### Ambiguous Input
```
You: "Done"
System: 'Done' could mean several things:
        - Done with current recall → Mark recall complete
        - Done with session → End session
        - Done with current page → Start micro-loop
        
        What did you finish?
```

### Failed Command
```
System: The command failed: osl session start
        Error: Already in active session
        
        Would you like to:
        1. Continue current session
        2. End current and start new
        3. See session status
```

## Natural Language Boundaries

### Full Natural Language OK
Activities that don't affect learning:
- Scheduling ("Remind me at 3pm")
- Navigation ("Show weekly summary")
- Queries ("What's my retrieval rate?")
- Admin ("Backup my data")

### Structured Input Required
Activities that ARE learning:
- Free recall text (verbatim)
- Feynman explanations (verbatim)
- Flashcard content (verbatim)
- Permanent notes (verbatim)
- Quiz answers (verbatim)

### Mixed Mode
Workflow guidance with structured content:
```
System: [Natural language guidance]
        "Time for free recall. Write everything you remember."
        
You: [Structured verbatim input]
     The main concept was deep work, which is...
     
System: [Natural language transition]
        "Good! Now explain it simply."
        
You: [Structured verbatim input]
     Deep work is like being in a bubble where...
```

## Implementation Examples

### Good: Clear Interpretation
```python
def interpret_user_input(raw_input):
    interpretation = ai_parse(raw_input)
    
    print(f"I understand you want to: {interpretation.intent}")
    print(f"I'll run: {interpretation.command}")
    print(f"This will: {interpretation.effects}")
    
    if requires_confirmation(interpretation):
        confirm = input("Proceed? [Y/n] ")
        if confirm.lower() != 'y':
            return handle_cancellation()
    
    result = execute_command(interpretation.command)
    return result
```

### Good: Preserved Context
```python
def preserve_with_interpretation(raw_input):
    # Store exactly what user said
    preserved = {
        'raw': raw_input,
        'hash': hashlib.sha256(raw_input.encode()).hexdigest(),
        'timestamp': datetime.now().isoformat()
    }
    
    # Add interpretation layer
    interpreted = {
        'preserved': preserved,
        'ai_intent': detect_intent(raw_input),
        'confidence': calculate_confidence(),
        'command': generate_command()
    }
    
    # Both stored
    save_to_session(interpreted)
```

### Bad: Hidden Interpretation
```python
# NEVER DO THIS
def hidden_interpretation(user_input):
    command = ai_decide_command(user_input)  # Hidden decision
    execute(command)  # No confirmation
    print("Done!")  # No transparency
```

## Quick Reference

| Input Type | AI Role | Confirmation | Preservation |
|------------|---------|--------------|--------------|
| Commands | Translate | Show command | Log intent |
| Questions | Answer | None needed | Log query |
| Learning | Guide only | N/A | Exact verbatim |
| State changes | Interpret | Always | Full context |
| Navigation | Route | None | Log path |

## The Golden Rules

1. **Show Your Work**: Every interpretation visible
2. **Confirm Changes**: Every state change confirmed
3. **Preserve Exactly**: Every learning input verbatim
4. **Fallback Clear**: Manual command always available
5. **Learner Decides**: AI suggests, learner chooses

## Testing Your Implementation

✅ **Good Implementation If:**
- User can see what command will run
- User can cancel before execution
- Original input preserved exactly
- Manual override always possible
- Interpretation confidence shown

❌ **Bad Implementation If:**
- Commands run without showing
- Learning content modified
- No way to correct misinterpretation
- Hidden decision making
- Lost original input

Remember: The AI makes natural interaction possible, but the learner maintains complete control over their learning process.