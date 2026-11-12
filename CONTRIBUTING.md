# Contributing to This Project

This document explains how to participate in the internship program and contribute to the repository.

## Weekly Workflow

Each week has an associated GitHub Issue. Here's how to work with it:

### 1. Read Your Week's Issue

Open the corresponding Issue (Week 01, Week 02, etc.) and review:

- Learning objectives
- Why the material matters
- Prerequisite skills
- Specific tasks and checkboxes
- Suggested resources
- Estimated workload
- Practical deliverable
- Definition of "done"

### 2. Complete the Tasks

Work through the checklist items:

- [ ] Check off each task as you complete it (click the checkbox)
- Document what you did
- Ask questions if anything is unclear
- Note any blockers or difficulties

### 3. Document Your Work

Leave comments on the Issue describing:

- What you accomplished
- Any challenges you encountered
- Questions that came up
- Resources that helped you
- Links to any code you submitted

### 4. Submit Code (When Applicable)

If the week involves writing code:

1. Create a feature branch: `git checkout -b week-XX-task-name`
2. Write your code and commit it with clear messages
3. Push to GitHub: `git push origin week-XX-task-name`
4. Open a pull request
5. Link the PR to the week's Issue by commenting: "Closes #XX"
6. Request review from your mentor

Your pull request should include:

- A clear description of what changed
- Why the change was needed
- How it was tested
- What you learned
- Any limitations or open questions

### 5. Reflect on Your Learning

At the end of each week, answer the reflection questions in the Issue:

1. What did I learn?
2. What did I find difficult?
3. What can I now do independently?
4. What questions remain?

### 6. Wait for Mentor Review

Your mentors will:

- [ ] Examine your deliverable
- [ ] Verify you understand the material
- [ ] Provide feedback
- [ ] Identify follow-up tasks
- [ ] Approve the week or request additional work

Do not move to the next week without mentor approval.

## Using Issue Labels

Issues are labeled to help organize work:

**Track labels:**
- `track:foundations` - Computational Foundations (Weeks 1-3)
- `track:satinn` - SATINN Research (Weeks 5-12)
- `track:independent-research` - Your independent research proposal

**Type labels:**
- `type:learning` - Skill-building tasks
- `type:research` - Research and analysis tasks
- `type:infrastructure` - System setup tasks
- `type:documentation` - Writing guides or documentation
- `type:blocker` - Problems blocking progress

**Review labels:**
- `review:needed` - Awaiting mentor review
- `review:approved` - Mentor has approved

**Priority labels:**
- `priority:high` - Must complete this week
- `priority:medium` - Important but somewhat flexible
- `priority:low` - Optional or stretch content

## Creating Issues for Blockers

If you get stuck or have a problem:

1. Use the [Blocker template](../.github/ISSUE_TEMPLATE/blocker.yml)
2. Describe the problem clearly
3. Include any error messages or unexpected behavior
4. Link to related Issues if applicable
5. Label it `type:blocker`

Your mentors will respond to blockers quickly.

## Code Standards

### Python Code

- Write readable, commented code
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Include docstrings for functions and classes
- Test your code before submitting
- Document any dependencies or special requirements

### Documentation

- Use clear, direct language
- Define technical terms when first used
- Include examples where helpful
- Link to relevant resources
- Proofread for typos and clarity

### Commit Messages

Write clear commit messages:

```
Short description of what changed (50 characters or less)

More detailed explanation if needed. Explain what changed
and why. Mention the related Issue number: "Closes #5"
```

Example:
```
Add Python virtual environment guide for Week 03

Explains how to create, activate, and use venv.
Includes common troubleshooting steps.
Closes #3
```

## Asking Questions

**Good places to ask questions:**

1. In the comments of the week's Issue
2. In a pull request review
3. By creating a Blocker Issue

**Please include:**

- What you're trying to do
- What you've already tried
- The exact error message or unexpected behavior
- Links to any relevant documentation

**Be specific:** "It doesn't work" is harder to help with than "When I run `python script.py`, I get `ModuleNotFoundError: No module named 'numpy'`"

## Submitting Research Work

For research tasks (literature reviews, analysis, proposals):

1. Create a document (Markdown in the repo or a shared format)
2. Submit a pull request or comment with a link
3. Request mentor review with `@Eisa` or `@ConradLab`
4. Address feedback
5. Wait for approval before finalizing

## Scientific Integrity

- Be honest about what you did and didn't understand
- Document limitations in your work
- Distinguish between confirmed results and speculation
- Verify your conclusions independently
- Cite sources for ideas and information
- If you used an AI tool for code or writing, you must understand and be able to explain every part

## Time Management

Each week should take approximately 4-6 hours:

- Spend about 1 hour reading materials and understanding tasks
- Spend 3-4 hours on practical work
- Spend 1 hour documenting and reflecting

If a week is taking significantly longer:

1. Check that you understand the task
2. Ask for clarification
3. Create a Blocker Issue if something is unclear
4. Your mentors may adjust the scope

If you finish early:

- Review the stretch activities in the Issue
- Dive deeper into learning resources
- Start planning the next week
- Help refine documentation

## Respect for Shared Resources

Prime8 is a shared research computer. Please:

- Monitor your CPU and memory usage
- Limit concurrent jobs
- Clean up temporary files
- Don't run unnecessary background processes
- Document what you're running
- Respect disk space limits
- Ask before making system-level changes

## Communication

**Weekly check-in:** 
- Schedule with your mentors
- Usually 15-30 minutes
- Review the week's progress
- Plan the next week
- Discuss blockers

**Monthly research review:**
- Deeper discussion of findings
- Mentor feedback on your work
- Adjustment of next-phase direction

**Asynchronous communication:**
- Leave comments on Issues for most questions
- Use `@Eisa` or `@ConradLab` to notify mentors
- Allow 24-48 hours for a response

## If Something Doesn't Make Sense

This curriculum was designed to be learnable, but it's also new. If something is:

- **Unclear:** Ask for clarification in the Issue comments
- **Too hard:** Create a Blocker Issue; mentors can adjust difficulty
- **Irrelevant:** Mention it in your reflection; mentors can adjust scope
- **Wrong:** Point it out; documentation can be improved

Feedback helps make this better for future interns.

---

## Summary

✅ Read your week's Issue carefully
✅ Work through tasks methodically  
✅ Document what you learn  
✅ Ask questions when stuck  
✅ Submit code and work for review  
✅ Reflect on your learning  
✅ Wait for mentor approval before moving forward  
✅ Respect shared resources  

Ready to start? Open [Week 01](../../issues/1)!

