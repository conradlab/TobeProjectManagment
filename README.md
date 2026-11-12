# Tobe's Research Internship at the Conrad Lab

Welcome to your research internship project repository! This is where you'll track your learning, research progress, and development as a computational researcher at OHSU's Conrad Lab.

## What This Repository Contains

This repository manages three interconnected learning tracks:

1. **Computational Foundations:** Linux, Python, Git, and remote computing skills
2. **SATINN Research:** Understanding and reimplementing SATINN (Software for Analysis of Testis Images with Neural Networks) in Python
3. **Independent Research:** Developing your own scientific research proposal

## Your Role

As a high-school research intern, you'll:

- Master computational research tools and workflows
- Understand published research and existing code
- Build reproducible Python implementations
- Develop hypothesis-driven scientific thinking
- Learn to communicate research effectively

## Your Mentors

- **Don Conrad:** Principal Investigator, scientific direction, and SATINN expertise
- **Eisa:** Computational mentorship, programming, and research planning

## Quick Start

**First time here?** Start with these three steps:

1. Read the [ROADMAP.md](ROADMAP.md) to understand the 12-week structure
2. Open [Week 01: Institutional Onboarding](../../issues/1)
3. Work through the checklist and leave a progress comment when you're done

**Each week:**
- Open the corresponding issue (Week 02, Week 03, etc.)
- Complete the tasks and deliverables
- Document what you learned
- Ask questions if anything is unclear
- Wait for mentor review before moving to the next week

## Repository Organization

```
README.md                    ← You are here
ROADMAP.md                   ← 12-week overview
CONTRIBUTING.md              ← How to participate
SECURITY.md                  ← Important guidelines

docs/
  getting-started.md         ← How to set up your environment
  mentorship-workflow.md     ← Weekly process
  student-progress.md        ← Track your progress
  decision-log.md            ← Pending mentor decisions
  
  onboarding/
    institutional-access.md  ← OHSU access
    linux-basics.md          ← Linux fundamentals
    remote-computing.md      ← SSH and Prime8
    python-environments.md   ← Virtual environments
    tmux-guide.md            ← Terminal multiplexing
    git-github-guide.md      ← Version control
  
  learning/
    python-foundations.md    ← Python fundamentals
    machine-learning-foundations.md
    scientific-reproducibility.md
    research-computing-etiquette.md
    learning-resources.md    ← Curated links
  
  research/
    satinn-overview.md       ← What is SATINN?
    satinn-python-roadmap.md ← Implementation plan
    satinn-architecture.md   ← Technical architecture
    satinn-validation-plan.md
    independent-research.md  ← Your research project
    specific-aims-guide.md   ← How to write Specific Aims
  
  templates/
    weekly-progress.md       ← Fill this out each week
    learning-reflection.md   ← How to reflect on learning
    experiment-log.md        ← How to document experiments
    paper-review.md          ← How to review papers
    specific-aims-outline.md ← Template for research proposal
    mentor-review.md         ← What mentors look for

.github/
  ISSUE_TEMPLATE/
    weekly-task.yml          ← Template for weekly issues
    research-task.yml        ← Template for research work
    blocker.yml              ← How to report problems
  
  PULL_REQUEST_TEMPLATE.md   ← Template for code submissions
```

## The Three Tracks

### Track 1: Computational Foundations (Weeks 1-3)

Learn the tools you'll use as a research programmer:

- **Week 01:** Access OHSU systems and communicate with your team
- **Week 02:** Navigate Linux remotely and connect to Prime8 (the Conrad Lab's powerful compute server)
- **Week 03:** Write Python code and make your first GitHub contribution

### Track 2: SATINN Research (Weeks 5-12)

Understand and reimplement a published machine learning system:

- **Week 05:** Study SATINN publications and existing architecture
- **Week 06:** Reproduce the existing MATLAB implementation
- **Week 07:** Plan a modular Python redesign
- **Weeks 08-10:** Implement and validate Python components
- **Weeks 11-12:** Explore future research directions

### Track 3: Independent Research (Weeks 3-12)

Develop your own scientific research idea:

- **Weeks 3-4:** Define your research problem
- **Weeks 5-6:** Conduct a focused literature review
- **Weeks 7-8:** Formulate hypotheses and Specific Aims
- **Weeks 9-10:** Refine your approach and feasibility
- **Weeks 11-12:** Present your research proposal

## How to Report Progress

1. **Completed a task?** Leave a comment on the Issue with what you did
2. **Stuck on something?** Create a new Issue using the [Blocker template](../.github/ISSUE_TEMPLATE/blocker.yml)
3. **Writing code?** Submit a pull request and request mentor review
4. **Done with a week?** Add your reflection answers in the Issue comments
5. **Ready for review?** Comment `@Eisa` or `@ConradLab` to notify your mentors

## Weekly Schedule

Each week follows this pattern:

1. Mentor prepares the week's tasks
2. You read and clarify what's expected
3. You work through the checklist
4. You document results and blockers
5. You submit code via pull requests (when applicable)
6. Your mentor reviews your work
7. You explain what you learned in your own words
8. Your mentor approves the week or assigns follow-up work

**Time commitment:** About 4-6 hours per week (this is a planning estimate).

## Important Principles

- **Ask questions.** It's better to ask than to guess wrong.
- **Document your learning.** Write down what you discovered, what confused you, and what questions remain.
- **Verify your results.** Never trust output without checking it independently.
- **Break large tasks into small steps.** Reviewable contributions are easier to help with.
- **Understand all code you submit.** If an AI tool helped you, you must still understand and be able to explain every line.

## Reporting Problems

**Issue with institutional access?**
→ See [institutional-access.md](docs/onboarding/institutional-access.md)

**Stuck on a technical task?**
→ Create a new Issue using the [Blocker template](../.github/ISSUE_TEMPLATE/blocker.yml)

**Question about the curriculum?**
→ Comment on the relevant week's Issue

**Security concern?**
→ Review [SECURITY.md](SECURITY.md) and contact your mentors directly

## Learning Resources

- [Curated Learning Resources by Week](docs/learning/learning-resources.md)
- [Official Python Documentation](https://docs.python.org/)
- [Official Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Linux Manual Pages](https://man7.org/)

## Research Ethics & Security

This repository is **public**. Do not publish:

- Passwords or authentication codes
- SSH private keys
- Personal institutional identifiers
- Unapproved datasets or laboratory materials
- Health information or protected data

See [SECURITY.md](SECURITY.md) for detailed guidelines.

## Success Looks Like

By the end of 12 weeks, you should be able to:

- ✅ Log into institutional systems and communicate with your team
- ✅ Navigate Linux command line confidently
- ✅ Connect to Prime8 and run Python scripts remotely
- ✅ Understand machine learning fundamentals
- ✅ Understand SATINN's scientific goal and technical architecture
- ✅ Reproduce published results using existing code
- ✅ Design modular Python implementations
- ✅ Write tested, documented Python code
- ✅ Validate your implementations against reference behavior
- ✅ Formulate a coherent scientific research question
- ✅ Communicate technical and scientific ideas clearly

## What Happens Next?

After 12 weeks, your mentors will review your progress and decide on the next phase:

- Deepen SATINN Python development
- Refine and conduct your independent research
- Learn advanced topics
- Explore publication or presentation opportunities

---

**Ready to start?** Open [Week 01: Institutional Onboarding](../../issues/1) and begin!

For questions about this curriculum, contact **Eisa** or **Don Conrad**.


