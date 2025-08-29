# OSL User Interaction Guide
_How to actually use OSL: What you type, when you type it, and what format to use_

---

## Daily Session Flow (45 minutes)

### 1. Starting Your Session (2 min)
```
You: "Starting Deep Work chapter 3"
OR: /osl-session start

System: ✅ Session started for Deep Work
        ⚠️ You have 12 cards due for review
        Timer running...
```

### 2. Reading Phase (20-25 min)

**After reading 5-10 pages, STOP and enter micro-loop:**

```
You: "Done reading pages 45-55"
OR: Just pause and wait

System: Great! Let's process what you just read.
        Starting micro-loop...
```

### 3. Micro-Loop Interaction (5-7 min per chunk)

#### A. Free Recall (1-2 min)
```
System: Take 1-2 minutes to write everything you remember from pages 45-55.
        Type 'done' when finished.

You: [Type freely in any format]
     "The main concept was deep work, which Newport defines as...
      Three key points:
      - Focused attention without distraction
      - Produces high value
      - Hard to replicate
      
      He gave an example about Carl Jung's tower..."
      
You: done
```

#### B. Feynman Explanation (2-3 min)
```
System: Now explain the main concept as if teaching a smart 12-year-old.
        Focus on: What it is, why it matters, and an example.

You: [Write 3-5 sentences]
     "Deep work is when you focus completely on one hard task without 
      checking your phone or email. It's like when you're so into a 
      video game that you forget everything else - but for important work.
      This matters because robots and computers can't do this kind of 
      thinking yet, so people who can do it will have the best jobs."

System: Good explanation! You covered the concept and importance.
        Consider adding: How is this different from regular work?
```

#### C. Tutor Q&A (2-3 min)
```
System: Let me check your understanding with a few questions.

Q1: What's the key difference between deep work and shallow work?

You: [Free text answer - 1-3 sentences]
     "Deep work requires full focus and creates new value, while 
      shallow work is logistical tasks that anyone could do"

System: ✅ Correct! Specifically, Newport emphasizes that shallow work
        is often replicable and doesn't create much new value (p. 46).

Q2: How would you apply deep work to your current project?

You: "I could block 2 hours each morning for coding without Slack"

System: Good application! Consider also: What specific project outcome
        would benefit most from deep work sessions?
```

### 4. Creating Flashcards (3-5 min)

```
System: Based on your retrieval gaps, let's create flashcards.
        I noticed you missed the "4 hours maximum" concept.

Suggested card - approve, edit, or skip?

FRONT: The maximum daily deep work capacity for most people is {{c1::?}} hours
BACK: 4 hours (with training, some can extend to 5)
SOURCE: Deep Work, p. 47

You: approve
OR: "edit - change to 3-4 hours"
OR: "skip"
OR: "I want to create one about Jung's tower"

System: Card created. You've made 5/8 cards for this session.
```

**Creating your own cards:**
```
You: "Create a card about the Jung tower example"

System: What should the question test?
        a) Recall facts about Jung's tower
        b) Apply the concept Jung demonstrated
        c) Compare/contrast with another example

You: b

System: Here's a draft:

FRONT: Carl Jung built a stone tower to escape Zurich. How does this 
       demonstrate deep work principles?
BACK: [What's the answer?]

You: "He used physical isolation to create uninterrupted thinking time,
     showing that environment design is crucial for deep work"

System: Card created with your answer.
```

### 5. Permanent Notes (8-12 min at session end)

```
System: Time to create permanent notes. What was the most important 
        insight from today's reading?

You: "The 4-hour limit on deep work"

System: Let's structure this as a permanent note:

Fill in each section (2-3 sentences each):

CLAIM (your own words):
You: "Humans have a biological limit of about 4 hours of deep work
     per day, regardless of training or motivation"

CONTEXT (when does this apply/fail?):
You: "Applies to cognitively demanding tasks requiring full focus.
     Doesn't apply to physical work or routine tasks that can be
     done on autopilot"

EXAMPLE:
You: "Even famous productive people like Darwin worked intensely for
     3-4 hours in the morning, then walked and corresponded in PM"

CITATION:
System: Auto-filled: Newport, Deep Work (2016), Ch. 3, p. 47-48

LINKS:
System: Related notes found:
        - [[Attention Residue]]
        - [[Deliberate Practice]]
        Select any that connect (or type new ones):

You: "Link to Attention Residue and add new link to Time Blocking"
```

### 6. Session End (2 min)

```
You: "Ending session"
OR: /osl-session end

System: Session summary needed:
        - Pages read?
        
You: "15 pages (45-60)"

System: - How many retrieval attempts?

You: "3 chunks"

System: - Successful recalls (felt confident)?

You: "2 good, 1 partial"

System: Session logged:
        ✅ Retrieval rate: 67%
        ✅ 5 cards created (3 from misses)
        ✅ 2 permanent notes
        ⚠️ Calibration slightly low - you predicted 80% but got 67%
        
        Next: Run /osl-review for your 12 due cards
```

---

## Weekly Synthesis (60-90 min)

### 1. Prediction Phase (5 min)
```
System: Weekly calibration time! First, predict your performance.
        
        How well do you know these topics (0-100%)?
        - Deep Work principles: ___
        - Attention management: ___
        - Time blocking methods: ___

You: "85, 70, 60"

System: Noted. Let's test your actual knowledge.
```

### 2. Quiz Format (20-30 min)

**Recall Questions:**
```
System: Q1: List the four disciplines of deep work execution.

You: [Bullet points or sentences]
     "- Focus on wildly important
      - Act on lead measures  
      - Keep a compelling scoreboard
      - Create accountability cadence"

System: ✅ All four correct! (p. 136-150)
```

**Application Questions:**
```
System: Q2: You have a busy open office. Design a deep work routine 
            using Newport's strategies.

You: [Paragraph answer]
     "I would use the rhythmic philosophy by blocking 7-9am daily
      before others arrive. I'd use visual cues like headphones and
      a 'deep work' sign. For accountability, I'd track hours on a
      visible calendar and review weekly with a colleague."

System: Good application of multiple strategies! 
        Consider also: How would you handle urgent requests during blocks?
```

**Transfer Questions:**
```
System: Q3: How might deep work principles apply to learning a musical
            instrument?

You: "Practice sessions would focus on difficult passages without
     interruption, rather than playing through pieces casually.
     Use a timer for focused technique work. Track progress on
     specific skills rather than just time practiced."

System: Excellent transfer! You've connected deliberate practice
        with deep work principles.
```

### 3. Synthesis Essay (30 min)
```
System: Write a 1-page synthesis connecting 2-3 concepts from this week.
        Focus on integration, not summary.

You: [Write directly or paste from editor]

Title: "Deep Work and Habit Formation: A Synergistic System"

"This week's readings on deep work (Newport) and atomic habits (Clear)
reveal a powerful synergy: deep work requires habitual practice to
be sustainable. Newport's call for 4 hours of daily deep work seems
daunting until viewed through Clear's habit-stacking lens...

[Continue for ~300-400 words]

...Therefore, the path to consistent deep work isn't through heroic
effort but through systematic habit design that makes focus the
default mode."

System: Synthesis captured. Strong connections between Newport and Clear.
        Added to: obsidian/20_synthesis/2024_week_4.md
```

---

## Input Format Reference

### Free Recall
- **Format**: Free text, any structure
- **Length**: 50-200 words
- **Style**: Bullets, paragraphs, or mixed
- **Focus**: What you remember, not what you think is important

### Feynman Explanations
- **Format**: Plain language paragraph
- **Length**: 3-5 sentences
- **Components**: What + Why + Example
- **Audience**: Smart 12-year-old

### Quiz Answers
- **Recall**: Lists, definitions, or short phrases
- **Application**: 1-2 paragraph scenarios
- **Transfer**: Paragraph connecting to new domain
- **Confidence**: Number 1-5 before each answer

### Flashcard Creation
- **Cloze format**: "The {{c1::answer}} is the key"
- **Application format**: 
  - Front: Scenario/question
  - Back: Action/answer + reasoning
- **Source**: Always included (page/location)

### Permanent Notes
- **Claim**: 1-2 sentences, your words
- **Context**: 2-3 sentences, boundaries
- **Example**: 2-3 sentences, concrete
- **Citation**: Author, Title (Year), location
- **Links**: [[Note Name]] format

### Misconception Tracking
```
You: "I was confused about the difference between deep work and flow"

System: Let's clarify this misconception:
        - Your understanding: "They're the same thing"
        - Correct understanding: [What's the actual difference?]

You: "Deep work is deliberate practice on hard tasks, flow is an
     optimal experience state that might happen during deep work
     but isn't required"

System: Misconception logged and will be reviewed next session.
```

---

## Natural Language Variations

The system understands many ways to say the same thing:

### Starting Work
- "Let's start"
- "Beginning chapter 3"
- "I'm ready to read"
- "Starting Deep Work"
- /osl-session start

### Completing Activities
- "Done"
- "Finished reading"
- "That's all I remember"
- "Ready for questions"
- "Next"

### Creating Items
- "Make a card about X"
- "I want to remember Y"
- "Create permanent note on Z"
- "That's worth a flashcard"

### Getting Help
- "What should I do now?"
- "How does this work?"
- "Show me an example"
- "I'm stuck"

---

## Common Scenarios

### Interrupted Session
```
You: "Need to pause - emergency"
System: Session paused at page 55. Run '/osl-session resume' when ready.
```

### Confused About Content
```
You: "I don't understand this concept at all"
System: Let's break it down. First, what specific part is confusing?
        Would you like me to:
        1. Ask clarifying questions
        2. Provide an analogy
        3. Skip and mark for review
```

### Too Many Cards Due
```
You: "I have 50 cards due, too many!"
System: Card debt detected. Options:
        1. Quick review: High-yield cards only (15 cards, 10 min)
        2. Suspend lowest-performing 30% 
        3. Power session: Clear all (30-40 min)
```

### Not Sure What to Create
```
You: "Should I make a card or permanent note about this?"

System: Quick decision tree:
        - Failed to recall it? → Flashcard
        - Important principle? → Permanent note  
        - Connects ideas? → Both
        - Just interesting? → Skip
```

---

## Quality Standards

### Good Flashcard
```
✅ Tests one concept
✅ Clear, unambiguous
✅ Includes source
✅ From actual retrieval miss
```

### Good Permanent Note
```
✅ Your own words
✅ Shows when it applies/fails
✅ Concrete example
✅ Properly cited
✅ Linked to related ideas
```

### Good Feynman Explanation
```
✅ Simple language
✅ Accurate concept
✅ Includes why it matters
✅ Uses analogy or example
```

---

## Quick Reference Card

```
DAILY FLOW (45 min)
1. Start: "Beginning [book]"
2. Read: 5-10 pages
3. Recall: Type what you remember
4. Explain: Teach it simply  
5. Answer: Tutor's questions
6. Create: Cards from misses
7. Note: Permanent insights
8. End: "Finished, 15 pages"

WEEKLY (90 min)
1. Predict: Rate confidence
2. Quiz: Answer 6-10 questions
3. Score: Compare prediction
4. Write: 1-page synthesis
5. Map: Update concept connections

SHORTCUTS
- Stuck? → "Help"
- Confused? → "I don't understand X"
- Create? → "Make a card about Y"
- Review? → /osl-review
- Status? → "How am I doing?"
```