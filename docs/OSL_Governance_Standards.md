# OSL Governance Standards
_Authoritative thresholds with tuning ranges_

## Core Philosophy

Governance gates prevent overload and ensure quality. They are **adaptive guardrails**, not rigid rules.

## Authoritative Thresholds

### 1. Calibration Gate
**Range:** 75-85%  
**Default:** 80%  
**Measurement:** 7-day rolling average of retrieval success

**When to Use Each Setting:**
- **75%** - Use when:
  - Starting OSL for the first time
  - Learning particularly difficult material
  - Building confidence after a break
  - Dealing with high cognitive load from other sources
  
- **80%** - Use when:
  - In steady-state learning
  - Material is moderate difficulty
  - Normal life circumstances
  
- **85%** - Use when:
  - Preparing for high-stakes application (exam, project)
  - Material is in familiar domain
  - Want to ensure mastery before progressing

**Gate Actions:**
- Below threshold: Reduce new cards to 4, increase review time
- At threshold: Normal operation
- Well above (>90%): Consider more challenging material

### 2. Card Debt Cap
**Range:** 1.5×-2.5× daily throughput  
**Default:** 2.0×  
**Measurement:** Due cards ÷ 7-day average completion rate

**When to Use Each Setting:**
- **1.5×** - Use when:
  - Time is limited (busy period)
  - Quality matters more than quantity
  - Recovering from break or illness
  - High stress periods
  
- **2.0×** - Use when:
  - Normal learning pace
  - Balanced schedule
  - Steady progress desired
  
- **2.5×** - Use when:
  - Have extra time for catch-up
  - Preparing for intensive review period
  - Comfortable with higher review loads
  - Material is becoming easier

**Gate Actions:**
- Above threshold: Block new material until reviews complete
- At threshold: Warning issued
- Below threshold: Normal operation

### 3. New Cards Per Session
**Range:** 4-10 cards  
**Default:** 8 cards  
**Measurement:** Cards created in current session

**When to Use Each Setting:**
- **4-6 cards** - Use when:
  - Dense technical material
  - Starting new subject
  - Card debt is high
  - Calibration gate is triggered
  
- **7-8 cards** - Use when:
  - Standard material complexity
  - Normal learning pace
  - Steady state operation
  
- **9-10 cards** - Use when:
  - Material is familiar domain
  - Review load is low
  - Making rapid progress
  - Lists or definitions (simpler cards)

**Gate Actions:**
- At limit: Prevent additional card creation
- Near limit (1-2 remaining): Warning issued
- Below limit: Show remaining count

### 4. Interleaving Frequency
**Range:** 1-3× per week (or 20-60% of sessions)  
**Default:** 2× per week (or 30-50% of sessions)  
**Measurement:** Sessions with mixed topics

**When to Use Each Setting:**
- **1×/week (20-30%)** - Use when:
  - Deep diving single topic
  - Time constraints
  - Building foundation in new area
  
- **2×/week (30-50%)** - Use when:
  - Normal learning variety
  - Balanced transfer goals
  - Standard OSL operation
  
- **3×/week (50-60%)** - Use when:
  - Preparing for comprehensive exam
  - Need strong transfer skills
  - Multiple active learning topics
  - Want to maximize discrimination

**Session Duration:** 20-30 minutes per interleaving session

### 5. Transfer Project Frequency
**Range:** Every 3-6 weeks  
**Default:** Monthly (4 weeks)  
**Measurement:** Days since last project

**When to Use Each Setting:**
- **3 weeks** - Intensive learning period
- **4 weeks** - Standard pace
- **6 weeks** - When learning single deep topic

## Governance State Machine

```
NORMAL → WARNING → BLOCKED → REMEDIATION → RECOVERY → NORMAL
```

### State Definitions

**NORMAL**: All gates passing
- Full features available
- Standard limits apply

**WARNING**: One gate at threshold
- Visual indicators active
- Suggestions provided
- Can continue with caution

**BLOCKED**: Hard gate triggered
- New material blocked
- Must address issue
- Clear remediation path shown

**REMEDIATION**: Actively fixing
- Focused review sessions
- Reduced new material
- Progress tracking

**RECOVERY**: Returning to normal
- Gates clearing
- Gradual increase allowed
- Monitoring continues

## Adjustment Protocol

### Who Can Adjust
- Learner: Within ranges at any time
- Coach AI: Suggest based on patterns
- System: Emergency adjustments only

### How to Adjust
```bash
osl governance set --calibration-gate 75
osl governance set --card-debt-cap 1.5
osl governance set --max-new-cards 6
osl governance set --interleaving-freq 1
```

### When to Adjust
- Weekly review shows consistent pattern
- Life circumstances change
- Material difficulty shifts
- Preparation for specific goal

## Tracking and Reporting

### Daily Metrics
- Current gate status (PASS/WARN/FAIL)
- Distance from thresholds
- Suggested adjustments

### Weekly Rollup
- Average performance vs gates
- Number of triggers
- Time in each state
- Trend direction

### Monthly Analysis
- Gate effectiveness
- Adjustment history
- Learning velocity impact
- Recommendations

## Emergency Overrides

Only in exceptional circumstances:
- System allows one-time override
- Must document reason
- Automatically reverts next session
- Coach AI reviews pattern

## Implementation Notes

1. **Store in `coach_state.json`:**
```json
{
  "governance_thresholds": {
    "calibration_gate": {
      "min": 75,
      "current": 80,
      "max": 85
    },
    "card_debt_multiplier": {
      "min": 1.5,
      "current": 2.0,
      "max": 2.5
    },
    "max_new_cards": {
      "min": 4,
      "current": 8,
      "max": 10
    },
    "interleaving_per_week": {
      "min": 1,
      "current": 2,
      "max": 3
    }
  },
  "governance_status": {
    "calibration_gate": "passing",
    "card_debt_gate": "passing",
    "transfer_gate": "passing",
    "overall_state": "NORMAL"
  }
}
```

2. **Check at key points:**
   - Session start
   - Before card creation
   - Weekly review
   - After metric calculation

3. **Clear communication:**
   - Always explain why gate triggered
   - Show path to resolution
   - Celebrate when gates clear

## Philosophy Reminder

Governance gates are **teaching tools**, not punishment. They help you:
- Maintain sustainable pace
- Ensure quality over quantity
- Prevent overwhelm
- Build lasting knowledge

Adjust them to serve your learning, not to game the system.