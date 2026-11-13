## WEEK 03: Python, Git & GitHub Fundamentals

**Learning Objective:**
Master Python virtual environments, Git version control basics, and the GitHub workflow for collaborative code development with mentor code review.

**Why This Week Matters:**
Scientific computing in Python requires isolated environments to avoid dependency conflicts. Git and GitHub allow you to track changes, collaborate with mentors, and maintain a record of your work. These are essential professional practices for all research code.

**Prerequisites:**
- SSH access to Prime8 confirmed from Week 02.
- Work directory created at `~/work/satinn-project`.
- Access to the Conrad Lab GitHub repository with read and write permissions.
- Git installed on Prime8 (should be pre-installed; verify with `git --version`).

**Expected Time Commitment:**
10-12 hours

**Learning Objectives:**
1. Create and activate Python virtual environments to isolate project dependencies.
2. Use `pip` to install and manage Python packages reproducibly.
3. Understand Git branching, commits, and the feature branch workflow.
4. Create a GitHub pull request with meaningful commit messages.
5. Respond to mentor code review comments and iterate on feedback.
6. Document Python script functionality and execution requirements.

---

## Plan

### Step 1: Python Virtual Environments (2–3 hours)

- [ ] **Verify Python is installed on Prime8:**
  - SSH to Prime8: `ssh prime8`
  - Run: `python3 --version` (should print Python 3.8 or higher)
  - Run: `which python3` (should print something like `/usr/bin/python3`)
  - If Python is not found, ask Eisa or Don to request installation or request loading a module.

- [ ] **Understand virtual environments:**
  - Read: https://docs.python.org/3/tutorial/venv.html (first section: what is venv and why)
  - Key concept: A virtual environment is a self-contained Python installation with its own packages.
  - Without virtual environments, installed packages conflict across different projects.

- [ ] **Create your project virtual environment:**
  - Navigate to your work directory: `cd ~/work/satinn-project`
  - Run: `python3 -m venv venv` (creates a virtual environment in a subdirectory called "venv")
  - Run: `ls -la` to confirm "venv" directory was created.
  - Run: `source venv/bin/activate` (activates the virtual environment)
  - The shell prompt should now show `(venv)` at the start, indicating the virtual environment is active.

- [ ] **Verify the virtual environment is working:**
  - Run: `which python` (should print a path inside ~/work/satinn-project/venv)
  - Run: `python --version` (should print the same version as before)
  - Run: `pip list` (should show very few packages; only pip, setuptools, wheel)

- [ ] **Install your first packages:**
  - Run: `pip install numpy pandas matplotlib scikit-learn jupyter` (installs common data science packages)
  - Run: `pip list` to confirm the packages are installed.
  - Run: `python -c "import numpy; print(numpy.__version__)"` to confirm numpy works.

- [ ] **Create requirements.txt:**
  - Run: `pip freeze > requirements.txt` (exports installed packages to a file)
  - Run: `cat requirements.txt` to see the list (each line shows package==version)
  - Document: This file allows others (and future you) to recreate the exact environment with `pip install -r requirements.txt`.

- [ ] **Deactivate the virtual environment:**
  - Run: `deactivate` (exits the virtual environment)
  - The `(venv)` prefix should disappear from the prompt.
  - Run: `which python` (should now point to the system Python, not the one in venv)

---

### Step 2: Git Basics and Configuration (1–2 hours)

- [ ] **Verify Git is installed and configured:**
  - Run: `git --version` (should print `git version X.X.X`)
  - Run: `git config --global user.name "Your Full Name"` (configure your name)
  - Run: `git config --global user.email "your_netid@ohsu.edu"` (configure your email)
  - Run: `git config --list | grep user` to confirm your configuration.

- [ ] **Understand Git concepts:**
  - Read: https://www.atlassian.com/git/tutorials/what-is-git (first section)
  - Key concepts:
    - **Repository:** A directory containing a `.git` folder that tracks changes.
    - **Commit:** A snapshot of your code at a specific point in time.
    - **Branch:** An independent line of development (feature branch, main branch).
    - **Pull Request (PR):** A request to merge changes from one branch into another.

- [ ] **Clone the Conrad Lab repository:**
  - Navigate to your work directory: `cd ~/work/satinn-project`
  - Check if you already have the repository locally; if not, ask Eisa or Don for the clone URL.
  - Run: `git clone <repo_url>` (replace with the actual URL, e.g., `git@github.com:ConradLab/satinn-pipeline.git`)
  - Run: `cd satinn-pipeline` (enter the cloned repository directory)
  - Run: `git log --oneline -5` (view the last 5 commits)
  - Run: `git branch -a` (view all branches, including remote)

- [ ] **Understand the default branch:**
  - Run: `git status` (shows your current branch, usually `main` or `master`)
  - Document the default branch name for your repository.

---

### Step 3: Feature Branch Workflow (1–2 hours)

- [ ] **Create a feature branch for your first assignment:**
  - Ensure you are in the repository directory: `cd ~/work/satinn-project/satinn-pipeline`
  - Run: `git pull origin main` (fetch the latest changes from the main branch)
  - Run: `git checkout -b first-assignment-week03` (create and switch to a new branch)
  - Run: `git branch` to confirm you are on the new branch (should show `* first-assignment-week03`).

- [ ] **Make a meaningful code change:**
  - Create a simple Python script that demonstrates your understanding of the tools so far.
  - Run: `cd ~/work/satinn-project/satinn-pipeline` (ensure you are in the repo)
  - Run: `touch analyze_sample_data.py` (create a new Python file)
  - Edit the file (use `nano`, `vim`, or your preferred editor):
    ```python
    #!/usr/bin/env python3
    """
    Analyze sample data using pandas and numpy.
    
    This script loads sample data, computes basic statistics,
    and saves results to a CSV file.
    """

    import numpy as np
    import pandas as pd

    def load_sample_data():
        """Create a sample dataset for demonstration."""
        data = {
            'sample_id': ['S001', 'S002', 'S003', 'S004', 'S005'],
            'measurement_1': np.random.rand(5) * 100,
            'measurement_2': np.random.rand(5) * 100,
        }
        return pd.DataFrame(data)

    def analyze_data(df):
        """Compute basic statistics on the dataset."""
        stats = {
            'mean': df[['measurement_1', 'measurement_2']].mean(),
            'std': df[['measurement_1', 'measurement_2']].std(),
            'min': df[['measurement_1', 'measurement_2']].min(),
            'max': df[['measurement_1', 'measurement_2']].max(),
        }
        return stats

    def main():
        print("Loading sample data...")
        df = load_sample_data()
        print(f"Loaded {len(df)} samples")
        print(df)
        
        print("\nAnalyzing data...")
        stats = analyze_data(df)
        print("\nStatistics:")
        print(stats)
        
        print("\nSaving results...")
        results_df = pd.DataFrame(stats)
        results_df.to_csv('analysis_results.csv')
        print("Results saved to analysis_results.csv")

    if __name__ == '__main__':
        main()
    ```

- [ ] **Test your script:**
  - Ensure your virtual environment is activated: `source venv/bin/activate`
  - Run: `python analyze_sample_data.py`
  - Confirm the output shows the sample data and statistics.
  - Confirm a file `analysis_results.csv` was created.

---

### Step 4: Git Commits and Staging (1 hour)

- [ ] **Review your changes:**
  - Run: `git status` (shows unstaged changes)
  - Run: `git diff` (shows the exact changes in each file)

- [ ] **Stage your changes:**
  - Run: `git add analyze_sample_data.py` (stage the Python file)
  - Run: `git add analysis_results.csv` (stage the output file)
  - Run: `git status` (should show both files as "Changes to be committed")

- [ ] **Write a meaningful commit message:**
  - Run: `git commit -m "Add sample data analysis script with statistics computation"`
  - Run: `git log --oneline -3` to confirm the commit was recorded.

- [ ] **Understand commit message best practices:**
  - Good: "Add sample data analysis script with statistics computation"
  - Bad: "fixed stuff" or "update"
  - Good: "Fix memory leak in data preprocessing"
  - Bad: "blah"
  - Key: Describe *what* changed and *why*, not *how*.

---

### Step 5: Create and Review a GitHub Pull Request (2–3 hours)

- [ ] **Push your branch to GitHub:**
  - Run: `git push origin first-assignment-week03` (uploads your branch to GitHub)
  - Run: `git log --oneline -3` to confirm your commit is logged locally.

- [ ] **Create a pull request on GitHub:**
  - Open your browser and go to the GitHub repository (ask Eisa or Don for the link).
  - You should see a notification or button suggesting to create a PR from your newly pushed branch.
  - Click "Create Pull Request" or "Compare & pull request".
  - Fill in the PR title: "Week 03: Add sample data analysis script"
  - Fill in the PR description:
    ```markdown
    ## Summary
    This PR adds a Python script that demonstrates data analysis using pandas and numpy.

    ## Changes
    - Added `analyze_sample_data.py`: Generates sample data and computes statistics
    - Added `analysis_results.csv`: Output file from the script

    ## Testing
    - Ran the script locally: `python analyze_sample_data.py`
    - Confirmed CSV output is created correctly

    ## Related to
    Week 03 assignment in the research internship curriculum.
    ```
  - Click "Create Pull Request".

- [ ] **Share the PR link with your mentors:**
  - Copy the PR URL (e.g., `https://github.com/ConradLab/satinn-pipeline/pull/42`)
  - Share the link via email or Teams: "I have submitted my first PR. Please review at [URL]"
  - Mentors will review your code and may request changes.

- [ ] **Respond to mentor feedback:**
  - Check the GitHub PR for comments from Eisa or Don.
  - If they request changes:
    - Make the changes locally on your feature branch.
    - Commit the changes: `git add .` then `git commit -m "Address feedback: improve documentation"`
    - Push the updated branch: `git push origin first-assignment-week03`
    - The PR will automatically update with your new commits.
  - Reply to each comment on the PR (click "Reply" under their comment).
  - Once all feedback is resolved, mentors will approve and merge the PR.

- [ ] **Merge and clean up:**
  - Once the PR is approved, mentors may merge it, or you may be asked to merge it yourself.
  - After merging, run: `git checkout main && git pull origin main` to sync your local main branch.
  - Run: `git branch -d first-assignment-week03` to delete your local feature branch.

---

### Step 6: Document Your Work (1 hour)

- [ ] **Create a README for your project:**
  - Create a file: `~/work/satinn-project/README.md`
  - Content:
    ```markdown
    # Satinn Pipeline Development

    ## Project Setup

    ### Prerequisites
    - Python 3.8 or higher
    - Git

    ### Installation

    1. Clone the repository (if not already cloned):
       ```bash
       git clone <repo_url>
       cd satinn-pipeline
       ```

    2. Create and activate a virtual environment:
       ```bash
       python3 -m venv venv
       source venv/bin/activate
       ```

    3. Install dependencies:
       ```bash
       pip install -r requirements.txt
       ```

    ## Running Scripts

    ### Sample Data Analysis
    ```bash
    python analyze_sample_data.py
    ```
    Output: `analysis_results.csv`

    ## Weekly Assignments
    - Week 03: Created sample data analysis script with pandas/numpy integration.

    ## Notes
    - Always activate the virtual environment before running scripts.
    - Do not commit the `venv/` directory; it will be recreated from `requirements.txt`.
    ```

---

## Deliverable

Document your progress in a GitHub comment on this assignment or in a document:

```markdown
**Week 03 Progress Report**

- Virtual environment created and activated: [Yes / No]
- Python packages installed (numpy, pandas, matplotlib, scikit-learn): [Yes / No]
- requirements.txt generated: [Yes / No]
- Git configured with name and email: [Yes / No]
- Repository cloned to ~/work/satinn-project: [Yes / No]
- Feature branch created: [Yes / No]
- Sample data analysis script completed and tested: [Yes / No]
- Pull request created and shared: [GitHub PR URL]
- Mentor feedback addressed (if any): [Addressed / Pending]
- README.md documentation created: [Yes / No]
```

---

## Objective Completion Criteria

✅ You have completed this week when:

1. You can create and activate a Python virtual environment on Prime8.
2. You have installed packages using `pip` and created a `requirements.txt` file.
3. You understand Git basics: cloning, branching, committing, and pushing.
4. You have created a feature branch and made a meaningful code change.
5. You have successfully created a GitHub PR with a clear description.
6. You have responded to mentor feedback and iterated on your code.
7. Your PR has been approved and merged (or is ready for review).
8. You have documented the project setup in a README.

---

## Student Reflection Questions

Answer in a GitHub comment or your learning journal:

1. **Virtual Environments:** Why is it important to use a virtual environment rather than installing packages globally?
2. **Branching Strategy:** Why do we create a feature branch instead of committing directly to main?
3. **Commit Messages:** Look at your commit message. Does it clearly explain what changed and why?
4. **Code Review:** What feedback did your mentors give? How did you address it?
5. **Workflow:** What part of the Git/GitHub workflow is still confusing to you?

---

## Mentor Review Checklist

- [ ] Tobe has created a functional Python virtual environment on Prime8.
- [ ] Tobe has installed required packages and generated requirements.txt.
- [ ] Tobe has configured Git with correct name and email.
- [ ] Tobe has cloned the Conrad Lab repository successfully.
- [ ] Tobe has created a feature branch and committed meaningful changes.
- [ ] Tobe's sample data analysis script runs without errors.
- [ ] Tobe has created a GitHub PR with a clear description and tested output.
- [ ] Tobe has responded to code review feedback professionally.
- [ ] Tobe has created a project README with setup and execution instructions.
- [ ] Tobe's commit messages follow best practices.
- [ ] Approve Tobe to proceed to Week 04 (Machine Learning Foundations).

---

## Optional Stretch Activities

- [ ] Set up a `.gitignore` file to exclude venv/, __pycache__/, and .pyc files.
- [ ] Create a simple unit test for your analyze_data function using pytest.
- [ ] Add a configuration file (YAML or JSON) to make your script more flexible.
- [ ] Explore Git aliases: `git config --global alias.co checkout` to create shortcuts.

---

## Reporting a Blocker

If you cannot clone the repository or push to GitHub:

1. Verify you have GitHub SSH key configured: `ssh -T git@github.com`
2. Verify you have write access to the repository (ask Eisa or Don).
3. Verify your local `.git/config` has the correct repository URL: `cat .git/config`
4. If pushing fails, check your branch: `git branch` and try again: `git push origin branch-name`
5. Comment on this assignment with the error message and the step at which it fails.

---

## Links and Resources

- **Python Virtual Environments:** https://docs.python.org/3/tutorial/venv.html
- **Git Tutorial:** https://www.atlassian.com/git/tutorials
- **GitHub Pull Requests:** https://docs.github.com/en/pull-requests/collaborating-with-pull-requests
- **Commit Message Best Practices:** https://www.conventionalcommits.org/
- **Python Package Management:** https://docs.python.org/3/tutorial/venv.html#managing-packages

---

## Related Epics

- **SATINN Research Track:** All code development uses this Git/GitHub workflow.
- **Python Development:** Foundation for weeks 04-12.
