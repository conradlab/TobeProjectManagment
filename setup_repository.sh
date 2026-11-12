#!/bin/bash
# Initialize Tobe's research internship repository
# This script creates labels, milestones, and all 12 weekly Issues
# Safe to rerun - checks for existing items before creating

set -e

REPO="conradlab/TobeProjectManagment"
echo "Initializing repository: $REPO"
echo ""

# Verify gh CLI is available
if ! command -v gh &> /dev/null; then
    echo "ERROR: GitHub CLI (gh) not found. Install it: https://cli.github.com/"
    exit 1
fi

# Verify authentication
if ! gh auth status &> /dev/null; then
    echo "ERROR: Not authenticated with GitHub. Run: gh auth login"
    exit 1
fi

echo "✓ GitHub CLI authenticated"
echo ""

# === CREATE LABELS ===
echo "--- Creating Labels ---"

declare -a LABELS=(
    "track:foundations|0075ca|Computational Foundations (Weeks 1-3)"
    "track:satinn|a2eeef|SATINN Research (Weeks 5-12)"
    "track:independent-research|ffd700|Independent Research Proposal"
    "type:learning|cccccc|Skill-building tasks"
    "type:research|84b6eb|Research and analysis"
    "type:infrastructure|e99695|System setup and tools"
    "type:documentation|d4c5f9|Writing guides or docs"
    "type:blocker|ff6b6b|Problems blocking progress"
    "priority:high|b60205|Must complete this week"
    "priority:medium|fbca04|Important but flexible"
    "priority:low|0e8a16|Optional or stretch content"
    "review:needed|fc2929|Awaiting mentor review"
    "review:approved|0e8a16|Mentor has approved"
)

for label_def in "${LABELS[@]}"; do
    IFS="|" read -r name color description <<< "$label_def"
    
    # Check if label exists
    if gh label list --repo "$REPO" --limit 100 | grep -q "^$name"; then
        echo "  ✓ Label '$name' already exists"
    else
        gh label create "$name" \
            --repo "$REPO" \
            --color "$color" \
            --description "$description" 2>&1
        echo "  ✓ Created label '$name'"
    fi
done

echo ""

# === CREATE MILESTONES ===
echo "--- Creating Milestones ---"

declare -a MILESTONES=(
    "Foundational Onboarding (Weeks 1-3)"
    "Scientific & ML Foundations (Weeks 4-6)"
    "Python Research Development (Weeks 7-10)"
    "Research Review & Next Steps (Weeks 11-12)"
)

for milestone in "${MILESTONES[@]}"; do
    # Check if milestone exists
    if gh milestone list --repo "$REPO" | grep -q "$milestone"; then
        echo "  ✓ Milestone '$milestone' already exists"
    else
        gh milestone create "$milestone" --repo "$REPO" 2>&1
        echo "  ✓ Created milestone '$milestone'"
    fi
done

echo ""

# === CREATE WEEKLY ISSUES ===
echo "--- Creating Weekly Issues ---"

# Array of week data
declare -a WEEKS=(
    "1|Institutional Onboarding|track:foundations|priority:high"
    "2|Linux, SSH & Prime8|track:foundations|priority:high"
    "3|Python, Git & GitHub|track:foundations|priority:high"
    "4|Machine Learning Foundations|type:learning|priority:high"
    "5|Understanding SATINN|track:satinn|priority:high"
    "6|SATINN Reproducibility|track:satinn|priority:high"
    "7|Design Modular Python Architecture|track:satinn|priority:high"
    "8|First Python Implementation|track:satinn|priority:high"
    "9|Model Interfaces & Baselines|track:satinn|priority:high"
    "10|Validation & Scientific Comparison|track:satinn|priority:high"
    "11|Alternative Machine Learning Approaches|track:satinn|priority:medium"
    "12|Presentation & Research Review|type:research|priority:high"
)

for week_def in "${WEEKS[@]}"; do
    IFS="|" read -r week_num title label1 label2 <<< "$week_def"
    
    # Check if issue already exists (by title pattern)
    issue_title="Week $(printf "%02d" $week_num): $title"
    
    if gh issue list --repo "$REPO" --state all | grep -q "Week $(printf "%02d" $week_num)"; then
        echo "  ✓ Issue '$issue_title' already exists"
        continue
    fi
    
    # Create temporary issue body file
    issue_body="/tmp/week_${week_num}_issue.md"
    
    cat > "$issue_body" << 'WEEK_EOF'
## Weekly Objective

This is Week WEEK_NUM: WEEK_TITLE

**Why it matters:**
[Details about why this week's work is important will be added by mentor]

## Plan

### Prerequisites
- [ ] Verify prerequisites from prior weeks

### Expected Time Commitment
- 4-6 hours this week (provisional)

### Learning Objectives
1. First learning objective
2. Second learning objective
3. Third learning objective

### Resources
- See [Learning Resources](../docs/learning/learning-resources.md) for Week WEEK_NUM links

## Execute

### Tasks
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3
- [ ] Task 4

### Optional Stretch Tasks
- [ ] Stretch task 1
- [ ] Stretch task 2

## Deliverable

Describe what you will produce or demonstrate this week.

## Student Reflection

Answer these questions at the end of the week:

1. What was the most challenging concept this week?
2. What would you explain differently to a friend?
3. What questions remain unanswered?
4. What are you most proud of from this week?

## Mentor Review

- [ ] All essential tasks completed
- [ ] Deliverable submitted and working
- [ ] Student answers reflect understanding
- [ ] Code (if applicable) is documented
- [ ] Blockers resolved or documented
- [ ] Approved for next week

---

**Mentor:** Please review and approve when complete.
**Student:** Mark tasks complete as you finish them. Leave comments with progress.

WEEK_EOF
    
    # Replace placeholders
    sed -i "" "s/WEEK_NUM/$week_num/g" "$issue_body"
    sed -i "" "s/WEEK_TITLE/$title/g" "$issue_body"
    
    # Create the issue
    gh issue create \
        --repo "$REPO" \
        --title "$issue_title" \
        --body-file "$issue_body" \
        --label "$label1" \
        --label "$label2" \
        --label "type:learning" 2>&1 > /tmp/create_issue_output.txt
    
    # Extract issue number from output
    issue_num=$(grep -oP '#\K[0-9]+' /tmp/create_issue_output.txt | head -1)
    
    if [ -n "$issue_num" ]; then
        echo "  ✓ Created Issue #$issue_num: $issue_title"
    else
        echo "  ✗ Failed to create Issue: $issue_title (check output above)"
    fi
    
    rm -f "$issue_body"
done

echo ""
echo "✓ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Open https://github.com/$REPO"
echo "2. Verify all labels are present"
echo "3. Verify all milestones are created"
echo "4. Verify all 12 weekly Issues exist (Issues #1-#12)"
echo "5. Have mentors personalize each week's tasks"
echo ""
