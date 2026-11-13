## WEEK 06: SATINN Reproducibility and Reference Workflow

**Learning Objective:**
Locate the SATINN reference implementation, set up dependencies, execute the reference workflow on a demonstration dataset, and establish ground truth outputs for validation.

**Why This Week Matters:**
Before reimplementing SATINN in Python, you need a working reference: original code, training data, and known outputs. This week ensures you understand the exact computations SATINN performs and can reproduce them. It also identifies which dependencies and software licenses your Python implementation must support.

**Prerequisites:**
- SATINN conceptual understanding from Week 05.
- SSH access to Prime8 and Python environment from Week 02-03.
- Access to OHSU research data servers (may require additional permissions).
- MATLAB or alternative software if required by the reference implementation.

**Expected Time Commitment:**
12-14 hours (mostly waiting for data downloads and software installations)

**Learning Objectives:**
1. Locate the original SATINN code repository or codebase.
2. Document all software dependencies (versions, licenses).
3. Access the reference demonstration dataset.
4. Execute the complete SATINN reference workflow.
5. Capture and document reference outputs (accuracy metrics, output files).
6. Identify and document blockers or missing resources.
7. Create a reproducibility checklist for future reference.

---

## Plan

### Step 1: Locate SATINN Code and Data (2–3 hours)

- [ ] **Get SATINN code from mentors:**
  - Email Eisa and Don: "I am ready to work on the reference SATINN implementation. Can you provide: (1) Link to the original SATINN code (GitHub, internal server, or ZIP file), (2) Location of the demonstration dataset, (3) Documentation of dependencies."
  - Possible locations:
    - Public GitHub repository (check ConradLab organization).
    - OHSU internal GitLab or server.
    - ZIP file or cloud storage (Dropbox, Google Drive).
    - Archived code on Zenodo or figshare (if published).

- [ ] **Verify code access:**
  - If code is on GitHub: `git clone <url>` to your Prime8 work directory.
  - If code is in a ZIP: Download, extract, and navigate to the directory.
  - If code is on an OHSU server: Ask for the path and permissions required.

- [ ] **Examine the repository structure:**
  - Run: `find . -type f -name "*.md" -o -name "README*" -o -name "INSTALL*" | head -20`
  - Read any README, INSTALL, or CONTRIBUTING files.
  - Document the repository structure:
    ```
    satinn-ref/
      ├── src/              (source code)
      ├── data/             (example datasets)
      ├── results/          (expected outputs)
      ├── docs/             (documentation)
      ├── README.md
      └── requirements.txt  (dependencies)
    ```

- [ ] **Locate the demonstration dataset:**
  - Ask Eisa or Don: "Where is the reference dataset for testing SATINN?"
  - Possible locations:
    - In the code repository: `/data` or `/demo_data` directory.
    - On OHSU research data servers: `/data/satinn/demo` or similar.
    - Online resource: Zenodo, figshare, or publication supplementary data.
    - Size: May be large (1-10 GB); verify storage available on Prime8.

- [ ] **Download or copy the dataset:**
  - If on OHSU server: `cp -r /data/satinn/demo ~/work/satinn-project/reference_data`
  - If remote: `wget [URL]` or `curl -O [URL]` to download.
  - Verify file integrity: `md5sum` or `sha256sum` if checksums are provided.
  - Run: `du -sh reference_data` to confirm size downloaded correctly.

---

### Step 2: Catalog Dependencies (2–3 hours)

- [ ] **Identify all software requirements:**
  - Read the README or INSTALL file for explicit requirements.
  - Look for requirements files:
    - `requirements.txt` (Python packages)
    - `environment.yml` (Conda environment)
    - `Dockerfile` (containerized dependencies)
    - `MATLAB_requirements.txt` or similar (MATLAB toolboxes)
  - Search for comments in code: `grep -r "import\|require\|library" src/ | head -20`

- [ ] **Create a dependency inventory:**
  - File: `reference_dependencies.md`
  - Document:
    ```markdown
    # SATINN Reference Implementation Dependencies

    ## System Requirements
    - OS: Linux / macOS / Windows
    - Architecture: x86_64 / ARM
    - Storage: [Size] GB
    - RAM: [Minimum] GB
    - GPU: [Required/Optional] ([Model if specified])

    ## Programming Languages
    - Python: [Version, e.g., 3.8+]
    - MATLAB: [Version, e.g., R2021a+]
    - R: [If needed]

    ## Python Packages
    - numpy: [Version]
    - scipy: [Version]
    - scikit-image: [Version]
    - scikit-learn: [Version]
    - opencv-python: [Version]
    - matplotlib: [Version]
    - [Other packages]

    ## MATLAB Toolboxes (if applicable)
    - Image Processing Toolbox: [Version]
    - Computer Vision Toolbox: [Version]
    - Machine Learning Toolbox: [Version]
    - [Other toolboxes]

    ## External Tools
    - ImageMagick: [Version, for image conversion]
    - GraphViz: [Version, for visualization]
    - [Other tools]

    ## Licenses
    - MATLAB: [License type: Individual/Campus/Other]
    - Commercial libraries: [Any proprietary dependencies?]
    - Open source: [Licenses: MIT, Apache, GPL, etc.]

    ## Known Issues
    - [Any documented compatibility issues]
    - [OS-specific workarounds]
    ```

- [ ] **Test availability on Prime8:**
  - For each major dependency, verify it is installed:
    - `python3 --version`
    - `matlab -version` (if needed)
    - `apt list --installed | grep opencv` (Linux) or `brew list | grep opencv` (macOS)
    - `pip show numpy`
  - Document which tools are missing and need installation.

- [ ] **Request missing software:**
  - If MATLAB is not installed: Ask OHSU IT for access or explore alternatives (Octave, Python equivalents).
  - If Python packages are missing: Plan to install them: `pip install -r requirements.txt`
  - Document: "Can this workflow run with open-source tools only, or is MATLAB required?"

---

### Step 3: Install and Verify Environment (2–3 hours)

- [ ] **Set up a clean Python environment:**
  - SSH to Prime8: `ssh prime8`
  - Create a new virtual environment for the reference: `cd ~/work/satinn-project && python3 -m venv satinn-ref-env`
  - Activate: `source satinn-ref-env/bin/activate`

- [ ] **Install dependencies:**
  - If a `requirements.txt` exists in the reference code:
    - Run: `pip install -r satinn-ref/requirements.txt`
  - Or install manually:
    - Run: `pip install numpy scipy scikit-image scikit-learn opencv-python matplotlib pandas` (typical packages)
  - Verify each package:
    - `python -c "import numpy; print(numpy.__version__)"`
    - `python -c "import cv2; print(cv2.__version__)"`
  - Document the installed versions: `pip freeze > satinn-ref-versions.txt`

- [ ] **Verify the reference code can be imported:**
  - If code is organized as a Python module: `python -c "import satinn; print(satinn.__version__)"`
  - Or if running as scripts: Navigate to the code directory and list available scripts: `ls satinn-ref/src/*.py`
  - Test a simple import: `python -c "from satinn.preprocessing import normalize_image"` (adjust to actual module names)

- [ ] **Create a setup log:**
  - Document every step and any errors encountered:
    ```markdown
    # Reference Implementation Setup Log

    ## Date: [Today's date]
    ## Environment: Prime8, Python 3.9.7

    ### Steps Completed
    1. ✓ Code cloned from [URL]
    2. ✓ Virtual environment created
    3. ✓ Dependencies installed from requirements.txt
    4. ✓ All imports verified

    ### Issues Encountered
    - [Any errors and how they were resolved]

    ### Next Steps
    - [What needs to be done next]
    ```

---

### Step 4: Execute Reference Workflow (3–4 hours)

- [ ] **Prepare to run SATINN:**
  - Identify the entry point (main script, function, or executable):
    - Look for: `main.py`, `run.py`, `satinn.py`, or similar.
    - Read comments and docstrings to understand how to invoke it.
  - Check for command-line arguments: `python satinn-ref/main.py --help`
  - Understand the expected input and output formats.

- [ ] **Run SATINN on the demonstration dataset:**
  - Typical workflow:
    ```bash
    cd ~/work/satinn-project/satinn-ref
    source ../satinn-ref-env/bin/activate
    python main.py \
      --input ../reference_data/demo_image.tif \
      --output ../reference_outputs/demo_result.pkl \
      --config config.yaml
    ```
  - If the code is MATLAB-based: Consult with Eisa or Don on how to run it from the command line.
  - **Log the execution:**
    - Capture stdout and stderr: `python main.py [...] > execution_log.txt 2>&1`
    - Document running time (may take 10 minutes to several hours).

- [ ] **Monitor the execution:**
  - Use `tmux` (from Week 02) to keep the job running if it takes long:
    - `tmux new-session -s satinn-run`
    - Inside tmux: `cd ~/work/satinn-project && time python satinn-ref/main.py [...]`
    - Detach: `Ctrl+B d`
    - Check progress later: `tmux attach-session -s satinn-run`

- [ ] **Verify the output:**
  - Check that output files were created: `ls -lh ../reference_outputs/`
  - Verify file sizes are reasonable (not empty).
  - Check for output format:
    - Images: PNG, TIFF, HDF5
    - Data: CSV, JSON, PKL (pickle)
    - Metrics: Text file with accuracy, precision, recall
  - Open and inspect an output file: `python -c "import pickle; print(pickle.load(open('result.pkl', 'rb')))"`

---

### Step 5: Capture Reference Outputs and Metrics (2 hours)

- [ ] **Document output structure:**
  - For each output file, record:
    - File name and format
    - File size
    - Number of samples/images processed
    - Data type (array shape, value ranges)
  - Example:
    ```markdown
    ## Reference Outputs

    ### Output File 1: segmentation_map.tif
    - Format: TIFF (uint8)
    - Shape: (2048, 2048)
    - Value range: 0-255 (binary mask)
    - Meaning: Binary segmentation of tissue vs. background

    ### Output File 2: features.csv
    - Format: CSV (comma-separated)
    - Rows: 1250 (number of regions analyzed)
    - Columns: 48 (morphological, texture, spatial features)
    - Meaning: Quantitative features for each tissue region

    ### Output File 3: classification_results.json
    - Format: JSON
    - Keys: region_id, predicted_class, confidence
    - Classes: {0: 'normal', 1: 'abnormal'}
    - Meaning: Predicted tissue classification for each region
    ```

- [ ] **Extract and document metrics:**
  - If the reference outputs performance metrics (accuracy, F1-score, etc.):
    - Extract from output file or log.
    - Document in: `reference_metrics.txt`
    - Example:
      ```
      SATINN Reference Implementation Metrics (Demo Dataset)
      
      Overall Accuracy: 92.3%
      Precision (Normal): 91.5%
      Recall (Normal): 93.8%
      F1-Score (Normal): 92.6%
      Precision (Abnormal): 93.1%
      Recall (Abnormal): 90.7%
      F1-Score (Abnormal): 91.9%
      
      Processing time: 14 minutes 32 seconds for 1250 regions
      ```

- [ ] **Save reference outputs for comparison:**
  - Create a directory: `mkdir -p ~/work/satinn-project/reference_outputs_golden`
  - Copy all outputs: `cp reference_outputs/* reference_outputs_golden/`
  - These become your "golden" baseline for future Python implementation validation.

---

### Step 6: Document Blockers and Implementation Plan (2–3 hours)

- [ ] **List any unresolved issues:**
  - File: `reference_implementation_blockers.md`
  - Examples:
    ```markdown
    # Blockers and Issues

    ## Critical Blockers
    - [ ] MATLAB R2021a is not available on Prime8
      - Resolution: Contact OHSU IT or switch to Python/Octave equivalent
      - Impact: Cannot run reference implementation until resolved
    - [ ] Demo dataset exceeds Prime8 storage quota
      - Resolution: Request additional storage or download only required subset
      - Impact: Cannot execute workflow

    ## Non-Critical Issues
    - [ ] Documentation is sparse; had to read source code to understand parameters
    - [ ] Code assumes specific directory structure; needed to create symlinks
    - [ ] Warning: memory usage reaches 8 GB for large images

    ## Missing Information
    - [ ] No ground truth labels available for validation
    - [ ] Training data not included in demo; unclear if pre-trained model is used
    - [ ] Performance metrics not documented in README
    ```

- [ ] **Create an implementation roadmap:**
  - File: `python_implementation_roadmap.md`
  - Based on Week 05 SATINN understanding + Week 06 reference implementation experience:
    ```markdown
    # Python Implementation Roadmap

    ## Phase 1: Core Modules (Weeks 07-08)
    - [ ] Image preprocessing (color normalization, resizing)
    - [ ] Tissue segmentation (thresholding or simple classifier)
    - [ ] Basic feature extraction (morphological features only)

    ## Phase 2: Model Integration (Weeks 09-10)
    - [ ] Model loading and inference
    - [ ] Feature-to-prediction pipeline
    - [ ] Output formatting and visualization

    ## Phase 3: Validation (Weeks 10-11)
    - [ ] Comparison with reference outputs
    - [ ] Numerical tolerance testing
    - [ ] Alternative ML approaches

    ## Phase 4: Documentation & Demo (Week 12)
    - [ ] Complete README with setup instructions
    - [ ] Example notebook demonstrating workflow
    - [ ] Performance comparison with reference

    ## Known Challenges
    1. Feature extraction complexity (48 features × 1000+ regions)
    2. Floating-point precision matching reference implementation
    3. Memory efficiency for large images
    4. Reproducibility of model predictions
    ```

- [ ] **Identify implementation priorities:**
  - Ask Eisa or Don: "Which SATINN components are most critical? Should I prioritize accuracy or modularity?"
  - Document: "We will implement modules in this order: [list]"

---

### Step 7: Create Reproducibility Checklist (1 hour)

- [ ] **Document every resource needed:**
  - File: `reproducibility_checklist.md`
  - Content:
    ```markdown
    # SATINN Reproducibility Checklist

    ## Software
    - [ ] Python 3.8+ installed
    - [ ] Required packages installed (see requirements.txt)
    - [ ] MATLAB R2021a (if reference implementation requires)
    - [ ] All environment variables set correctly

    ## Data
    - [ ] Reference dataset downloaded to ~/work/satinn-project/reference_data
    - [ ] File integrity verified (checksums matched)
    - [ ] Dataset size: [Size] GB, available storage verified
    - [ ] Ground truth labels accessible

    ## Code
    - [ ] SATINN reference code cloned/downloaded
    - [ ] Code tested and imports verified
    - [ ] Entry point identified: main.py (or other)
    - [ ] Command-line arguments documented

    ## Execution
    - [ ] Run SATINN on reference dataset: SUCCESS / FAILURE
    - [ ] Execution time recorded: [Time]
    - [ ] Output files generated and verified
    - [ ] Metrics extracted and documented

    ## Validation
    - [ ] Reference metrics recorded: [Link to reference_metrics.txt]
    - [ ] Output files saved as golden baseline: [Location]
    - [ ] Known limitations documented: [Link to blockers file]

    ## To Reproduce (for future reference)
    1. Activate environment: source satinn-ref-env/bin/activate
    2. Navigate to code: cd satinn-ref
    3. Run: python main.py --input reference_data/demo.tif --output results.pkl
    4. Compare outputs with golden baseline in reference_outputs_golden/
    5. Verify metrics match reference_metrics.txt (within tolerance: ±0.5%)
    ```

- [ ] **Commit all documentation:**
  - Run: `git add reference_dependencies.md reference_metrics.txt reference_implementation_blockers.md python_implementation_roadmap.md reproducibility_checklist.md`
  - Run: `git commit -m "Week 06: Reference SATINN implementation, dependencies documented, metrics captured"`
  - Run: `git push origin main`

---

## Deliverable

Document your reproducibility work in a GitHub comment or document:

```markdown
**Week 06 Reproducibility Report**

- Reference SATINN code located and cloned: [Yes / No]
- Demonstration dataset downloaded/accessed: [Yes / No]
- Dependencies inventoried and documented: [Yes / No]
- All required software installed: [Yes / No]
- Reference workflow executed successfully: [Yes / No]
- Execution time recorded: [Minutes]
- Reference output files captured and stored: [Yes / No]
- Metrics documented (accuracy, precision, recall): [Yes / No]
- Blockers identified and mitigation planned: [Yes / No]
- Python implementation roadmap created: [Yes / No]
- Reproducibility checklist completed: [Yes / No]
```

---

## Objective Completion Criteria

✅ You have completed this week when:

1. You have located and cloned/downloaded the SATINN reference code.
2. You have documented all software dependencies (languages, packages, versions).
3. You have successfully installed the reference environment on Prime8.
4. You have accessed the demonstration dataset.
5. You have executed the complete SATINN workflow on reference data.
6. You have captured output files and recorded performance metrics.
7. You have identified and documented any blockers or missing resources.
8. You have created a clear roadmap for Python implementation.
9. You have created a reproducibility checklist for future reference.
10. You are ready to begin reimplementing SATINN in modular Python (Week 07).

---

## Student Reflection Questions

Answer in your report or in a GitHub comment:

1. **Reference Implementation:** What was the most surprising or challenging aspect of running the reference implementation?
2. **Dependencies:** Are there any dependencies that concern you for the Python reimplementation?
3. **Performance:** How long did the reference implementation take? Is this acceptable for practical use?
4. **Blockers:** What blockers did you encounter, and how did you resolve them?
5. **Implementation:** Based on what you've learned, where should you start the Python reimplementation?

---

## Mentor Review Checklist

- [ ] Tobe has located and successfully cloned the reference SATINN code.
- [ ] Tobe has documented all dependencies (software, packages, versions).
- [ ] Tobe has installed the reference environment without critical errors.
- [ ] Tobe has accessed and verified the demonstration dataset.
- [ ] Tobe has executed the reference workflow successfully.
- [ ] Tobe has captured and documented reference metrics.
- [ ] Tobe has identified blockers and proposed mitigation strategies.
- [ ] Tobe has created a clear implementation roadmap.
- [ ] Tobe's reproducibility checklist is complete and testable.
- [ ] Tobe is ready to begin Python modular implementation (Week 07).

---

## Optional Stretch Activities

- [ ] Run SATINN on a second dataset (if available) and verify consistent metrics.
- [ ] Create a Jupyter notebook demonstrating the reference workflow with visualizations.
- [ ] Document performance profiling (CPU/memory/time) for each pipeline step.
- [ ] Explore alternative open-source tools that might replace proprietary dependencies.
- [ ] Create a Docker container with all dependencies for reproducibility.

---

## Reporting a Blocker

If you cannot execute the reference workflow:

1. Verify all dependencies: `pip list | grep -E "numpy|scipy|opencv"`
2. Check data access: `ls -lh reference_data/` (confirm files exist)
3. Test imports: `python -c "from satinn import ..."`
4. Run with verbose output: `python main.py --verbose 2>&1 | tee debug.log`
5. Compare with mentor's execution: "Can you run this command on Prime8 and show me the output?"
6. Comment on this assignment with the error message and debug log.

---

## Links and Resources

- **SATINN GitHub (if public):** [Ask mentors for link]
- **Reference Data Location:** [Ask mentors for link]
- **Zenodo/figshare Archive (if published):** [Ask mentors for link]
- **OHSU Data Storage Guide:** https://www.ohsu.edu/research/high-performance-computing
- **Docker Guide for Reproducibility:** https://docs.docker.com/
- **Environment Reproducibility Best Practices:** https://packaging.python.org/guides/

---

## Related Epics

- **SATINN Research Track:** This week establishes ground truth for Python reimplementation (Weeks 07-12).
- **Research Computing:** Demonstrates best practices for reproducible science.
