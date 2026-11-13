# Scientific Reproducibility in Computational Research

**Target Week:** Week 6  
**Learning Objective:** Understand reproducibility principles and implement reproducible workflows  
**Time Estimate:** 2-3 hours reading + practice  

## Why Reproducibility Matters

**Reproducibility** means someone else (or you, 6 months later) can run your code with the same data and get identical results.

### In Published Research
- Journals increasingly require reproducible methods before publishing
- Reviewers want to verify findings independently
- Your own future work depends on trusting past code

### In SATINN Development
- Multiple people will extend the Python implementation
- SATINN outputs will be used in biological experiments—errors propagate
- Validation (Week 10) requires identical outputs from reference and reimplementation
- Debugging is impossible if results change on each run

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
