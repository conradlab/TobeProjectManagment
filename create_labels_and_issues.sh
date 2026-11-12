#!/bin/bash

echo "Creating labels..."

# Track labels
gh label create "track:foundations" --color "0075ca" --description "Computational Foundations (Weeks 1-3)"
gh label create "track:satinn" --color "a2eeef" --description "SATINN Research (Weeks 5-12)"
gh label create "track:independent-research" --color "ffd700" --description "Independent Research Proposal"

# Type labels
gh label create "type:learning" --color "cccccc" --description "Skill-building tasks"
gh label create "type:research" --color "84b6eb" --description "Research and analysis"
gh label create "type:infrastructure" --color "e99695" --description "System setup and tools"
gh label create "type:documentation" --color "d4c5f9" --description "Writing guides or docs"
gh label create "type:blocker" --color "ff6b6b" --description "Problems blocking progress"

# Priority labels
gh label create "priority:high" --color "b60205" --description "Must complete this week"
gh label create "priority:medium" --color "fbca04" --description "Important but flexible"
gh label create "priority:low" --color "0e8a16" --description "Optional or stretch content"

# Review labels
gh label create "review:needed" --color "fc2929" --description "Awaiting mentor review"
gh label create "review:approved" --color "0e8a16" --description "Mentor has approved"

echo "Creating milestones..."

# Create milestones
gh milestone create --title "Foundational Onboarding (Weeks 1-3)" --description "Institutional access, Linux, Python, Git"
gh milestone create --title "Scientific & ML Foundations (Weeks 4-6)" --description "ML fundamentals, SATINN study, reproducibility"
gh milestone create --title "Python Research Development (Weeks 7-10)" --description "Architecture design, implementation, validation"
gh milestone create --title "Research Review & Next Steps (Weeks 11-12)" --description "Alternative approaches, presentation, next-phase planning"

echo "Labels and milestones created!"
