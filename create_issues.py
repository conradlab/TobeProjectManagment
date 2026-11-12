#!/usr/bin/env python3
import subprocess
import json
import sys

REPO = "conradlab/TobeProjectManagment"

weeks_data = [
    {
        "num": 1,
        "title": "Institutional Onboarding",
        "labels": ["track:foundations", "priority:high", "type:learning"],
        "milestone": "Foundational Onboarding (Weeks 1-3)"
    },
    {
        "num": 2,
        "title": "Linux, SSH & Prime8",
        "labels": ["track:foundations", "priority:high", "type:learning"],
        "milestone": "Foundational Onboarding (Weeks 1-3)"
    },
    {
        "num": 3,
        "title": "Python, Git & GitHub",
        "labels": ["track:foundations", "priority:high", "type:learning"],
        "milestone": "Foundational Onboarding (Weeks 1-3)"
    },
    {
        "num": 4,
        "title": "Machine Learning Foundations",
        "labels": ["type:learning", "priority:high"],
        "milestone": "Scientific & ML Foundations (Weeks 4-6)"
    },
    {
        "num": 5,
        "title": "Understanding SATINN",
        "labels": ["track:satinn", "priority:high", "type:research"],
        "milestone": "Scientific & ML Foundations (Weeks 4-6)"
    },
    {
        "num": 6,
        "title": "SATINN Reproducibility",
        "labels": ["track:satinn", "priority:high", "type:research"],
        "milestone": "Scientific & ML Foundations (Weeks 4-6)"
    },
    {
        "num": 7,
        "title": "Design Modular Python Architecture",
        "labels": ["track:satinn", "priority:high", "type:learning"],
        "milestone": "Python Research Development (Weeks 7-10)"
    },
    {
        "num": 8,
        "title": "First Python Components",
        "labels": ["track:satinn", "priority:high", "type:learning"],
        "milestone": "Python Research Development (Weeks 7-10)"
    },
    {
        "num": 9,
        "title": "Model Interfaces & Baselines",
        "labels": ["track:satinn", "priority:high", "type:learning"],
        "milestone": "Python Research Development (Weeks 7-10)"
    },
    {
        "num": 10,
        "title": "Validation & Scientific Comparison",
        "labels": ["track:satinn", "priority:high", "type:research"],
        "milestone": "Python Research Development (Weeks 7-10)"
    },
    {
        "num": 11,
        "title": "Alternative Machine Learning Approaches",
        "labels": ["track:satinn", "priority:medium", "type:research"],
        "milestone": "Research Review & Next Steps (Weeks 11-12)"
    },
    {
        "num": 12,
        "title": "Presentation & Research Review",
        "labels": ["type:research", "priority:high"],
        "milestone": "Research Review & Next Steps (Weeks 11-12)"
    },
]

def issue_exists(week_num):
    """Check if issue for this week already exists"""
    result = subprocess.run(
        ["gh", "issue", "list", "--repo", REPO, "--state", "all", "--json", "number,title"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        issues = json.loads(result.stdout)
        for issue in issues:
            if f"Week {week_num:02d}" in issue['title']:
                return True
    return False

def create_issue(week):
    """Create a single week's issue"""
    week_num = week["num"]
    
    if issue_exists(week_num):
        print(f"✓ Week {week_num:02d} Issue already exists")
        return
    
    title = f"Week {week_num:02d}: {week['title']}"
    
    # Build issue body
    body = f"""## Weekly Objective

This is Week {week_num}: {week['title']}

**Why it matters:**
[Mentor: Add explanation of why this week is important]

## Plan

### Prerequisites
- [ ] Verify prerequisites from prior weeks

### Expected Time Commitment
- 4-6 hours this week (this is a planning estimate)

### Learning Objectives
1. [Learning objective 1]
2. [Learning objective 2]
3. [Learning objective 3]

### Resources
See [Learning Resources](../../docs/learning/learning-resources.md) for Week {week_num} links

## Execute

### Essential Tasks
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
2. How would you explain this to a friend?
3. What questions remain unanswered?
4. What are you most proud of from this week?

## Mentor Review

- [ ] All essential tasks completed
- [ ] Deliverable submitted and working correctly
- [ ] Student reflection answers demonstrate understanding
- [ ] Code (if applicable) is documented and understandable
- [ ] Any blockers were resolved or documented
- [ ] Approved for Week {week_num + 1 if week_num < 12 else 'completion'}

---

**Mentor:** Review and approve when complete.  
**Student:** Mark tasks as complete. Leave comments with progress and questions.
"""
    
    # Build label arguments
    label_args = []
    for label in week['labels']:
        label_args.extend(["--label", label])
    
    # Create issue
    cmd = ["gh", "issue", "create", "--repo", REPO, "--title", title, "--body", body]
    cmd.extend(label_args)
    cmd.extend(["--milestone", week['milestone']])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        # Extract issue number from output
        if "#" in result.stdout:
            issue_num = result.stdout.strip().split("#")[1].split(" ")[0]
            print(f"✓ Created Issue #{issue_num}: Week {week_num:02d}: {week['title']}")
        else:
            print(f"✓ Created Issue: Week {week_num:02d}: {week['title']}")
    else:
        print(f"✗ Failed to create Issue: Week {week_num:02d}")
        print(f"  Error: {result.stderr}")

# Create all issues
print("Creating weekly Issues...")
print()

for week in weeks_data:
    create_issue(week)

print()
print("✓ Weekly Issues created!")
