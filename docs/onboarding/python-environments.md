# Python Environments & Virtual Environments

Python can have many different versions and libraries installed. Virtual environments let you create isolated, reproducible Python setups for each project.

## What's a Virtual Environment?

A **virtual environment** is a self-contained Python installation:

- Different from your system Python
- Has its own packages
- Doesn't affect other projects or system tools
- Easy to recreate later
- Reproducible: document what's installed, recreate it anywhere

**Why use them?**
- Project A needs NumPy 1.19, Project B needs NumPy 1.23
- Don't want one project's packages breaking another
- Can cleanly test new packages without breaking existing setup
- Can document exactly what's needed (reproducibility)

## Creating a Virtual Environment (venv)

Python 3.3+ includes `venv` built-in. Use it like this:

```bash
# Create a virtual environment in folder called 'venv'
python3 -m venv venv

# This creates a folder with:
# venv/bin/python       ← Isolated Python
# venv/bin/pip          ← Isolated package manager
# venv/lib/python3.x/   ← Isolated packages
```

## Activating a Virtual Environment

Before using the environment, you must **activate** it:

```bash
# On Linux/Mac:
source venv/bin/activate

# On Windows (PowerShell):
venv\Scripts\Activate.ps1

# On Windows (Command Prompt):
venv\Scripts\activate.bat
```

**How to tell if activated:**
- Your terminal prompt shows `(venv)` at the start
- `which python` shows path inside `venv/` folder
- `python --version` matches what you expect

## Installing Packages

Once activated, use `pip` to install packages:

```bash
# Activate first (if not already)
source venv/bin/activate

# Install a package
pip install numpy

# Install a specific version
pip install numpy==1.23.0

# Install multiple packages
pip install numpy scipy scikit-learn

# Upgrade a package
pip install --upgrade numpy

# List installed packages
pip list
```

## Saving Your Environment (requirements.txt)

Always document what packages you're using:

```bash
# Generate a list of packages
pip freeze > requirements.txt

# This creates a file with:
# numpy==1.23.0
# scipy==1.9.1
# scikit-learn==1.1.3
```

**Later, recreate the exact environment:**

```bash
# In a new virtual environment on a different computer
pip install -r requirements.txt
```

This ensures reproducibility.

## Deactivating

When done working, deactivate the environment:

```bash
deactivate

# Prompt returns to normal (no more (venv) prefix)
```

**Important:** Deactivating doesn't delete anything. Your code and packages are still there. Deactivating just switches back to your system Python.

## Common Workflow

```bash
# 1. Create a folder for your project
mkdir my_research_project
cd my_research_project

# 2. Create a virtual environment
python3 -m venv venv

# 3. Activate it
source venv/bin/activate

# 4. Install packages you need
pip install numpy matplotlib scikit-learn

# 5. Save the list
pip freeze > requirements.txt

# 6. Write your Python code
# ... create script.py ...

# 7. Run your code
python script.py

# 8. When done for the day
deactivate

# 9. Next time, just activate (packages still there)
source venv/bin/activate
python script.py
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `python` not found | Use `python3` instead, or ensure activation |
| Import error: "No module named 'numpy'" | Make sure environment is activated; install package |
| Want to delete everything and start over | `rm -r venv/` then create new one |
| Different package versions on different computers | Use `requirements.txt` to match versions |

## Best Practices

✅ **Do:**
- Always use virtual environments for projects
- Keep `requirements.txt` in your repository
- Activate before installing or running code
- Name the environment `venv` (standard convention)

❌ **Don't:**
- Install packages to system Python (use virtual environment)
- Manually edit `requirements.txt` (use `pip freeze`)
- Commit the `venv/` folder to Git (it's huge; regenerate using `requirements.txt`)

## Practice Exercise

```bash
# Week 03 Exercise: Create and use a virtual environment

# 1. Create a new folder
mkdir python_practice
cd python_practice

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate it
source venv/bin/activate

# 4. Install a package
pip install requests

# 5. Create a simple script
cat > test_script.py << 'EOF'
import requests
print("Requests library version:", requests.__version__)
EOF

# 6. Run it
python test_script.py

# 7. Save the environment
pip freeze > requirements.txt

# 8. Check what was saved
cat requirements.txt

# 9. Deactivate when done
deactivate
```

## Next Steps

- Create a virtual environment on Prime8 (Week 03)
- Install packages as you need them
- Always save with `pip freeze > requirements.txt`
- Destroy and recreate to verify reproducibility

## Additional Resources

- [Official venv documentation](https://docs.python.org/3/library/venv.html)
- [pip documentation](https://pip.pypa.io/)
- [Real Python: Virtual Environments](https://realpython.com/python-virtual-environments-a-primer/)

---

**Key Takeaway:** Virtual environments are your friend. Use them for every project, and your future self will thank you.

