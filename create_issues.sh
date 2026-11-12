#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Creating weekly GitHub Issues...${NC}"

# Week 01
gh issue create --title "[Week 01] Institutional Onboarding" --body "## Goal

Verify that you can access OHSU systems and communicate with your mentors.

**Expected Time:** 2-4 hours

## Why This Matters

Before diving into technical work, you need:
- Access to institutional communication systems
- A working GitHub account for code collaboration
- Contact information for your mentors

## Prerequisites

- OHSU NetID (should have been provided)
- Email account
- GitHub account (you should already have this)

## Required Tasks

- [ ] Verify OHSU account login works
- [ ] Complete multifactor authentication setup
- [ ] Access OHSU email
- [ ] Send an introductory email to Eisa and Don
- [ ] Access Microsoft Teams using your OHSU account
- [ ] Find and join the Conrad Lab team/channel
- [ ] Read existing lab communications as appropriate
- [ ] Send a brief introduction to the lab in Teams
- [ ] Verify your GitHub account
- [ ] Open this project repository on GitHub
- [ ] Accept collaborator invitation if provided
- [ ] Read the README.md completely
- [ ] Learn how GitHub Issues and checkboxes work
- [ ] Leave a progress comment on this Issue
- [ ] Confirm who to contact for institutional access problems
- [ ] Identify any onboarding/training still pending

## Deliverable

Verified onboarding checklist and introductory communication to mentors.

## Definition of Done

- [ ] You can access OHSU email, Teams, and GitHub
- [ ] Mentors know who you are and how to reach you
- [ ] You understand how to use this repository and GitHub Issues

## Resources

- [Institutional Access Guide](../docs/onboarding/institutional-access.md)
- [Getting Started Guide](../docs/getting-started.md)
- OHSU IT Support: (503) 494-4357

## Reflection

At the end of Week 01, answer these questions in a comment:

1. What did I learn?
2. What did I find difficult?
3. What can I now do independently?
4. What questions remain?

## Mentor Review Checklist

- [ ] Student demonstrated successful access to all systems
- [ ] Introductory communication verified
- [ ] Student understands how to use Issues and GitHub
- [ ] Week approved or additional tasks identified

---

Ready to start? Begin with the [Institutional Access Guide](../docs/onboarding/institutional-access.md)." --label "track:foundations,type:infrastructure,priority:high" --milestone "Foundational Onboarding (Weeks 1-3)"

echo -e "${GREEN}✓ Week 01 created${NC}"

# Week 02
gh issue create --title "[Week 02] Linux, SSH & Prime8" --body "## Goal

Become comfortable navigating Linux remotely and connecting to Prime8.

**Expected Time:** 4-6 hours

## Why This Matters

Prime8 (Conrad Lab's compute server) runs Linux. To use it effectively, you need to:
- Understand Linux file systems and commands
- Use SSH to connect securely to remote systems
- Use tmux to manage long-running jobs

These skills are essential for all computational research.

## Prerequisites

- Week 01 completed
- OHSU account access confirmed
- SSH key setup with your mentors (if not done, ask!)

## Required Tasks

- [ ] Understand what Linux is and why it's used in research
- [ ] Learn basic navigation commands (pwd, ls, cd, mkdir)
- [ ] Understand local vs. remote computing
- [ ] Learn what SSH does and how it works
- [ ] Understand SSH public/private key concepts
- [ ] Learn safe SSH key management
- [ ] Verify authorization for remote access
- [ ] Connect to the approved institutional gateway
- [ ] Connect from gateway to Prime8
- [ ] Confirm hostname of Prime8
- [ ] Check your username and current directory
- [ ] Learn directory permissions and ownership
- [ ] Locate the Conrad Lab shared directory
- [ ] Obtain mentor approval for a personal working directory
- [ ] Create your work directory on Prime8
- [ ] Organize directory structure (scripts, experiments, notes, outputs)
- [ ] Learn about disk usage and responsible storage
- [ ] Learn basic process monitoring (ps, top)
- [ ] Learn what tmux is and why it's useful
- [ ] Practice creating, detaching, reattaching tmux sessions

## Practical Exercise

On Prime8, practice:
1. SSH connection and basic commands
2. Creating a practice folder and files
3. Creating and managing a tmux session with multiple windows

## Deliverable

Screenshot or demonstration showing:
- Successful SSH connection to Prime8
- Proof of approved work directory creation
- Functioning tmux session with multiple windows/panes

## Definition of Done

- [ ] You can SSH to Prime8 independently
- [ ] You can navigate Linux file system confidently
- [ ] You can create and manage tmux sessions
- [ ] Work directory created and organized

## Resources

- [Linux Basics Guide](../docs/onboarding/linux-basics.md)
- [SSH & Remote Computing Guide](../docs/onboarding/remote-computing.md)
- [tmux Guide](../docs/onboarding/tmux-guide.md)
- [Learning Resources](../docs/learning/learning-resources.md)

## Reflection

At the end of Week 02, answer in a comment:

1. What did I learn?
2. What did I find difficult?
3. What can I now do independently?
4. What questions remain?

## Mentor Review Checklist

- [ ] Prime8 access verified
- [ ] Basic Linux commands demonstrated
- [ ] tmux functionality working
- [ ] Work directory structure approved
- [ ] Week approved or additional tasks identified

---

**Tip:** Don't memorize commands. Focus on understanding concepts and learning where to find help (man pages, Google, mentors)." --label "track:foundations,type:infrastructure,priority:high" --milestone "Foundational Onboarding (Weeks 1-3)"

echo -e "${GREEN}✓ Week 02 created${NC}"

# Week 03
gh issue create --title "[Week 03] Python, Git & GitHub" --body "## Goal

Write and test Python code, use version control, and make your first code contribution.

**Expected Time:** 4-6 hours

## Why This Matters

Python and Git are fundamental tools for computational research:
- **Python:** Write reproducible scientific programs
- **Git:** Track changes, collaborate with others, maintain history
- **GitHub:** Share code and receive feedback

## Prerequisites

- Week 01-02 completed
- Python 3 installed locally (Mac/Linux) or accessible on Prime8
- Git installed locally
- GitHub account ready

## Required Tasks

- [ ] Install Git locally (if not already done)
- [ ] Identify available Python installations
- [ ] Understand system Python vs. isolated environments
- [ ] Create a Python virtual environment with venv
- [ ] Activate and deactivate the environment
- [ ] Install a test Python package (like requests)
- [ ] Write a simple Python script (5-10 lines)
- [ ] Run it both locally and remotely
- [ ] Learn how package dependencies are documented
- [ ] Create a requirements.txt file
- [ ] Understand Git repositories and purpose
- [ ] Learn git status, git add, git commit, git log
- [ ] Learn about branches and pull requests
- [ ] Clone this project repository
- [ ] Create a small documentation contribution
- [ ] Create a feature branch for your work
- [ ] Submit a pull request with your changes
- [ ] Request mentor review
- [ ] Incorporate reviewer feedback
- [ ] Verify your changes merged successfully

## Practical Deliverable

Submit a pull request containing:
- A Python script you wrote
- A requirements.txt documenting dependencies
- Clear commit message explaining what changed and why
- Comments showing you understand the code

## Definition of Done

- [ ] Python virtual environment created and working
- [ ] Python script written and tested
- [ ] First pull request submitted and reviewed
- [ ] Code contribution merged successfully
- [ ] Comfortable with basic Git workflow

## Resources

- [Python Environments Guide](../docs/onboarding/python-environments.md)
- [Git & GitHub Guide](../docs/onboarding/git-github-guide.md)
- [Python Documentation](https://docs.python.org/3/)
- [GitHub Guides](https://guides.github.com/)
- [Learning Resources](../docs/learning/learning-resources.md)

## Reflection

Answer in a comment:

1. What did I learn about Python environments?
2. What was confusing about Git/GitHub?
3. What can I now do independently?
4. What questions remain?

## Mentor Review Checklist

- [ ] Python code is readable and works
- [ ] Virtual environment properly documented
- [ ] Git workflow understood (branching, commits, PR)
- [ ] Code demonstrates learning, not just copying
- [ ] PR feedback addressed appropriately
- [ ] Week approved or additional tasks identified

---

**Remember:** Focus on understanding, not perfection. Your first code won't be elegant, and that's completely normal." --label "track:foundations,type:learning,priority:high" --milestone "Foundational Onboarding (Weeks 1-3)"

echo -e "${GREEN}✓ Week 03 created${NC}"

