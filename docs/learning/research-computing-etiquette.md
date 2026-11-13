# Research Computing Etiquette: Shared Resources and Best Practices

**Target Week:** Week 2  
**Learning Objective:** Use shared computing resources responsibly  
**Time Estimate:** 2 hours reading + setup  

## Introduction: Why Etiquette Matters

OHSU's Prime8 compute cluster runs research jobs from hundreds of users. Poor resource management can:
- Crash the cluster or freeze other researchers' work
- Get your account suspended
- Waste electricity and compute budget
- Create frustration across the lab and department

**Goal:** Learn to run computationally intensive SATINN jobs without disrupting others.

## Prime8 Cluster Basics

**Prime8** is OHSU's high-performance computing (HPC) cluster with:
- Multiple compute nodes (servers)
- Shared storage for data
- Job scheduling system (SLURM) to fairly allocate resources

### Key Resources

| Resource | Limit | Notes |
|----------|-------|-------|
| **CPU cores** | 64 per node | Typical node has 64 cores; don't request more than available |
| **Memory (RAM)** | 256 GB per node | Request in GB; default is ~2 GB per core |
| **Disk space** | 100 TB shared | Do not store personal files; only research data |
| **Wall time** | 24 hours typical | Jobs running >24h risk being killed |
| **GPU** | 4 GPUs per node (optional) | Reserved for GPU-intensive work |

### Login and Access

```bash
# SSH into Prime8 (from OHSU network or VPN)
ssh your_username@prime8.ohsu.edu

# List available compute nodes
sinfo

# Check your quota and usage
lfs quota /home/username
lfs df

# Navigate to your workspace
cd /data/users/your_username/
```

## Job Scheduling with SLURM

**SLURM** (Simple Linux Utility for Resource Management) queues jobs fairly.

### Submitting a Job

Create a job script (`run_satinn.sh`):

```bash
#!/bin/bash

#SBATCH --job-name=satinn_preprocessing
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --output=logs/satinn_%j.out
#SBATCH --error=logs/satinn_%j.err
#SBATCH --mail-user=your_email@ohsu.edu
#SBATCH --mail-type=END,FAIL

# Load required modules
module load python/3.10
module load cuda/11.8  # Only if using GPU

# Activate environment
source /data/users/your_username/satinn_env/bin/activate

# Run preprocessing on all images
python satinn/preprocess_images.py \
  --input-dir /data/datasets/testis_slides/raw \
  --output-dir /data/users/your_username/satinn_output \
  --num-workers 8 \
  --log-level INFO

# If finished successfully, notify
echo "SATINN preprocessing complete" | mail -s "Job completed" your_email@ohsu.edu
```

**Submit the job:**
```bash
sbatch run_satinn.sh
# Submitted batch job 45678
```

**Monitor the job:**
```bash
# Check all your jobs
squeue -u your_username

# Check job details
sinfo -l

# Monitor in real-time
watch -n 5 'squeue -u your_username'

# Cancel a job
scancel 45678
```

**Check output files:**
```bash
# View live output
tail -f logs/satinn_45678.out

# View errors
cat logs/satinn_45678.err
```

### SBATCH Parameters Explained

| Parameter | Purpose | Example |
|-----------|---------|---------|
| `--job-name` | Descriptive name for your job | `satinn_week7_segmentation` |
| `--nodes` | Number of compute nodes | 1 (for SATINN, typically 1) |
| `--ntasks` | Number of parallel tasks | 1 (unless parallelizing with MPI) |
| `--cpus-per-task` | CPU cores needed | 8 (reasonable for image processing) |
| `--mem` | Total memory needed | 32G (e.g., 4 GB × 8 cores) |
| `--time` | Max job duration (HH:MM:SS) | 02:00:00 (2 hours) |
| `--output` | Where to save stdout | logs/job_%j.out |
| `--error` | Where to save stderr | logs/job_%j.err |
| `--mail-user` | Email for notifications | your_email@ohsu.edu |
| `--mail-type` | When to email | END,FAIL (on completion or failure) |

### Queue Times and Partitions

**Default partition:** `general` (first-come, first-served, up to 24 hours)  
**High-priority partition:** `express` (faster but shorter wall time, reserved for urgent work)  
**GPU partition:** `gpu` (for deep learning, limited availability)

**Check available partitions:**
```bash
sinfo --all
```

**Request specific partition in script:**
```bash
#SBATCH --partition=express
#SBATCH --time=00:30:00
```

## Fair Sharing Principles

### 1. Request Only What You Need

**Bad:** Request 64 cores and 256 GB for a simple Python script
```bash
#SBATCH --cpus-per-task=64  # Wastes resources
#SBATCH --mem=256G          # Wastes resources
```

**Good:** Test locally, then estimate
```bash
# Test locally first
python satinn/preprocess_images.py --num-workers 4
# Took 30 seconds for 10 images
# Estimate: 100 images × (30/10) / 60 = 5 minutes
# Add buffer: request 10 minutes, 4 cores, 8 GB

#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=00:10:00
```

### 2. Parallelize Efficiently

**CPU parallelization (for multi-image processing):**
```python
# satinn/preprocess_images.py
from multiprocessing import Pool
import os

# Use all available cores efficiently
num_workers = int(os.environ.get('SLURM_CPUS_PER_TASK', 1))

def preprocess_image(image_path):
    """Process one image."""
    return apply_satinn_preprocessing(image_path)

if __name__ == '__main__':
    images = list(Path('raw_images/').glob('*.tif'))
    
    with Pool(num_workers) as pool:
        results = pool.map(preprocess_image, images)
    
    print(f"Processed {len(results)} images using {num_workers} workers")
```

**In SLURM script:**
```bash
#SBATCH --cpus-per-task=8  # Now uses 8 cores in parallel
python satinn/preprocess_images.py
```

### 3. Avoid Resource Oversubscription

**Bad:** Request 8 cores but actually use only 1
```python
# Forgot to use multiprocessing
for image_path in images:
    result = preprocess_image(image_path)  # Sequential, slow
```

**Good:** Match resource request to actual usage
```python
# Use all 8 cores
with Pool(8) as pool:
    results = pool.map(preprocess_image, images)
```

### 4. Submit Jobs During Off-Peak Hours

- Avoid 9 AM - 5 PM Monday-Friday if possible
- Batch multiple jobs into one script
- Combine several small jobs into a single SLURM job

## Naming Conventions

### Datasets

```
/data/datasets/
├── testis_slides_raw_20241015/      # Date added for tracking
│   ├── slide_001_specimen_A.tif
│   ├── slide_001_specimen_A.txt    # Metadata file
│   └── README.md                    # Source, acquisition parameters
├── testis_slides_processed_20241015_kernel5/  # Processing params in name
│   └── slide_001_preprocessed.tif
└── validation_set_Week10_20241105/  # Explicitly versioned for validation
    └── ...
```

**Key principles:**
- Include date processed (YYYYMMDD format)
- Include key parameters (kernel size, threshold, etc.)
- Use underscores, not spaces
- Add metadata README explaining source and processing

### Experiments and Results

```bash
# Bad naming (not reproducible)
/data/users/username/output/
├── result1.tif
├── result2.tif
└── final_FINAL_actualfinal.tif    # Confusing

# Good naming (reproducible)
/data/users/username/satinn_results/
├── 20241015_preprocessing_kernel5_blur2/
│   ├── config.yaml                  # Exact parameters used
│   ├── results_summary.json         # Metrics and metadata
│   ├── processed_slide_001.tif
│   └── processed_slide_002.tif
└── 20241016_segmentation_threshold127/
    ├── config.yaml
    ├── segmented_slide_001.tif
    └── ...
```

**Result filename conventions:**
```bash
# Format: YYYYMMDD_stage_parameters_replicate.ext
20241015_preprocessing_kernel5_v1.tif
20241015_segmentation_threshold127_watershed_v2.tif
20241015_features_extracted_morphology_v1.csv
```

## Logging and Monitoring Long-Running Jobs

### 1. Structured Logging

```python
# satinn/preprocess_images.py
import logging
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/satinn_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting SATINN preprocessing")
    logger.info(f"Processing images from: {input_dir}")
    
    images = list(Path(input_dir).glob('*.tif'))
    logger.info(f"Found {len(images)} images")
    
    start_time = time.time()
    
    for i, image_path in enumerate(images):
        logger.info(f"Processing {i+1}/{len(images)}: {image_path.name}")
        
        try:
            result = preprocess_image(image_path)
            logger.info(f"  ✓ Success (shape: {result.shape})")
        except Exception as e:
            logger.error(f"  ✗ Failed: {str(e)}", exc_info=True)
            continue
    
    elapsed = time.time() - start_time
    logger.info(f"Completed in {elapsed:.1f} seconds ({elapsed/len(images):.2f}s per image)")
```

**Log output:**
```
2024-10-15 10:23:45,123 - __main__ - INFO - Starting SATINN preprocessing
2024-10-15 10:23:45,456 - __main__ - INFO - Processing images from: /data/datasets/testis_slides/
2024-10-15 10:23:45,789 - __main__ - INFO - Found 20 images
2024-10-15 10:23:46,012 - __main__ - INFO - Processing 1/20: slide_001.tif
2024-10-15 10:23:46,789 - __main__ - INFO -   ✓ Success (shape: (2048, 2048))
2024-10-15 10:23:47,456 - __main__ - INFO - Processing 2/20: slide_002.tif
...
```

### 2. Monitor Resource Usage

```bash
# Check current memory usage in your job
# (Run inside SLURM job)
ps aux | grep python  # See process details

# Monitor real-time system stats
top -u $USER

# Check disk usage
du -sh /data/users/username/
quota -s /data/users/username/
```

### 3. Checkpointing for Long Jobs

Save intermediate results so you can restart if job fails:

```python
# satinn/preprocess_images.py
from pathlib import Path
import pickle

def main(resume=False):
    output_dir = Path('satinn_results')
    checkpoint_file = output_dir / 'checkpoint.pkl'
    
    # Load checkpoint if resuming
    if resume and checkpoint_file.exists():
        with open(checkpoint_file, 'rb') as f:
            state = pickle.load(f)
        processed = set(state['processed_files'])
        logger.info(f"Resuming from checkpoint: {len(processed)} files already processed")
    else:
        processed = set()
    
    images = sorted(Path('raw_images/').glob('*.tif'))
    
    for image_path in images:
        if image_path.name in processed:
            logger.info(f"Skipping {image_path.name} (already processed)")
            continue
        
        logger.info(f"Processing {image_path.name}")
        result = preprocess_image(image_path)
        
        # Save intermediate result
        output_file = output_dir / f"{image_path.stem}_preprocessed.tif"
        cv2.imwrite(str(output_file), result)
        
        # Update checkpoint
        processed.add(image_path.name)
        with open(checkpoint_file, 'wb') as f:
            pickle.dump({'processed_files': list(processed)}, f)
        
        logger.info(f"  Saved to {output_file}")
    
    logger.info(f"All {len(processed)} images processed successfully")

# Submit first run
# sbatch run_satinn.sh

# If job times out, resume with:
# sbatch --dependency=afternotok:45678 run_satinn_resume.sh
```

**Resume script (run_satinn_resume.sh):**
```bash
#!/bin/bash
#SBATCH --job-name=satinn_preprocessing_resume
#SBATCH --time=02:00:00
# ... other parameters ...

python satinn/preprocess_images.py --resume
```

## Common Mistakes and Recovery

### 1. Requesting Too Much Memory

**Symptom:** Job queued for hours, never runs
```bash
#SBATCH --mem=512G  # More than any node has!
```

**Fix:** Check node capacity and request realistic amount
```bash
# Check node specs
sinfo -N -l | head -10

# Node memory is typically 256-512 GB
# Request 50-75% of that
#SBATCH --mem=200G  # Safe
```

### 2. Job Killed Due to Timeout

**Symptom:** Job stops abruptly, error says "Time limit exceeded"
```bash
#SBATCH --time=00:30:00  # Too short!
```

**Fix:** Estimate time accurately
```bash
# Test locally to measure
time python satinn/preprocess_images.py --sample 10

# Extrapolate: if 10 images take 5 minutes, 200 images take ~100 minutes
# Add 20% buffer
#SBATCH --time=02:00:00  # Safe
```

### 3. Running Interactive Jobs (Bad!)

**Bad:** Logging into Prime8 and running jobs directly
```bash
ssh prime8.ohsu.edu
cd /data/datasets
# Running command here directly (blocking terminal, wastes headroom)
python satinn/preprocess_images.py  # Runs interactively
```

This ties up the login node and can freeze the cluster.

**Good:** Always use SLURM for compute jobs
```bash
# On your laptop
sbatch run_satinn.sh  # Submit to cluster

# Monitor from anywhere
squeue -u your_username

# Results stored on cluster, download later
scp prime8.ohsu.edu:/data/users/username/results/* ~/Downloads/
```

### 4. Forgetting Output Redirection

**Bad:** Output lost if job fails
```bash
#SBATCH --job-name=satinn

python satinn/preprocess_images.py
# Output disappears if job crashes!
```

**Good:** Always capture output
```bash
#SBATCH --job-name=satinn
#SBATCH --output=logs/satinn_%j.out
#SBATCH --error=logs/satinn_%j.err

python satinn/preprocess_images.py
```

### 5. Filling Disk with Intermediate Files

**Symptom:** "Disk quota exceeded" error mid-job
```python
# Saving every intermediate step (wasteful)
for image in images:
    result1 = preprocess(image)
    cv2.imwrite(f'intermediate_{i}_step1.tif', result1)  # 1 GB
    
    result2 = segment(result1)
    cv2.imwrite(f'intermediate_{i}_step2.tif', result2)  # 1 GB
    
    result3 = extract_features(result2)
    cv2.imwrite(f'intermediate_{i}_step3.tif', result3)  # 1 GB
    # Total: 3 GB × 200 images = 600 GB!
```

**Fix:** Keep only essential outputs
```python
for image in images:
    result1 = preprocess(image)
    result2 = segment(result1)
    result3 = extract_features(result2)
    
    # Save only final result
    np.save(f'features_{i}.npy', result3)  # 10 MB instead of 3 GB
    
    # Clean up intermediate results
    del result1, result2
```

## SATINN-Specific Recommendations

### For Week 2 Assignment

1. **Set up your account:** Request Prime8 access from mentor
2. **Create directory structure:**
   ```bash
   cd /data/users/your_username
   mkdir -p satinn_code satinn_data satinn_results logs
   ```

3. **Test a simple job:**
   ```bash
   # Create test_job.sh
   #!/bin/bash
   #SBATCH --job-name=satinn_test
   #SBATCH --cpus-per-task=1
   #SBATCH --mem=2G
   #SBATCH --time=00:05:00
   
   python -c "import numpy; print(f'NumPy version: {numpy.__version__}')"
   
   # Submit
   sbatch test_job.sh
   
   # Monitor
   squeue -u your_username
   cat logs/satinn_test_*.out
   ```

4. **Document your setup** in a README for your mentor to review

### For SATINN Preprocessing (Weeks 7-8)

- Request 8-16 cores for image parallelization
- Estimate memory as 50-100 MB per image + buffer
- Save preprocessing logs with parameters for validation (Week 10)
- Name results with date and parameters for traceability

## Next Steps

- **Assignment (Week 2):** Get Prime8 access, run a test job, document how to submit and monitor
- **Weeks 7-8:** Submit preprocessing jobs with proper resource requests and logging
- **Week 10:** Use logs to compare Python and reference implementations

## References

- OHSU Prime8 Documentation: https://ohsu.edu/xsede/
- SLURM Guide: https://slurm.schedmd.com/quickstart.html
- HPC Best Practices: https://www.prace-ri.eu/best-practice-guide/

### The Reproducibility Crisis
Studies in psychology, biology, and medicine show that 50-70% of published findings cannot be reproduced. Common culprits:
- Undocumented random operations
- Different library versions
- Slightly different data preprocessing
- Manual parameter changes not recorded

## Version Control for Code, Data, and Environment

### 1. Code Version Control (Git)

Already required for SATINN, but key principles:

**Commit frequently with descriptive messages:**
```
GOOD: "Add Gaussian blur preprocessing step with radius=2 (tested on training set)"
BAD:  "updates" or "fix"
```

**Include what changed and why:** This helps you (and reviewers) understand the computational decisions.

**Example commit for SATINN preprocessing:**
```bash
git commit -m "Implement histogram equalization in preprocessing

- Add cv2.equalizeHist() to normalize image contrast
- Tested: improves segmentation accuracy on low-contrast slides
- Parameters: default cv2 settings (CLAHE skipped for now)
- Issue: #6"
```

### 2. Data Version Control

**Problem:** Images and datasets are large; you can't store 100 versions in Git.

**Solution:** Use a data manifest + external storage.

**Approach for SATINN:**
```bash
# Create a manifest file (tracked in Git)
data/
├── MANIFEST.md              # Track data versions
├── raw/
│   └── testis_slides/
│       └── .gitignore       # Ignore actual images
└── README.md
```

**MANIFEST.md example:**
```markdown
# Data Manifest

## raw/testis_slides/

| Filename | MD5 Hash | Date | Notes |
|----------|----------|------|-------|
| slide_001.tif | a1b2c3d4e5f6... | 2024-10-15 | Original acquisition |
| slide_002.tif | x9y8z7w6v5u4... | 2024-10-15 | Original acquisition |

Source: OHSU Pathology Core Facility
Storage: `/data/satinn/raw/testis_slides/` (Prime8 cluster)
MD5 checksums: verify file integrity across platforms

To verify:
  md5sum slide_001.tif
  # Should match: a1b2c3d4e5f6...
```

**Why MD5 hash?** Ensures data hasn't been corrupted or accidentally modified.

**Command to generate manifest:**
```bash
# Generate MD5 hashes for all images
cd data/raw/testis_slides/
md5sum *.tif > MD5SUMS
# Store MD5SUMS in MANIFEST.md
```

### 3. Environment Version Control

**Problem:** Your code works in Python 3.9.1 with scikit-image 0.18.1, but fails in 3.11.0 with scikit-image 0.21.0.

**Solution:** Pin all dependencies explicitly.

**For SATINN, create `requirements.txt`:**
```
numpy==1.24.3
scipy==1.11.1
opencv-python==4.8.0.74
scikit-image==0.21.0
scikit-learn==1.3.0
matplotlib==3.7.2
jupyter==1.0.0
pytest==7.4.0
```

**Install from this file:**
```bash
pip install -r requirements.txt
```

**In notebooks, document setup:**
```python
import sys
print(f"Python version: {sys.version}")

import numpy as np
import cv2
import sklearn

print(f"NumPy: {np.__version__}")
print(f"OpenCV: {cv2.__version__}")
print(f"scikit-learn: {sklearn.__version__}")
```

**For conda environments:**
```yaml
# environment.yml
name: satinn-dev
channels:
  - defaults
  - conda-forge
dependencies:
  - python=3.10
  - numpy=1.24.3
  - opencv=4.8.0
  - scikit-image=0.21.0
  - jupyter=1.0.0
```

**Activate the same environment:**
```bash
conda env create -f environment.yml
conda activate satinn-dev
```

## Documenting Parameters, Random Seeds, and Dependencies

### Parameters Must Be Explicit

**Bad code:**
```python
# Hidden magic numbers—how do you know what was tested?
blurred = cv2.GaussianBlur(image, (5, 5), 0)
thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)[1]
```

**Good code:**
```python
# All parameters documented
GAUSSIAN_KERNEL_SIZE = 5  # Tested: smaller blurs too much, larger is too slow
GAUSSIAN_SIGMA = 0        # Let OpenCV calculate automatically
THRESHOLD_VALUE = 127     # Midpoint; consider adaptive thresholding for uneven lighting
THRESHOLD_MAX = 255       # Standard 8-bit image range

blurred = cv2.GaussianBlur(image, (GAUSSIAN_KERNEL_SIZE, GAUSSIAN_KERNEL_SIZE), GAUSSIAN_SIGMA)
thresh = cv2.threshold(blurred, THRESHOLD_VALUE, THRESHOLD_MAX, cv2.THRESH_BINARY)[1]
```

**Better: Configuration file**
```python
# config.py
PREPROCESSING = {
    'gaussian_kernel_size': 5,
    'gaussian_sigma': 0,
    'threshold_value': 127,
    'threshold_max': 255,
}

# usage.py
from config import PREPROCESSING
blurred = cv2.GaussianBlur(image, 
                           (PREPROCESSING['gaussian_kernel_size'], 
                            PREPROCESSING['gaussian_kernel_size']),
                           PREPROCESSING['gaussian_sigma'])
```

### Random Seeds Must Be Set

**Random operations:** model training, data shuffling, stochastic algorithms

```python
import numpy as np
import random
from sklearn.ensemble import RandomForestClassifier

# Set all random seeds at script start
RANDOM_SEED = 42

np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

# Now reproducible
model = RandomForestClassifier(n_estimators=100, random_state=RANDOM_SEED)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=RANDOM_SEED)
```

**Document the seed choice:**
```python
# RANDOM_SEED = 42
# Chosen for reproducibility (fixed for entire project)
# If changed, re-run validation against reference outputs
```

### Dependencies in Code Comments

```python
"""
satinn/preprocessing.py

Dependencies:
  - OpenCV 4.8.0+ (cv2) for image processing
  - NumPy 1.24.3+ for array operations
  - scikit-image 0.21.0+ for advanced morphology
  
If using different versions, validate against reference_outputs/ (see Week 10).

Author: Tobe, Mentor: [Mentor Name]
Date: 2024-10
"""
```

## Literate Programming and Notebooks

**Literate programming** interleaves code and narrative—code tells the story.

### Jupyter Notebook Best Practices for Reproducibility

```python
# Cell 1: Setup (always run first)
import sys
import numpy as np
import cv2
from pathlib import Path

print(f"Python {sys.version}")
print(f"NumPy {np.__version__}, OpenCV {cv2.__version__}")

# Cell 2: Configuration
DATA_DIR = Path('../data/raw')
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# Cell 3: Load data
images = sorted(DATA_DIR.glob('*.tif'))
print(f"Found {len(images)} images")

# Cell 4: Preprocess
def preprocess_image(path, kernel_size=5):
    """
    Apply Gaussian blur and thresholding.
    
    Args:
        path: Path to image file
        kernel_size: Gaussian kernel size (must be odd)
    
    Returns:
        thresh: Binary thresholded image
    """
    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    blurred = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
    _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)
    return thresh

# Cell 5: Process all images (with progress)
results = []
for img_path in images:
    processed = preprocess_image(img_path)
    results.append({'file': img_path.name, 'shape': processed.shape})
    print(f"✓ {img_path.name}")

# Cell 6: Verify outputs
print(f"Processed {len(results)} images successfully")
```

**Notebook organization:**
1. **Setup** – imports, versions, paths
2. **Configuration** – all parameters and seeds
3. **Load** – read input data
4. **Process** – functions and transformations
5. **Evaluate** – metrics and visualizations
6. **Save** – export results and logs

### Export Notebooks for Version Control

Notebooks contain metadata that makes Git diffs messy. Solution:

```bash
# Use nbstripout to remove execution history before committing
pip install nbstripout
git config filter.jupyternotebook.clean "nbstripout"

# .gitattributes
*.ipynb filter=jupyternotebook
```

Now Git tracks only source code, not execution output.

## Computational Reproducibility Checklist

Use this before committing code:

```markdown
## Reproducibility Checklist

- [ ] All random seeds set (numpy, random, sklearn, etc.)
- [ ] Dependencies listed in requirements.txt with versions
- [ ] All magic numbers moved to config file or top-of-file constants
- [ ] Data input documented: file paths, MD5 hashes where applicable
- [ ] Expected outputs documented (shapes, ranges, example values)
- [ ] Parameters explained in comments
- [ ] Code runs without user intervention (no manual copy-paste)
- [ ] Commit message explains *why*, not just *what*
- [ ] Cross-platform path handling (use pathlib, not hardcoded paths)
- [ ] Output timestamps logged (for debugging timing issues)

Example output log for SATINN preprocessing:
  Input: 20 images, 2048x2048 pixels each
  Processing time: 45 seconds
  Output: 20 binary masks, mean fill density 0.32
  Random seed: 42
  OpenCV version: 4.8.0
```

## SATINN-Specific Reproducibility Requirements

### Why Version Control Matters for SATINN

1. **Reference Comparison (Week 10):** You'll compare Python outputs to MATLAB reference. Must be byte-for-byte identical (or within documented tolerance).

2. **Segmentation Stability:** If segmentation results differ between runs, validation fails. Fixed seed ensures consistency.

3. **Feature Extraction Traceability:** Each feature value is traced to a parameter choice. Document every choice.

4. **Collaborative Extension:** Others will extend your code. Clear documentation prevents silent bugs.

### Example: SATINN Preprocessing Module

```python
# satinn/preprocessing.py
"""
Image preprocessing pipeline for testis histology slides.

Reproducibility notes:
- All random operations use RANDOM_SEED (see config.py)
- Kernel sizes tuned on training set (slide_001-010), validated on test set (slide_011-020)
- MD5 hashes of input images checked before processing
- Output stored with metadata log

See docs/research/satinn-validation-plan.md for tolerance thresholds.
"""

from pathlib import Path
import hashlib
import json
import numpy as np
import cv2
from config import RANDOM_SEED, PREPROCESSING_CONFIG

def compute_md5(filepath):
    """Verify data integrity."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def preprocess_pipeline(image_path, config=PREPROCESSING_CONFIG):
    """
    Apply full preprocessing: normalize, blur, threshold.
    
    Args:
        image_path: Path to input .tif file
        config: Dict with parameters (see config.py)
    
    Returns:
        result: Dict with {preprocessed_image, metadata}
    """
    np.random.seed(RANDOM_SEED)  # Ensure reproducibility
    
    # Verify data integrity
    md5 = compute_md5(image_path)
    expected_md5 = load_expected_md5(image_path)
    assert md5 == expected_md5, f"Data corruption detected in {image_path}"
    
    # Load and preprocess
    img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    blurred = cv2.GaussianBlur(img, 
                               (config['kernel_size'], config['kernel_size']), 
                               config['sigma'])
    _, thresh = cv2.threshold(blurred, 
                              config['threshold'], 
                              255, 
                              cv2.THRESH_BINARY)
    
    # Log metadata for reproducibility
    metadata = {
        'input_file': str(image_path),
        'input_md5': md5,
        'kernel_size': config['kernel_size'],
        'sigma': config['sigma'],
        'threshold': config['threshold'],
        'output_shape': thresh.shape,
        'output_dtype': str(thresh.dtype),
        'random_seed': RANDOM_SEED,
    }
    
    return {'preprocessed': thresh, 'metadata': metadata}

def load_expected_md5(image_path):
    """Load expected MD5 from data/MANIFEST.md"""
    # Implementation reads manifest and returns expected hash
    pass
```

## Next Steps

- **Assignment (Week 6):** Set up a Git repo with reproducible workflow: fixed seeds, documented parameters, version-pinned requirements.txt, README explaining how to reproduce results.
- **For SATINN:** Create config.py and requirements.txt for the project. Test that code runs identically on two machines.
- **Validation (Week 10):** Use these practices to document discrepancies between Python and reference implementations.

## References

- Good Research Code: https://goodresearch.dev/
- Ten Years of Reproducibility in CS: https://arxiv.org/abs/1805.06881
- Jupyter Best Practices: https://docs.jupyter.org/en/latest/
- nbstripout: https://github.com/kynan/nbstripout
