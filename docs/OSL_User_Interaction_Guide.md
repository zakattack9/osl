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

**Track your curiosity questions while reading:**
```
You: "Found answer to question 2 about flow state on page 48"
System: Marking question 2 as resolved. What was the answer?
You: "Deep work requires deliberate practice, flow is just the experience"
```

**After reading 5-10 pages (or 1 scene/chapter for literature), STOP:**

```
You: "Done reading pages 45-55"
OR: "Finished chapter 3 scene 2" (for literature)
OR: "Stopping at page 48 - dense material" (3-5 pages for technical)

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

#### C. Tutor Q&A (2-3 min) [AFTER Your Recall & Explanation]
```
System: [AI generates questions based on the material, not your recall quality]
        Let me check your understanding with a few questions.

Q1 (Recall): What's the key difference between deep work and shallow work?

You: [Free text answer - 1-3 sentences]
     "Deep work requires full focus and creates new value, while 
      shallow work is logistical tasks that anyone could do"

System: ✅ Correct! Specifically, Newport emphasizes that shallow work
        is often replicable and doesn't create much new value (p. 46).
        [Immediate corrective feedback enhances testing effect]

Q2 (Application): How would you apply deep work to your current project?

You: "I could block 2 hours each morning for coding without Slack"

System: Good application! Consider also: What specific project outcome
        would benefit most from deep work sessions?

Q3 (Transfer): How might deep work principles apply to learning a new skill?

You: "I'd practice without distractions and focus on the hardest parts first"

System: Excellent transfer! That connects to deliberate practice principles.
```

### 4. Creating Flashcards (3-5 min) [Learner-Authored]

```
System: Time to create flashcards from what YOU identified as important.
        What concepts from pages 45-55 do you want to remember?
        [Generation effect: You decide what becomes a card]

You: "I want to create a card about the 4-hour maximum for deep work"

System: I'll help you format it. What should the question test?
        a) Simple recall of the number
        b) Understanding why there's a limit
        c) Application to your schedule

You: a

System: Here's the format - you provide the content:

FRONT: [What's your question?]

You: "What's the maximum daily deep work capacity for most people?"

BACK: [Your answer?]

You: "4 hours (with training, some can extend to 5)"

System: I'll add the citation. Card created with your content.
        SOURCE: Deep Work, p. 47
        You've made 5/8 cards for this session.
```

**Creating application cards (your decision):**
```
You: "I want to create a card about the Jung tower example"

System: What should the question test?
        a) Recall facts about Jung's tower
        b) Apply the concept Jung demonstrated
        c) Compare/contrast with another example

You: b

System: You write the question:

FRONT: [Your question about applying Jung's example?]

You: "How did Jung's stone tower demonstrate deep work principles?"

BACK: [Your answer?]

You: "He used physical isolation to create uninterrupted thinking time,
     showing that environment design is crucial for deep work"

System: Card created with your content. I can help refine wording if needed.
        [AI assists only - you author the learning material]
```

### 5. Permanent Notes (8-12 min at session end) [Learner-Driven]

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

CITATION (you write to reinforce source awareness):
You: "Newport, Cal. Deep Work (2016), Chapter 3, pages 47-48"

System: Citation format verified ✓

LINKS (you identify connections):
You: "What existing notes might this connect to?"

System: You have these notes in your vault:
        - Attention Residue
        - Deliberate Practice
        - Time Management
        - Flow State
        [Shows titles only - you decide connections]

You: "I'll link to Attention Residue and Time Blocking because..."
```

### 6. Session End (2 min)

```
You: "Ending session"
OR: /osl-session end

System: Session summary:
        ✅ 3 micro-loops completed (real-time tracking)
        ✅ Retrieval rate: 67% (calculated during session)
        ✅ 5 cards created by you (within limit)
        ✅ 2 permanent notes with your links
        ✅ 3/5 curiosity questions resolved
        ⚠️ 1 misconception identified and logged
        
        Unresolved questions to carry forward:
        - Question 4: How does this relate to GTD?
        - Question 5: What about creative work?
        
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

### Curiosity Questions (Start of Session)
- **Format**: Natural questions in your words
- **Number**: 5 questions
- **Tracking**: Note page when answered
- **CLI**: `osl questions add --question "Your question"`

### Free Recall (Preserved Verbatim)
- **Format**: Free text, any structure
- **Length**: 50-200 words
- **Style**: Bullets, paragraphs, or mixed
- **Focus**: What you remember, not what you think is important
- **Preservation**: Your exact text is hashed and stored

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

### Misconception Tracking (Learner-Identified)
```
[During micro-loop Q&A]
You: "Wait, I was wrong about deep work and flow being the same"

System: Let's log this misconception. What did you think?

You: "I thought they were the same thing"

System: And what's the correct understanding?

You: "Deep work is deliberate practice on hard tasks, flow is an
     optimal experience state that might happen during deep work
     but isn't required"

System: Misconception logged:
        Concept: deep work vs flow
        During: micro_loop_2
        Will review next session
        
CLI: osl misconception add --concept "deep work vs flow" \
     --wrong "same thing" --correct "practice vs experience"
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
✅ From YOUR identified gaps (not AI-suggested)
✅ Written in YOUR words (generation effect)
✅ You decided it was worth remembering
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
- Create card? → "I want to make a card about Y"
- Add question? → "osl questions add"
- Track micro-loop? → "osl microloop complete"
- Note misconception? → "I was wrong about X"
- Review? → /osl-review
- Status? → "How am I doing?"
```