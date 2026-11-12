# Git & GitHub Basics

Git is a version control system that tracks changes to code. GitHub is a platform for sharing and collaborating on code.

## Why Version Control?

Git solves real problems:

- **Track changes:** See what changed, when, and why
- **Undo mistakes:** Revert to previous versions
- **Collaboration:** Multiple people can work on the same project
- **Branching:** Experiment without breaking the main code
- **Documentation:** Commit messages explain the "why" behind changes

## Key Concepts

**Repository:** A folder with all your code and Git history
**Commit:** A snapshot of your code at a point in time
**Branch:** A parallel version of your code (e.g., "add-feature" branch)
**Pull Request:** A way to suggest changes and get review
**Merge:** Combining changes from one branch into another

## Basic Workflow

```bash
# 1. Clone a repository (download it)
git clone https://github.com/conradlab/TobeProjectManagment.git

# 2. Go into the folder
cd TobeProjectManagment

# 3. Check status
git status

# 4. Make changes (edit files)
# ... edit README.md ...

# 5. Check what changed
git status
git diff README.md

# 6. Stage changes (prepare to commit)
git add README.md

# 7. Commit (save snapshot)
git commit -m "Update README with new information"

# 8. Push (upload to GitHub)
git push origin main
```

## Important Commands

```bash
# See repository status
git status

# View changes made
git diff filename

# See commit history
git log

# Create and switch to a branch
git checkout -b feature-name

# Switch to existing branch
git checkout main

# Stage changes for commit
git add filename

# Commit with a message
git commit -m "Clear description of changes"

# Upload changes
git push origin branch-name

# Download latest changes
git pull origin main
```

## Branching (Safe Experimentation)

Always work in a branch, not directly on `main`:

```bash
# Create a new branch
git checkout -b week-03-learning

# Make changes, commit them
git add my_file.py
git commit -m "Add Python learning script"

# Push the branch
git push origin week-03-learning

# Later, create a Pull Request on GitHub to merge into main
```

**Why branches?**
- `main` is always stable
- Feature/experiment branches keep work isolated
- Easy to test before merging
- Team can review code before merge

## Commits & Commit Messages

A good commit message:
- Starts with what changed (verb + noun)
- Explains why, not what the code does
- Short first line (50 chars), longer explanation if needed

```bash
# Bad commit message
git commit -m "changes"

# Good commit message
git commit -m "Add data validation for user input

- Check that age is positive
- Reject empty strings
- Raise ValueError with helpful message
Fixes #15"
```

## Pull Requests (Getting Review)

When your code is ready for review:

1. Push your branch to GitHub
2. On GitHub, click "Create Pull Request"
3. Describe what changed and why
4. Mentors review and comment
5. Address feedback
6. Merge once approved

**Example PR description:**

```
## What Changed?

Added a Python script to process data files

## Why?

Automates the data preparation step (previously manual)

## How to Test?

```bash
python process_data.py sample_data.csv
# Should output processed_data.csv
```

## What I Learned

- How to use pandas for data processing
- Importance of error handling for malformed CSV files
```

## Merge Conflicts

If two people edit the same file:

```bash
# Git will report a conflict
git status

# Open the conflicted file, look for:
<<<<<<< HEAD
    my changes
=======
    their changes
>>>>>>> their-branch

# Choose which version to keep, save the file
# Then commit
git add file.py
git commit -m "Resolve merge conflict"
```

## .gitignore (What NOT to Track)

Create a `.gitignore` file to exclude files from Git:

```
# Don't track temporary files
*.pyc
__pycache__/
*.tmp

# Don't track venv
venv/

# Don't track secrets
.env
secrets.txt

# Don't track large data
*.csv
*.tar.gz
```

## Undoing Mistakes

```bash
# Undo uncommitted changes
git restore filename

# Undo last commit (keep changes)
git reset HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# View history after undoing
git log
git reflog
```

## Workflow for Week 03

```bash
# 1. Clone the project
git clone https://github.com/conradlab/TobeProjectManagment.git
cd TobeProjectManagment

# 2. Create a feature branch
git checkout -b week-03-python-learning

# 3. Write Python code
cat > my_script.py << 'EOF'
print("Hello, computational research!")
EOF

# 4. Test it
python my_script.py

# 5. Stage and commit
git add my_script.py
git commit -m "Add introductory Python script"

# 6. Push to GitHub
git push origin week-03-python-learning

# 7. On GitHub: Create a Pull Request
# (Visit GitHub, click "Create PR", describe changes)

# 8. Mentors review
# (They comment on your code, suggest improvements)

# 9. Address feedback
# (Edit files, commit, push—PR updates automatically)

# 10. Merge once approved
# (On GitHub, click "Merge Pull Request")
```

## Collaboration Best Practices

✅ **Do:**
- Work in branches
- Write clear commit messages
- Push frequently (daily)
- Pull before pushing
- Review code before merging
- Use `.gitignore` to exclude generated files

❌ **Don't:**
- Commit sensitive data (passwords, keys, credentials)
- Commit large files (> 100MB) without permission
- Force-push to main branch
- Edit others' commits without permission
- Skip code review (even for yourself)

## Common Mistakes & Fixes

| Mistake | Fix |
|---------|-----|
| Committed password | Tell mentors immediately; they can remove it |
| Wrong branch | `git reset HEAD~1` to undo, switch branch, recommit |
| Merge conflict | Edit file to choose correct version, commit |
| Committed large file | Use git-filter-branch or ask for help |

## Practice Exercise (Week 03)

```bash
# 1. Clone the repository
git clone https://github.com/conradlab/TobeProjectManagment.git
cd TobeProjectManagment

# 2. Create a branch
git checkout -b week-03-first-commit

# 3. Create a file with your name
echo "name: Tobe" > my_info.txt

# 4. Add and commit
git add my_info.txt
git commit -m "Add student information"

# 5. Push to GitHub
git push origin week-03-first-commit

# 6. Create PR on GitHub
# (Visit https://github.com/conradlab/TobeProjectManagment)
# (Click "Pull requests" then "New pull request")
# (Select your branch, describe changes, click "Create")

# 7. Request review from mentor
# (Comment @Eisa in the PR description)

# 8. Wait for feedback and address it
```

## Next Steps

- Set up Git locally (Week 03)
- Clone the repository
- Make your first commit
- Submit your first pull request
- Get feedback from mentors

## Additional Resources

- [Official Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials)
- [Pro Git Book](https://git-scm.com/book/en/v2) (free)

---

**Key Takeaway:** Git and GitHub are how modern research is done. Master these, and you can collaborate with researchers worldwide.

