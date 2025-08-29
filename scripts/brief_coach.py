#!/usr/bin/env python3
"""
Generate AI-readable context from current learning state.
Execute from osl/ root directory.
"""
import json
from datetime import datetime

def generate_coach_context():
    with open('ai_state/coach_state.json') as f:
        state = json.load(f)
    
    context = f"""
Current Learning State:
- Active books: {len(state['active_books'])}
- 7-day retrieval average: {state['performance_metrics']['7d_avg_retrieval']}%
- Card debt ratio: {state['performance_metrics']['current_card_debt_ratio']}x
- Governance gates: {state['governance_status']}
- Next scheduled events: {state['review_schedule']}
"""
    return context

if __name__ == "__main__":
    print(generate_coach_context())
