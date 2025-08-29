# OSL Parsing Framework
_Structured extraction while preserving verbatim inputs_

---

## Core Principle: Dual Storage

1. **Raw Layer**: Original user input stored verbatim with hash
2. **Parsed Layer**: Structured extraction with source reference
3. **Approval Layer**: User confirms parsing before final storage

```
User Input → Raw Storage → Parser → Preview → User Approval → Structured Storage
     ↓                                    ↓                          ↓
  [Verbatim]                        [Can Reject]              [Links to Raw]
```

---

## Parsing Architecture

### Storage Structure

```json
// ai_state/session_inputs/{session_id}_parsed.json
{
  "parsed_items": {
    "flashcard_1": {
      "raw_input_id": "input_7",
      "raw_text": "I want to remember that deep work has a maximum of 4 hours per day for most people",
      "parsed": {
        "type": "flashcard",
        "front": "What is the maximum daily capacity for deep work for most people?",
        "back": "4 hours per day",
        "parser": "intent_to_card",
        "confidence": 0.95
      },
      "user_approved": true,
      "approval_timestamp": "2025-01-29T15:45:00Z"
    },
    "permanent_note_1": {
      "raw_input_id": "input_12",
      "raw_text": "The 4-hour limit exists because deep work is cognitively demanding and our brains have limited glucose and attention resources. This applies to mental work but not physical labor. Like how athletes can train for hours but need recovery.",
      "parsed": {
        "type": "permanent_note",
        "claim": "Deep work has a 4-hour daily limit due to cognitive resource constraints",
        "context": "This applies to mental work but not physical labor",
        "example": "Athletes can train for hours but need recovery",
        "parser": "note_extractor",
        "confidence": 0.87
      },
      "user_approved": false,
      "user_edited": {
        "claim": "Humans have a biological limit of about 4 hours for deep work",
        "context": "Applies to cognitively demanding tasks, not routine work",
        "example": "Like how athletes can train physically for hours but mental training is limited"
      }
    }
  }
}
```

---

## Parsing Rules (Deterministic)

### Flashcard Parsers

```python
# osl/parsers/flashcard_parser.py
class FlashcardParser:
    """Deterministic parsing of user input into flashcards"""
    
    def parse(self, raw_text, context=None):
        """Parse text into flashcard structure"""
        
        # Pattern 1: Explicit Q&A
        if '?' in raw_text:
            parts = raw_text.split('?')
            if len(parts) == 2:
                return {
                    'parser': 'explicit_qa',
                    'front': parts[0].strip() + '?',
                    'back': parts[1].strip(),
                    'confidence': 0.95
                }
        
        # Pattern 2: "I want to remember X"
        remember_match = re.match(r"(?:I want to remember|Remember that|Don't forget):?\s*(.*)", raw_text, re.I)
        if remember_match:
            fact = remember_match.group(1)
            return {
                'parser': 'remember_intent',
                'front': self._generate_question(fact),
                'back': self._extract_answer(fact),
                'confidence': 0.85
            }
        
        # Pattern 3: "X is Y" statements
        is_match = re.match(r"(.*?)\s+(?:is|are|was|were)\s+(.*)", raw_text)
        if is_match and len(raw_text) < 200:  # Short enough for card
            return {
                'parser': 'definition',
                'front': f"What is {is_match.group(1)}?",
                'back': is_match.group(2),
                'confidence': 0.75
            }
        
        # Pattern 4: Cloze detection
        if '{{c1::' in raw_text or '__' in raw_text:
            return {
                'parser': 'cloze',
                'text': raw_text.replace('__', '{{c1::}}'),
                'type': 'cloze',
                'confidence': 0.99
            }
        
        return None
    
    def _generate_question(self, fact):
        """Generate question from statement - DETERMINISTIC"""
        # Use templates, not AI
        if 'maximum' in fact or 'limit' in fact:
            return "What is the " + self._extract_subject(fact) + "?"
        elif 'because' in fact:
            parts = fact.split('because')
            return f"Why {parts[0].strip()}?"
        else:
            return f"What do you know about: {self._extract_subject(fact)}?"
```

### Permanent Note Parser

```python
# osl/parsers/note_parser.py
class PermanentNoteParser:
    """Extract structured note from paragraph"""
    
    def parse(self, raw_text):
        """Parse into claim, context, example"""
        
        sentences = self._split_sentences(raw_text)
        
        # Look for structure markers
        structure = {
            'claim': None,
            'context': None,
            'example': None
        }
        
        # Explicit markers
        for sent in sentences:
            if sent.lower().startswith(('the claim:', 'claim:', 'main point:')):
                structure['claim'] = sent.split(':', 1)[1].strip()
            elif sent.lower().startswith(('applies to:', 'context:', 'when:')):
                structure['context'] = sent.split(':', 1)[1].strip()
            elif sent.lower().startswith(('example:', 'for instance:', 'like:')):
                structure['example'] = sent.split(':', 1)[1].strip()
        
        # Implicit structure (if no markers)
        if not structure['claim'] and sentences:
            # First sentence often the claim
            structure['claim'] = sentences[0]
            
            # Look for context clues
            for sent in sentences[1:]:
                if not structure['context'] and any(word in sent.lower() for word in ['applies', 'when', 'during', 'for']):
                    structure['context'] = sent
                elif not structure['example'] and any(word in sent.lower() for word in ['example', 'like', 'such as', 'instance']):
                    structure['example'] = sent
        
        return structure
```

---

## User Approval Flow

### Interactive Parsing Approval

```python
# osl/cli_commands.py
def cmd_flashcard_create(self, args):
    """Create flashcard with user approval"""
    
    # 1. Store raw input verbatim
    raw_input_id = self.preserver.preserve_input(
        'flashcard_intent',
        args.text,
        'CARDS_ACTIVE'
    )
    
    # 2. Parse using deterministic rules
    parser = FlashcardParser()
    parsed = parser.parse(args.text)
    
    if not parsed:
        return self.error_with_suggestion(
            "Couldn't parse into flashcard format",
            "Try: 'Question? Answer' or 'I want to remember X'"
        )
    
    # 3. Show user the parsed version
    preview = f"""
    Parsed your input into:
    
    FRONT: {parsed.get('front', parsed.get('text'))}
    BACK: {parsed.get('back', '[cloze deletion]')}
    
    Original: "{args.text[:100]}..."
    Parser: {parsed['parser']} (confidence: {parsed['confidence']:.0%})
    
    Options:
    1. Approve - Create this card
    2. Edit - Modify the card
    3. Manual - Type your own Q&A
    4. Skip - Don't create a card
    """
    
    # 4. Get user choice
    choice = self.get_user_input(preview)
    
    if choice == '1':  # Approve
        # Store both raw and parsed
        self.store_parsed_item('flashcard', raw_input_id, parsed)
        return self.success_response({
            'card_created': True,
            'raw_preserved': raw_input_id,
            'structure': parsed
        })
    
    elif choice == '2':  # Edit
        return self.interactive_edit(parsed)
    
    elif choice == '3':  # Manual
        return self.manual_card_creation(raw_input_id)
    
    else:  # Skip
        return self.success_response({'skipped': True})
```

### Manual Override Option

```
System: I parsed your input into this flashcard:

FRONT: What is the maximum daily capacity for deep work?
BACK: 4 hours per day

Is this correct? (yes/edit/manual)

User: edit

System: Edit the card:
FRONT [What is the maximum daily capacity for deep work?]: 
User: "What's the deep work hour limit for most people?"

BACK [4 hours per day]: 
User: "4 hours (some can extend to 5 with training)"

System: ✅ Card created with your edits
Original input preserved with ID: input_7
```

---

## Parsing Categories

### 1. Flashcards

| User Input Pattern | Parsing Method | Example |
|-------------------|----------------|---------|
| "Question? Answer" | Split on ? | "What is deep work? Focused cognition" |
| "I want to remember X" | Extract X as answer | "I want to remember the 4-hour limit" |
| "Term: Definition" | Split on : | "Deep work: Cognitively demanding activities" |
| Cloze with __ or {{c1::}} | Direct cloze | "The limit is __4 hours__" |
| "X because Y" | Why X? → Because Y | "Deep work is valuable because it's rare" |

### 2. Permanent Notes

| Content Pattern | Extraction | Structure |
|----------------|------------|-----------|
| First sentence = claim | Sentence 1 | Claim |
| "This applies to..." | Context markers | Context |
| "For example..." | Example markers | Example |
| "Like..." | Analogy as example | Example |

### 3. Quiz Answers

| Answer Type | Parsing | Validation |
|------------|---------|------------|
| List items | Split on bullets/numbers | Check count |
| Definition | First sentence | Check key terms |
| Explanation | Full paragraph | Check length |
| Application | Scenario + action | Check both parts |

---

## Validation Rules

### Parsed Content Validation

```python
def validate_parsing(raw_input, parsed_output):
    """Ensure parsing preserves meaning"""
    
    # 1. All key terms from raw must appear in parsed
    raw_terms = extract_key_terms(raw_input)
    parsed_terms = extract_key_terms(str(parsed_output))
    
    missing = raw_terms - parsed_terms
    if missing:
        return {
            'valid': False,
            'warning': f'Key terms lost: {missing}',
            'suggestion': 'Review parsing - information may be lost'
        }
    
    # 2. No new information added
    if len(parsed_output) > len(raw_input) * 1.5:
        return {
            'valid': False,
            'warning': 'Parsed version seems to add information',
            'suggestion': 'Check that parser didn\'t invent content'
        }
    
    # 3. Reversibility check
    if can_reconstruct_original(raw_input, parsed_output):
        return {'valid': True, 'reversible': True}
    
    return {'valid': True, 'reversible': False, 'note': 'Structure extracted'}
```

---

## CLI Parser Commands

```bash
# Parse with preview
osl parse flashcard --text "I want to remember the 4-hour limit"
Output:
  Suggested card:
  Q: What is the 4-hour limit?
  A: [Extracted from your input]
  
  Approve? (y/n/edit)

# Parse permanent note
osl parse note --text "Deep work has limits because..."
Output:
  Extracted structure:
  Claim: Deep work has limits
  Context: [Extracted]
  Example: [Extracted or request]
  
  Approve? (y/n/edit)

# Batch parsing with review
osl parse batch --file recall_1.txt --type flashcards
Output:
  Found 5 potential flashcards:
  1. [Preview] (y/n/edit)
  2. [Preview] (y/n/edit)
  ...

# Show parsing confidence
osl parse analyze --text "complex statement"
Output:
  Parsing options:
  1. Flashcard (confidence: 45%)
  2. Permanent note (confidence: 78%)
  3. Keep as-is (confidence: 95%)
  
  Recommendation: Keep as-is for manual processing
```

---

## Edge Cases

### Ambiguous Input

```
User: "The limit is 4 hours but some say 5"

System: This could be parsed multiple ways:

Option A - Simple fact:
Q: What is the limit?
A: 4 hours (but some say 5)

Option B - Nuanced:
Q: What is the typical deep work limit?
A: 4 hours
Q: Can the limit be extended?
A: Yes, some achieve 5 hours

Option C - Keep original:
Store as-is for manual card creation

Choose: A, B, or C?
```

### Multiple Facts

```
User: "Deep work needs focus, time blocks, and no distractions. 
       Maximum 4 hours. Jung had a tower for this."

System: Found multiple facts. Create:
□ Card about requirements (focus, time, no distractions)
□ Card about 4-hour maximum
□ Card about Jung's tower
□ One combined card
□ Permanent note instead

Select which to create (space-separated numbers):
```

### Unparseable Input

```
User: [Long rambling paragraph with no clear structure]

System: This is too complex for automatic parsing.
Options:
1. Save as recall text (verbatim)
2. Break into smaller parts
3. Create permanent note manually
4. Skip and continue

Your choice:
```

---

## Configuration

```yaml
# osl_config.yaml
parsing:
  require_approval: true
  show_confidence: true
  min_confidence: 0.7
  
  flashcard_patterns:
    - explicit_qa      # Question? Answer
    - remember_intent  # I want to remember X
    - definition       # X is Y
    - cloze           # Text with __blanks__
    
  note_patterns:
    - claim_first     # First sentence as claim
    - explicit_markers # Claim: X, Context: Y
    - paragraph_split  # Split by meaning
    
  preservation:
    always_store_raw: true
    link_to_source: true
    show_original: true
    allow_edit: true
    
  approval_timeout: 30  # seconds before auto-skip
```

---

## Summary

This parsing framework achieves:

1. **Verbatim Preservation**: Original always stored with hash
2. **Structured Extraction**: Deterministic parsing into useful formats
3. **User Control**: Preview and approve all parsing
4. **Reversibility**: Can always get back to original
5. **Transparency**: Shows which parser used and confidence
6. **Manual Override**: User can always edit or create manually

The key insight: **The CLI tool does parsing, not AI**. AI only identifies which parser to use. This maintains determinism while enabling practical structured storage.