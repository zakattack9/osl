# OSL Interleaving Specification
_Mixed practice detection and scheduling for discrimination learning_

## Purpose: Strengthen Discrimination Through Mixing

Interleaving forces your brain to discriminate between similar concepts, improving both retention and transfer. It's the difference between recognizing patterns and truly understanding distinctions.

## Two Implementation Models

### Model 1: Dedicated Interleaving Sessions
**2× per week, 20-30 minutes each**
```
Monday: Regular Deep Work reading
Tuesday: Regular Atomic Habits reading  
Wednesday: INTERLEAVING SESSION (mix both)
Thursday: Regular Deep Work reading
Friday: Regular Atomic Habits reading
Saturday: INTERLEAVING SESSION (mix both)
Sunday: Weekly synthesis
```

### Model 2: Natural Interleaving Detection
**Track topic switches within regular sessions**
```
If 30-50% of session time involves multiple topics:
→ Count as interleaving
→ No separate session needed
```

## Mixing Ratios

### Optimal Distribution (20-30 min session)
```
40% - Current week's material (8-12 min)
40% - Recent material (last 2-3 weeks) (8-12 min)
20% - Distant/adjacent material (older or cross-domain) (4-6 min)
```

### Example Session Breakdown
```
Minutes 1-8:    Chapter 5 problems (current)
Minutes 9-16:   Chapter 3 concepts (recent)
Minutes 17-20:  Chapter 1 principles (distant)
Minutes 21-24:  Apply to different book (transfer)
```

## Detection Algorithm

### Automatic Detection in Regular Sessions
```python
def detect_interleaving(session_data):
    """Detect if session qualifies as interleaving"""
    
    # Track topic switches
    topics = []
    for activity in session_data['activities']:
        topics.append(activity['topic'])
    
    unique_topics = len(set(topics))
    topic_switches = count_transitions(topics)
    
    # Calculate mixing percentage
    total_time = session_data['duration_minutes']
    mixed_time = calculate_mixed_minutes(session_data)
    mixing_ratio = mixed_time / total_time
    
    # Criteria for interleaving credit
    if (unique_topics >= 2 and 
        topic_switches >= 3 and 
        mixing_ratio >= 0.3):
        return True
    
    return False
```

### Manual Interleaving Session
```python
def create_interleaving_session(books, week_number):
    """Create dedicated interleaving session"""
    
    session = {
        'type': 'interleaving',
        'duration_target': 25,  # minutes
        'materials': []
    }
    
    # Add current material (40%)
    session['materials'].append({
        'source': books['current'],
        'chapters': get_current_week_chapters(week_number),
        'duration': 10,
        'activity': 'retrieval_practice'
    })
    
    # Add recent material (40%)
    session['materials'].append({
        'source': books['current'],
        'chapters': get_recent_chapters(week_number - 2),
        'duration': 10,
        'activity': 'application_problems'
    })
    
    # Add distant/transfer (20%)
    session['materials'].append({
        'source': books['secondary'],
        'chapters': 'connections',
        'duration': 5,
        'activity': 'transfer_exercise'
    })
    
    return session
```

## Scheduling Logic

### Coach AI Scheduling
```python
def schedule_interleaving(state):
    """Determine when interleaving is due"""
    
    # Get current settings
    target_per_week = state['governance_thresholds']['interleaving_per_week']['current']
    completed_this_week = state['performance_metrics']['interleaving_sessions_week']
    
    # Check if behind schedule
    days_into_week = datetime.now().weekday()
    expected_by_now = (target_per_week / 7) * days_into_week
    
    if completed_this_week < expected_by_now:
        return {
            'status': 'DUE',
            'message': f'Interleaving session needed ({completed_this_week}/{target_per_week} this week)',
            'suggested_time': 'today'
        }
    
    return {
        'status': 'ON_TRACK',
        'next_due': calculate_next_session_time(state)
    }
```

### Flexible Scheduling Options
```json
{
  "interleaving_preferences": {
    "mode": "dedicated|natural|hybrid",
    "dedicated_days": ["wednesday", "saturday"],
    "dedicated_time": "09:00",
    "min_mixing_ratio": 0.3,
    "max_mixing_ratio": 0.6,
    "preferred_duration": 25,
    "auto_detect": true
  }
}
```

## Activity Types for Interleaving

### 1. Discrimination Exercises
```
Present similar concepts from different sources:
- Deep Work "Focus" vs GTD "Next Actions"
- Atomic Habits "Systems" vs Deep Work "Disciplines"
- Memory Palace "Loci" vs Anki "Spaced Repetition"

Task: Identify which principle applies to scenario
```

### 2. Mixed Retrieval Practice
```
Quiz questions randomly drawn from:
- 40% current chapter
- 40% previous chapters
- 20% different book

No warning about source switching
```

### 3. Transfer Applications
```
Take principle from Book A, apply to Book B context:
- Apply Deep Work to language learning
- Apply Atomic Habits to deep work practice
- Apply memory techniques to coding
```

### 4. Comparison Tables
```
Create during session:
| Concept | Deep Work | Atomic Habits | Similarities | Differences |
|---------|-----------|---------------|--------------|-------------|
| Focus   | ...       | ...           | ...          | ...         |
```

## Implementation in State

### Session Tracking
```json
{
  "session_id": "20250129_103000",
  "type": "interleaving",
  "materials_covered": [
    {
      "book": "Deep Work",
      "chapters": [3, 5],
      "duration_minutes": 10,
      "activity": "retrieval"
    },
    {
      "book": "Atomic Habits", 
      "chapters": [2],
      "duration_minutes": 10,
      "activity": "application"
    },
    {
      "book": "both",
      "activity": "comparison",
      "duration_minutes": 5
    }
  ],
  "mixing_metrics": {
    "topic_switches": 8,
    "unique_topics": 4,
    "mixing_ratio": 0.45,
    "discrimination_exercises": 3
  }
}
```

### Weekly Rollup
```json
{
  "week_number": 4,
  "interleaving_summary": {
    "target_sessions": 2,
    "completed_sessions": 2,
    "natural_interleaving_detected": 1,
    "dedicated_sessions": 1,
    "total_interleaving_minutes": 55,
    "topics_mixed": ["deep_work", "atomic_habits", "memory"],
    "transfer_exercises_completed": 3
  }
}
```

## User Experience

### Starting Dedicated Session
```
System: Time for interleaving practice! (25 min)
        Today we'll mix:
        - Deep Work Ch 5 (current) - 10 min
        - Deep Work Ch 3 (recent) - 10 min  
        - Atomic Habits connections - 5 min
        
        Ready? [Y/n]

You: Y

System: Starting with retrieval from Chapter 5...
        [No warning when switching topics]
```

### Natural Detection Notification
```
System: Great session! I noticed you naturally interleaved:
        - 45% Deep Work content
        - 35% Atomic Habits content
        - 20% connection exercises
        
        This counts as 1 of 2 weekly interleaving sessions ✓
```

### Scheduling Reminder
```
System: You're due for an interleaving session.
        Options:
        1. Quick 20-min dedicated session now
        2. Natural mixing in your next reading
        3. Schedule for tomorrow morning
        
        What works best?
```

## Benefits Tracking

### Metrics to Monitor
```python
def calculate_interleaving_benefits(state):
    """Track benefits of interleaving"""
    
    metrics = {
        'discrimination_accuracy': 0,  # % correct on similar concepts
        'transfer_success': 0,         # % successful applications
        'retention_delta': 0,          # Improvement vs blocked practice
        'confusion_reduction': 0       # Decrease in mix-ups
    }
    
    # Compare interleaved vs blocked practice
    interleaved = state['interleaved_topics']
    blocked = state['blocked_topics']
    
    metrics['discrimination_accuracy'] = (
        interleaved['correct'] / interleaved['total']
    )
    
    metrics['retention_delta'] = (
        interleaved['7d_retention'] - blocked['7d_retention']
    )
    
    return metrics
```

## Governance Integration

### Adjustment Triggers
```
If discrimination_accuracy < 60%:
    → Increase interleaving to 3×/week
    
If retention_delta < 10%:
    → Adjust mixing ratio
    
If confusion increasing:
    → Reduce to 1×/week temporarily
```

### Settings Range
- **Minimum**: 1×/week (single domain focus)
- **Default**: 2×/week (balanced)
- **Maximum**: 3×/week (exam prep or high transfer needs)

## Common Patterns

### Pattern 1: Book Comparison
Alternate between two books on similar topics
- Session 1: Book A only
- Session 2: Book B only
- Session 3: Mix A and B
- Repeat

### Pattern 2: Progressive Mixing
Gradually increase mixing ratio:
- Week 1: 80% blocked, 20% mixed
- Week 2: 60% blocked, 40% mixed
- Week 3: 50% blocked, 50% mixed

### Pattern 3: Transfer Focus
Each interleaving session has transfer theme:
- Session 1: Apply to work
- Session 2: Apply to personal projects
- Session 3: Apply to learning itself

## CLI Commands

```bash
# Start dedicated interleaving
osl interleave start --duration 25

# Check interleaving status
osl interleave status
# Output: 1/2 sessions complete this week

# Configure preferences
osl interleave config --mode hybrid --target 2

# Review interleaving benefits
osl metrics interleaving
# Shows discrimination accuracy, retention delta
```

## Key Principles

1. **No Warning**: Don't announce topic switches
2. **Force Discrimination**: Make brain identify source
3. **Track Benefits**: Monitor if it's working
4. **Stay Flexible**: Adjust based on results
5. **Credit Both**: Natural and dedicated both count

## Remember

Interleaving feels harder than blocked practice - that's the point. The difficulty IS the learning signal. Your brain working to discriminate between concepts strengthens both.

**Confusion during interleaving → Clarity during application**