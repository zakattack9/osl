#!/usr/bin/env python3
"""
Update coach state with session data.
Execute from osl/ root directory.
"""
import json
import sys
from datetime import datetime
from pathlib import Path

def update_state(session_log_path, state_path='ai_state/coach_state.json'):
    # Load current state
    with open(state_path) as f:
        state = json.load(f)
    
    # Load session log
    if Path(session_log_path).exists():
        with open(session_log_path) as f:
            session = json.load(f)
        
        # Update state with session data
        state['last_updated'] = datetime.now().isoformat()
        
        # Update performance metrics if available
        if 'test_results' in session:
            # This is a simplified update - expand as needed
            if session['test_results']['actual'] > 0:
                state['performance_metrics']['7d_avg_retrieval'] = session['test_results']['actual']
    
    # Save updated state
    with open(state_path, 'w') as f:
        json.dump(state, f, indent=2)
    
    print(f"Coach state updated at {datetime.now()}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        update_state(sys.argv[1])
    else:
        print("Usage: python scripts/update_coach_state.py <session_log_path>")
