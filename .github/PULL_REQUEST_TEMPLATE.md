# Pull Request

## What Changed?

Describe what you modified in this pull request. Be specific about:
- Files you changed
- Features you added
- Bugs you fixed
- Documentation you updated

Example:
```
Added Python script for data preprocessing:
- Created `preprocess.py` to normalize image data
- Added `requirements.txt` with dependencies (numpy, scipy)
- Updated README with usage instructions
```

## Why Was the Change Needed?

Explain the motivation. What problem does this solve?

Example:
```
Week 03 required implementing a Python script to demonstrate
understanding of virtual environments and package management.
This script reads raw data files and normalizes them for analysis.
```

## How Was It Tested?

Describe what you did to verify the change works correctly.

Example:
```
Tested locally:
- Created virtual environment: `python3 -m venv venv`
- Installed dependencies: `pip install -r requirements.txt`
- Ran script on sample data: `python preprocess.py sample.csv`
- Verified output file was created and had expected format
```

## What Did You Learn?

Reflect on what this work taught you. What concepts do you now understand better?

Example:
```
I learned:
- How virtual environments isolate Python packages
- The importance of documenting dependencies in requirements.txt
- How to handle CSV files with pandas
- Why testing small changes frequently prevents big errors
```

## Any Known Limitations or Open Questions?

Be honest about what's not perfect or what you didn't understand fully.

Example:
```
Limitations:
- Currently handles only CSV files; could extend to other formats
- Doesn't validate input file structure; could add error checking
- Performance not tested on large datasets (>1GB)

Questions:
- Should I add type hints to the functions?
- Is there a standard way to handle missing values in images?
```

## Checklist

- [ ] Code follows PEP 8 style guidelines
- [ ] Comments explain complex logic
- [ ] I've tested this locally
- [ ] Relevant documentation is updated
- [ ] I can explain every line of this code
- [ ] No sensitive data (passwords, keys) committed
- [ ] Requested review from mentor

---

**Tip:** Smaller PRs are easier to review. If this PR touches many files, consider splitting it into multiple smaller PRs.
