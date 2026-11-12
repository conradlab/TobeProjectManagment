# Mentorship Workflow

This document describes how mentors and you will work together during this internship.

## Weekly Process

### 1. Mentor Prepares (Before the week)

Your mentors will:
- [ ] Review your progress from the previous week
- [ ] Prepare the week's tasks and Issue
- [ ] Gather any needed resources or links
- [ ] Post the week's Issue with clear requirements
- [ ] Verify you can access necessary tools

### 2. You Read & Clarify (Start of week)

You should:
- [ ] Open the week's Issue and read it completely
- [ ] Review the learning goals and prerequisites
- [ ] Check that you have access to required resources
- [ ] Ask clarifying questions if any task is unclear
- [ ] Review suggested resources

**Ask questions here—don't guess!** If anything seems ambiguous, post a comment before spending hours on the wrong thing.

### 3. You Work Through Tasks (Mid-week)

You should:
- [ ] Work through the checklist methodically
- [ ] Check off tasks as you complete them (click the checkbox)
- [ ] Document what you do in comments on the Issue
- [ ] Note any problems or blockers
- [ ] Take screenshots or save outputs when relevant
- [ ] Test that your work actually does what you think it does

**Leave progress comments.** Your mentors can see your progress through comments and checked boxes.

### 4. Document Results & Blockers (Before review)

You should:
- [ ] Summarize what you completed
- [ ] List any tasks that weren't finished and why
- [ ] Explain any blockers clearly (what were you trying to do, what went wrong, what error did you see?)
- [ ] Link to any pull requests or submitted code
- [ ] Answer the reflection questions at the end

Example comment:

```
### Week 01 Progress Summary

**Completed:**
- ✅ Verified OHSU account login
- ✅ Accessed OHSU email
- ✅ Sent introductory email to Eisa and Don
- ✅ Joined Microsoft Teams

**In Progress:**
- ⏳ Finding Conrad Lab Team channel (not yet visible to me)

**Blocked:**
- ❌ GitHub access verification — When I try to open conradlab/TobeProjectManagment, 
  I get a "404 Not Found" error. Do I need a different permission level?

**Reflection:**
1. I learned how to access OHSU systems...
2. I found it confusing that...
3. I can now independently...
4. I still have questions about...

cc: @Eisa for review
```

### 5. Submit Code (When applicable)

If the week involves writing code or substantive documents:

- [ ] Create a feature branch: `git checkout -b week-XX-feature-name`
- [ ] Commit your changes with clear messages
- [ ] Push to GitHub: `git push origin week-XX-feature-name`
- [ ] Open a pull request
- [ ] Fill out the PR template (what changed, why, how tested, what you learned)
- [ ] Link the PR to the week's Issue by commenting "Closes #X"
- [ ] Request review from your mentor

Your mentors will:
- [ ] Review your code and comments
- [ ] Ask clarifying questions
- [ ] Suggest improvements
- [ ] Approve or request changes

### 6. Mentor Reviews (Mid-to-late week)

Your mentors will:
- [ ] Read your progress comments and pull requests
- [ ] Examine your deliverables
- [ ] Verify you understand the material (usually through conversation)
- [ ] Provide feedback and suggestions
- [ ] Answer your questions
- [ ] Identify any misconceptions to clear up

### 7. You Explain Your Learning

Your mentor may ask you to explain (verbally or in writing):
- What you did and why
- What you learned
- What confused you
- What you can now do independently
- What questions remain

**This is important.** Explaining your own understanding is how you cement learning.

### 8. Mentor Approves or Assigns Follow-up

Your mentor will:
- [ ] Mark the week as approved, or
- [ ] Request additional work or clarification, or
- [ ] Identify topics to revisit

You should **not** move to the next week until your mentor approves.

## Meeting Schedule

### Weekly Check-in (15-30 minutes)

**Frequency:** Once per week (usually Friday afternoon or early the following week)

**Purpose:**
- Review the week's progress
- Answer urgent questions
- Plan the next week
- Discuss any blockers

**Format:** In-person or video call, as arranged with your mentors

**What to have ready:**
- GitHub Issue with your week's progress
- Any code or documents you submitted
- List of blockers or questions
- Quick summary of what went well and what was hard

### Monthly Research Review (30-60 minutes)

**Frequency:** Approximately monthly (every 3-4 weeks)

**Purpose:**
- Discuss progress on research tracks
- Review scientific understanding
- Plan longer-term direction
- Discuss advanced topics

**Format:** In-person or video call with Eisa and Don

**What to have ready:**
- Summary of progress across all three tracks
- SATINN learning and findings
- Independent research progress
- Questions or concerns

## Communication Expectations

### Response Times

**Urgent blockers:** 24 hours
**Regular questions:** 24-48 hours
**Non-blocking discussion:** By next weekly meeting

### How to Notify Mentors

Use GitHub Issues and pull requests (leave no notification outside the repo if possible):

- Comment on an Issue and mention `@Eisa` or `@ConradLab`
- Use clear, descriptive language
- Include error messages or relevant context
- Be specific: "It broke" is less helpful than "When I run `python train.py`, I get `KeyError: 'model'`"

### What Mentors Expect to Hear

Each week, mentors should see:

- [ ] Progress on the week's checklist
- [ ] Comments documenting what you did
- [ ] Attempted tasks (even if stuck)
- [ ] Specific questions or blockers
- [ ] Reflection on your learning
- [ ] Submitted code or work for review (when applicable)

Mentors will **not** expect:

- ❌ Completed work without any evidence of learning
- ❌ Tasks marked done without evidence they were actually completed
- ❌ Silence until the end of the week (check in regularly!)
- ❌ Perfection (mistakes and questions are normal)

## If You're Stuck

**When you encounter a problem:**

1. **Try independent troubleshooting first (30 minutes max):**
   - Re-read the guide or documentation
   - Try a similar but slightly different approach
   - Look for error messages online
   - Ask if you can reframe the problem

2. **If still stuck, ask for help:**
   - Create a [Blocker Issue](../.github/ISSUE_TEMPLATE/blocker.yml)
   - Include: What were you trying to do? What went wrong? What's the exact error?
   - Your mentors will help within 24 hours

3. **In the meantime, move on:**
   - Skip that task and do the next one
   - Work on a different week's stretch activities
   - Document your questions for the weekly check-in
   - Don't wait idle for a response

## Expectations for Mentors

Your mentors will:

- [ ] Provide clear, achievable tasks each week
- [ ] Be available for questions (not instantly, but regularly)
- [ ] Give constructive feedback on your work
- [ ] Celebrate progress and learning
- [ ] Adjust the curriculum if needed
- [ ] Help when you're stuck
- [ ] Challenge you appropriately (not too easy, not impossible)
- [ ] Respect that you have other commitments

Your mentors are also busy researchers. They'll do their best, but sometimes response times are longer during conference season or heavy deadlines.

## Expectations for You

Your mentors expect:

- [ ] Genuine effort on tasks (perfection not required)
- [ ] Regular progress updates (don't go silent)
- [ ] Specific questions (not vague "I don't understand")
- [ ] Independent troubleshooting before asking (show you tried)
- [ ] Honesty about what you understand and don't
- [ ] Respect for their time (avoid "urgent" non-emergency requests)
- [ ] Willingness to learn from feedback

Mentors do **not** expect:

- ❌ Perfection or mastery
- ❌ Working 60-hour weeks (this is 4-6 hours/week)
- ❌ Already knowing how to do everything
- ❌ Understanding everything immediately
- ❌ AI-generated work you can't explain

## Adjusting the Pace

If a week is:

**Too hard:** Let your mentors know. They can:
- Slow down, break it into smaller steps
- Provide more resources
- Extend the deadline
- Adjust the scope

**Too easy:** You can:
- Work through the stretch activities
- Dive deeper into topics
- Start planning next week early
- Help refine the curriculum

The pace should be **challenging but achievable**. Speak up if it's not.

## Long-Term Perspective

This 12-week program is the beginning, not the end.

Your mentors' goal is to develop you into an independent researcher. This means:

- Early weeks will have detailed checklists (scaffolding)
- Later weeks will have more open-ended research tasks
- By Week 12, you should be able to tackle problems independently
- After Week 12, you'll continue with less structured guidance

You'll gradually take on more responsibility and fewer step-by-step instructions.

---

## Summary

✅ **Mentors prepare** clear, achievable tasks  
✅ **You read and clarify** before starting work  
✅ **You document progress** throughout the week  
✅ **You submit work** for review  
✅ **Mentors give feedback** and approve progress  
✅ **You reflect** on your learning  
✅ **You communicate** blockers and questions  
✅ **Together, you adjust** pace and scope as needed

The goal is partnership: mentors are here to help you grow as a researcher.

