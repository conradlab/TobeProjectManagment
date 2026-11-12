# Learning Resources by Week

These are curated, verified resources to support each week of the curriculum. Links and recommendations will be updated as you progress.

## Week 01: Institutional Onboarding

**Accounts & Access**
- OHSU IT Support: (503) 494-4357
- OHSU Portal: https://my.ohsu.edu
- GitHub: https://github.com

**Learning Goal:** Get access, no deep technical content this week.

---

## Week 02: Linux, SSH & Remote Computing

**Linux Fundamentals**
- [Linux Journey](https://linuxjourney.com/) — Interactive, beginner-friendly
- [Linux Manual Pages](https://man7.org/) — Official command documentation
- [The Bash Academy](https://www.bash.academy/) — Shell scripting basics

**SSH & Remote Access**
- [SSH Essentials](https://www.digitalocean.com/community/tutorials/ssh-essentials-working-with-ssh-servers-clients-and-keys) — DigitalOcean guide
- [OpenSSH Manual](https://linux.die.net/man/1/ssh) — Official documentation

**Terminal Multiplexing**
- [tmux Cheat Sheet](https://tmuxcheatsheet.com/) — Quick reference
- [Hamvocke's tmux Guide](https://www.hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/) — Tutorial

**Local Setup for Week 02**
- Windows users: Install [Git Bash](https://gitforwindows.org/) or [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/)
- Mac/Linux: Terminal is built-in
- Text editor: [VSCode](https://code.visualstudio.com/) (recommended), Sublime, or vim

---

## Week 03: Python, Git & GitHub

**Python Basics**
- [Official Python Tutorial](https://docs.python.org/3/tutorial/) — Comprehensive
- [Real Python Tutorials](https://realpython.com/) — Step-by-step (free articles)
- [Python for Beginners](https://www.python.org/about/gettingstarted/) — Overview

**Python Virtual Environments**
- [venv Documentation](https://docs.python.org/3/library/venv.html) — Official
- [Real Python on venv](https://realpython.com/python-virtual-environments-a-primer/) — Detailed guide

**Git & GitHub**
- [Official Git Documentation](https://git-scm.com/doc) — Comprehensive
- [GitHub Guides](https://guides.github.com/) — Official tutorials
- [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials) — Clear explanations
- [Pro Git Book](https://git-scm.com/book/en/v2) — Free, in-depth

**Tools**
- [Git](https://git-scm.com/downloads) — Version control
- [VSCode](https://code.visualstudio.com/) — Code editor with Git integration

---

## Week 04: Machine Learning Foundations

**Conceptual Understanding**
- [3Blue1Brown: Neural Networks](https://www.youtube.com/watch?v=aircAruvnKk) — Excellent visual intuition
- [Fast.ai: Practical Deep Learning](https://course.fast.ai/) — Accessible but rigorous
- [Google ML Crash Course](https://developers.google.com/machine-learning/crash-course) — Interactive

**Foundational Concepts**
- Supervised vs. unsupervised learning
- Classification vs. regression
- Training, validation, testing
- Overfitting and underfitting
- Confusion matrices and metrics

**Getting Hands-On**
- [Kaggle Learn](https://www.kaggle.com/learn) — Free micro-courses
- [scikit-learn](https://scikit-learn.org/) — Python ML library
- Datasets: [Iris Dataset](https://archive.ics.uci.edu/ml/datasets/iris), [MNIST](http://yann.lecun.com/exdb/mnist/)

**Note:** This week is foundational. Deep mathematics can wait; focus on intuition.

---

## Week 05: Understanding SATINN

**SATINN Publications**
- Your mentors will provide the exact papers to read
- Focus on: biological questions, data types, architecture, results

**Testis Histology (Biology Background)**
- [NIH: Male Infertility](https://www.nichd.nih.gov/health/topics/infertility/conditioninfo) — Overview
- Mentors can recommend specific resources

**Research Paper Reading**
- See: [docs/templates/paper-review.md](../templates/paper-review.md)
- Practice note-taking and summarization

**SATINN Repository**
- Public repo: https://github.com/conradlab/SATINN
- Review README, existing documentation, source code structure

---

## Week 06: SATINN Reproducibility

**Reproducibility Best Practices**
- [NIH: Reproducible Research](https://www.nih.gov/research-training/rigor-reproducibility)
- [The Turing Way: Reproducible Research](https://the-turing-way.netlify.app/reproducible-research/reproducible-research.html)

**Documentation**
- Keep detailed notes on software versions, parameters, results
- See: [docs/templates/experiment-log.md](../templates/experiment-log.md)

**Validation**
- Numerical comparison: exact vs. approximate agreement
- Visual comparison: plots and images
- Statistical measures appropriate for biological data

---

## Week 07: Modular Python Architecture

**Software Design**
- [Real Python: Clean Code](https://realpython.com/tutorials/python-intermediate/) — Intermediate topics
- [Design Patterns](https://refactoring.guru/design-patterns/python) — Common approaches
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID) — Scalable design

**Python Best Practices**
- [PEP 8](https://www.python.org/dev/peps/pep-0008/) — Style guide
- [PEP 257](https://www.python.org/dev/peps/pep-0257/) — Docstring conventions

---

## Week 08: First Python Implementation

**Testing**
- [pytest Documentation](https://docs.pytest.org/) — Testing framework
- [Real Python: Getting Started with Testing](https://realpython.com/python-testing/)

**Code Quality**
- [Pylint](https://www.pylint.org/) — Code analysis
- [Black](https://black.readthedocs.io/) — Code formatter
- [Mypy](https://mypy.readthedocs.io/) — Type checking

**Documentation**
- [Sphinx](https://www.sphinx-doc.org/) — Documentation generator
- Writing docstrings: [PEP 257](https://www.python.org/dev/peps/pep-0257/), [Google style](https://google.github.io/styleguide/pyguide.html)

---

## Week 09: Model Interfaces & Baselines

**API Design**
- [Real Python: APIs](https://realpython.com/tutorials/apis/)
- [Python Design Patterns: Strategy Pattern](https://refactoring.guru/design-patterns/strategy)

**Machine Learning Models**
- [scikit-learn](https://scikit-learn.org/) — For baseline models
- [PyTorch](https://pytorch.org/) — For deep learning (if needed)

---

## Week 10: Validation & Scientific Comparison

**Evaluation Metrics**
- [scikit-learn: Metrics](https://scikit-learn.org/stable/modules/model_evaluation.html)
- [Confusion Matrix](https://en.wikipedia.org/wiki/Confusion_matrix)
- [ROC Curves](https://en.wikipedia.org/wiki/Receiver_operating_characteristic)

**Biological Validation**
- Domain-specific metrics
- Sample-level splitting for independent data
- Mentors will recommend domain literature

---

## Week 11: Alternative Machine Learning Approaches

**Advanced Topics**
- [Transfer Learning](https://en.wikipedia.org/wiki/Transfer_learning)
- [Self-Supervised Learning](https://en.wikipedia.org/wiki/Self-supervised_learning)
- [Unsupervised Learning](https://scikit-learn.org/stable/modules/unsupervised_learning.html)

**Research Papers**
- Mentor-recommended papers on alternative approaches
- Use the paper review template: [docs/templates/paper-review.md](../templates/paper-review.md)

---

## Week 12: Presentation & Research Review

**Communication**
- [Effective Scientific Presentations](https://www.nature.com/articles/d41586-019-02606-4) — Nature article
- Practice explaining your work to non-experts

**Scientific Proposal Writing**
- See: [docs/research/specific-aims-guide.md](../research/specific-aims-guide.md)
- [NIH Specific Aims](https://grants.nih.gov/grants/how-to-apply-application-guide/format-and-instructions/format-instructions.pdf) — Official guide

---

## Cross-Cutting Resources

**Research Literature**
- [Google Scholar](https://scholar.google.com/) — Academic search
- [PubMed](https://pubmed.ncbi.nlm.nih.gov/) — Biomedical literature
- [bioRxiv](https://www.biorxiv.org/) — Preprints
- Your library may provide access to paywalled journals

**Data & Datasets**
- [Kaggle Datasets](https://www.kaggle.com/datasets) — Public datasets
- [UCI ML Repository](https://archive.ics.uci.edu/ml/) — Benchmark datasets
- [Zenodo](https://zenodo.org/) — Research data repository

**Professional Development**
- [The Turing Way](https://the-turing-way.netlify.app/) — Reproducible, ethical research
- [Code Review Best Practices](https://google.github.io/eng-practices/review/)

---

## How to Use These Resources

1. **Each week:** Review the resources listed for that week
2. **Start with the "must-read":** Listed first in each week
3. **Follow links:** Resources often link to other useful material
4. **Ask mentors:** If a topic is unclear, ask for clarification
5. **Add your own:** You'll discover great resources; share them!

---

## Updating This List

As you find helpful resources:
- Save them to a personal list
- Share with your mentors
- Discuss which should be added to the official curriculum

---

**Remember:** You don't need to read everything. These are options. Focus on what helps you learn and make progress on your weekly tasks.

