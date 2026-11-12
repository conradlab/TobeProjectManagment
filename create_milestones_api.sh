#!/bin/bash
# Create milestones using GitHub API

REPO="conradlab/TobeProjectManagment"

echo "Creating milestones via GitHub API..."

declare -a MILESTONES=(
    "Foundational Onboarding (Weeks 1-3)"
    "Scientific & ML Foundations (Weeks 4-6)"
    "Python Research Development (Weeks 7-10)"
    "Research Review & Next Steps (Weeks 11-12)"
)

for milestone in "${MILESTONES[@]}"; do
    # Check if exists
    existing=$(gh api repos/$REPO/milestones --jq ".[] | select(.title == \"$milestone\") | .title" 2>/dev/null)
    
    if [ "$existing" = "$milestone" ]; then
        echo "  ✓ Milestone '$milestone' already exists"
    else
        gh api repos/$REPO/milestones \
            -f title="$milestone" \
            -f description="" \
            2>&1 | grep -q "title" && echo "  ✓ Created milestone '$milestone'" || echo "  ✗ Failed to create '$milestone'"
    fi
done

echo "Done!"
