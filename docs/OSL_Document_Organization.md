# OSL Document Organization Recommendation

## Proposed Final Structure

### `/docs/core/` (Permanent - Methodology)
Essential OSL methodology that rarely changes:
- V3_Core.md
- V3_Implementation_Guide.md
- V3_Decision_History.md

### `/docs/specifications/` (Permanent - Guardrails)
Critical specifications that protect learning integrity:
- OSL_AI_Boundaries.md
- OSL_Flashcard_Philosophy.md  
- OSL_Governance_Standards.md
- OSL_State_Schema.md
- OSL_Natural_Language_Balance.md
- OSL_Activation_Probe.md

### `/docs/guides/` (Permanent - User Experience)
How users interact with the system:
- OSL_User_Interaction_Guide.md
- OSL_Guardrails_Checklist.md
- OSL_Master_Reference_Guide.md

### `/docs/implementation/` (Semi-Permanent - Technical)
Technical implementation details:
- OSL_Automation_Spec.md
- OSL_Infrastructure_Spec.md
- OSL_Validation_Framework.md
- OSL_Parsing_Framework.md
- OSL_Concept_Map_Implementation.md
- OSL_Interleaving_Specification.md

### `/docs/archive/` (Historical)
Completed reconciliation documents:
- OSL_Implementation_Summary.md
- OSL_Reconciliation_Summary.md

## Why These Documents Should Be Permanent

### 1. They Serve Different Audiences

**For Learners:**
- OSL_User_Interaction_Guide.md (how to use)
- OSL_Guardrails_Checklist.md (daily reminders)

**For Developers:**
- OSL_Automation_Spec.md (build instructions)
- OSL_State_Schema.md (data structures)
- OSL_Master_Reference_Guide.md (when to reference what)

**For AI Systems:**
- OSL_AI_Boundaries.md (interaction rules)
- OSL_Natural_Language_Balance.md (interpretation limits)
- OSL_Flashcard_Philosophy.md (generation restrictions)

**For Maintainers:**
- V3_Decision_History.md (why decisions were made)
- OSL_Governance_Standards.md (tuning guidance)

### 2. They Prevent Regression

Without these documents, future developers or AI systems might:
- Add AI features that bypass learning mechanisms
- Change thresholds without understanding impacts
- Modify flashcard creation in ways that break generation effect
- Create pre-reading assessments instead of minimal probes
- Allow AI to generate learning content

### 3. They Enable Consistent Implementation

Multiple implementations (CLI, web, mobile) need:
- Same governance thresholds
- Same AI boundaries
- Same state structures
- Same user experience patterns

## Maintenance Strategy

### Living Documents (Update Regularly)
- V3_Core.md - As methodology evolves
- OSL_State_Schema.md - Version with migrations
- OSL_Governance_Standards.md - Tune based on data

### Stable References (Update Rarely)
- OSL_AI_Boundaries.md - Core principles stable
- OSL_Flashcard_Philosophy.md - Research-based, stable
- OSL_Natural_Language_Balance.md - Principles stable

### Implementation Guides (Update with Features)
- OSL_Automation_Spec.md - As CLI evolves
- OSL_Infrastructure_Spec.md - As needs grow

## For the Implementing AI

**Your Reading Order:**
1. **OSL_Master_Reference_Guide.md** - Understand document map
2. **OSL_Automation_Spec.md** - Understand architecture
3. **OSL_AI_Boundaries.md** - Understand your limits
4. **OSL_State_Schema.md** - Understand data structures
5. Then reference others as needed per Master Reference Guide

**Your North Stars (Never Violate):**
- OSL_AI_Boundaries.md
- OSL_Flashcard_Philosophy.md
- OSL_Natural_Language_Balance.md

These three documents are your prime directives. They protect the learning system from well-intentioned but harmful automation.

## Recommendation

**Keep all documents permanent** but organize them by purpose. The cost of maintaining these documents is minimal compared to the cost of losing the knowledge they contain. They serve as:

1. **Guardrails** - Preventing harmful changes
2. **References** - Enabling consistent implementation
3. **Documentation** - Explaining decisions to future maintainers
4. **Training** - Onboarding new developers or AI systems

The only documents that could be archived are the reconciliation summaries, as they've served their purpose. Everything else has ongoing value.