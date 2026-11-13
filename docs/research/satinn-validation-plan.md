# SATINN Validation Plan and Methodology

**Target Week:** Week 10  
**Purpose:** Ensure Python implementation matches reference MATLAB outputs  
**Success Criteria:** > 95% agreement between implementations  

## Objective

Validate that the Python implementation of SATINN produces outputs equivalent to the MATLAB reference, within acceptable numerical tolerances.

**Why validation matters:**
- Ensures correctness before using Python version for research
- Provides confidence that algorithm was ported correctly
- Identifies any unintended algorithmic changes
- Creates benchmark for future extensions

---

## Validation Dataset

### Ground Truth and Reference Outputs

**Validation set:** 20 held-out images, not used during development (Weeks 1-9).

**Images:**
- 20 .tif files, 2048 × 2048 pixels each
- Acquisition date: [Date], same batch as training/development images
- Storage: `/data/satinn/validation_set_Week10/`
- File naming: `slide_XXX_validation.tif`

**Reference outputs (from MATLAB):**
- Stored in: `/data/satinn/reference_outputs/`
- For each image:
  - `slide_XXX_preprocessed.tif` – preprocessed binary image
  - `slide_XXX_segmented.tif` – segmentation label map
  - `slide_XXX_features.csv` – extracted features
  - `slide_XXX_predictions.csv` – cell type predictions
  - `slide_XXX_metadata.json` – processing parameters and timing

**Ground truth labels (manual):**
- 50-100 regions per image manually labeled by pathologist
- Labels: {nucleus, cytoplasm, artifact}
- Stored in: `/data/satinn/ground_truth_labels.csv`
- Fields: `image_id, region_id, ground_truth_type`

---

## Numerical Tolerance Thresholds

Different stages have different tolerance criteria (pixel-perfect matching is not required).

### Stage-by-Stage Tolerances

| Stage | Comparison | Metric | Acceptable Threshold | Rationale |
|-------|-----------|--------|----------------------|-----------|
| **Preprocessing** | Pixel values | Max absolute difference | ± 1 intensity (0-255 range) | Rounding and interpolation |
| | | Mean absolute error | < 0.1% | Should be very close |
| **Segmentation** | Label maps | Dice coefficient | > 0.95 | Allows minor boundary differences |
| | | Jaccard index | > 0.90 | |
| | Region counts | Total regions | ± 10% | Segmentation may vary slightly |
| **Features** | Morphological features | Relative error | < 1% | Computed from slightly different boundaries |
| | Intensity features | Relative error | < 0.5% | Depends on exact pixel values |
| **Predictions** | Cell type agreement | Accuracy | > 95% | Overall match rate |
| | | Per-class F1 score | > 0.90 | Balanced performance |
| **Counts** | Total counts | Relative error | < 5% | Final metric of interest |

### Why These Tolerances?

**Preprocessing (±1 pixel):**
- Different libraries (MATLAB vs. OpenCV) may implement filtering slightly differently
- Floating-point rounding can accumulate across operations
- ±1 pixel is imperceptible to human eye

**Segmentation (Dice > 0.95):**
- Watershed may find slightly different boundary locations
- But overall region assignment should be 95%+ the same
- Dice coefficient penalizes boundary shifts

**Features (< 1% error):**
- Computed from potentially different segmentations
- Area changes by 1 pixel → <1% error (for regions of ~100 pixels)
- Intensity is averaged, so robust to small pixel differences

**Predictions (> 95% accuracy):**
- This is the final output that matters
- 95% agreement means 1 in 20 regions misclassified
- Acceptable for scientific use (compare to human inter-rater variability)

---

## Comparison Methodology: Side-by-Side Evaluation

### Step 1: Run Both Implementations

**MATLAB (reference):**
```bash
# Already completed; outputs in reference_outputs/
cd /path/to/satinn_matlab
```

**Python (new implementation):**
```bash
# Run on same validation set
cd /data/users/username/satinn_python
python -m satinn.main \
  --input-dir /data/satinn/validation_set_Week10 \
  --output-dir /data/users/username/python_outputs \
  --config config_validation.yaml
```

### Step 2: Compare Each Stage

#### 2A. Preprocessing Comparison

```python
import cv2
import numpy as np
from pathlib import Path

def compare_images(matlab_path, python_path, image_name):
    """Compare preprocessed images pixel-by-pixel."""
    
    matlab_img = cv2.imread(str(matlab_path), cv2.IMREAD_GRAYSCALE).astype(np.float64)
    python_img = cv2.imread(str(python_path), cv2.IMREAD_GRAYSCALE).astype(np.float64)
    
    diff = np.abs(matlab_img - python_img)
    
    print(f"\n{image_name}:")
    print(f"  Max pixel difference: {np.max(diff)}")
    print(f"  Mean pixel difference: {np.mean(diff):.3f}")
    print(f"  Std pixel difference: {np.std(diff):.3f}")
    print(f"  Pixels with diff > 1: {np.sum(diff > 1)} / {diff.size}")
    
    if np.max(diff) <= 1:
        print(f"  Status: PASS (within tolerance)")
    else:
        print(f"  Status: FAIL (exceeds tolerance)")
    
    return diff

# Compare all validation images
matlab_dir = Path('/data/satinn/reference_outputs')
python_dir = Path('/data/users/username/python_outputs')

for i in range(1, 21):
    image_name = f'slide_{i:03d}_validation'
    matlab_file = matlab_dir / f'{image_name}_preprocessed.tif'
    python_file = python_dir / f'{image_name}_preprocessed.tif'
    compare_images(matlab_file, python_file, image_name)
```

**Output:**
```
slide_001_validation:
  Max pixel difference: 1
  Mean pixel difference: 0.012
  Std pixel difference: 0.089
  Pixels with diff > 1: 0 / 4194304
  Status: PASS (within tolerance)

slide_002_validation:
  Max pixel difference: 1
  Mean pixel difference: 0.008
  Std pixel difference: 0.071
  Pixels with diff > 1: 0 / 4194304
  Status: PASS (within tolerance)
```

#### 2B. Segmentation Comparison

```python
from sklearn.metrics import jaccard_score, f1_score
from scipy.ndimage import label

def compare_segmentations(matlab_seg, python_seg):
    """Compare segmentation label maps."""
    
    # Method 1: Jaccard index (overlap of non-zero regions)
    matlab_binary = (matlab_seg > 0).astype(int)
    python_binary = (python_seg > 0).astype(int)
    
    jaccard = jaccard_score(matlab_binary.ravel(), python_binary.ravel(), average='binary')
    
    # Method 2: Dice coefficient
    intersection = np.logical_and(matlab_binary, python_binary).sum()
    dice = 2.0 * intersection / (matlab_binary.sum() + python_binary.sum())
    
    # Method 3: Region count comparison
    matlab_regions = np.max(matlab_seg)
    python_regions = np.max(python_seg)
    
    print(f"Jaccard index: {jaccard:.4f} (target: > 0.95)")
    print(f"Dice coefficient: {dice:.4f} (target: > 0.95)")
    print(f"Region count: MATLAB={matlab_regions}, Python={python_regions}")
    print(f"Region count difference: {abs(matlab_regions - python_regions)} ({100*abs(matlab_regions-python_regions)/matlab_regions:.1f}%)")
    
    if jaccard > 0.95 and dice > 0.95:
        print("Status: PASS")
    else:
        print("Status: FAIL")
    
    return jaccard, dice

# Compare all segmentations
for i in range(1, 21):
    image_name = f'slide_{i:03d}_validation'
    matlab_seg = cv2.imread(str(matlab_dir / f'{image_name}_segmented.tif'), cv2.IMREAD_GRAYSCALE)
    python_seg = cv2.imread(str(python_dir / f'{image_name}_segmented.tif'), cv2.IMREAD_GRAYSCALE)
    
    print(f"\n{image_name}:")
    compare_segmentations(matlab_seg, python_seg)
```

**Output:**
```
slide_001_validation:
Jaccard index: 0.9621 (target: > 0.95)
Dice coefficient: 0.9808 (target: > 0.95)
Region count: MATLAB=1247, Python=1250
Region count difference: 3 (0.2%)
Status: PASS

slide_002_validation:
Jaccard index: 0.9501 (target: > 0.95)
Dice coefficient: 0.9745 (target: > 0.95)
Region count: MATLAB=1523, Python=1521
Region count difference: 2 (0.1%)
Status: PASS
```

#### 2C. Feature Comparison

```python
import pandas as pd
from scipy.stats import pearsonr

def compare_features(matlab_features_csv, python_features_csv, image_name):
    """Compare extracted feature tables."""
    
    matlab_df = pd.read_csv(matlab_features_csv)
    python_df = pd.read_csv(python_features_csv)
    
    # Merge on region_id
    merged = matlab_df.merge(python_df, on='region_id', suffixes=('_matlab', '_python'))
    
    feature_cols = [col for col in matlab_df.columns if col != 'region_id']
    
    print(f"\n{image_name}: Feature Comparison")
    print("-" * 60)
    
    all_pass = True
    for feature in feature_cols:
        matlab_col = f'{feature}_matlab'
        python_col = f'{feature}_python'
        
        if matlab_col in merged.columns and python_col in merged.columns:
            # Compute relative error
            relative_error = np.abs(merged[matlab_col] - merged[python_col]) / (np.abs(merged[matlab_col]) + 1e-6)
            mean_error = relative_error.mean() * 100  # as percentage
            
            # Correlation
            correlation = pearsonr(merged[matlab_col], merged[python_col])[0]
            
            tolerance = 1.0 if 'intensity' not in feature else 0.5
            status = "PASS" if mean_error < tolerance else "FAIL"
            all_pass = all_pass and (mean_error < tolerance)
            
            print(f"  {feature:20s}: {mean_error:6.2f}% error (r={correlation:.4f}) [{status}]")
    
    print(f"Overall: {'PASS' if all_pass else 'FAIL'}")
    return all_pass

# Compare all feature tables
for i in range(1, 21):
    image_name = f'slide_{i:03d}_validation'
    compare_features(
        matlab_dir / f'{image_name}_features.csv',
        python_dir / f'{image_name}_features.csv',
        image_name
    )
```

**Output:**
```
slide_001_validation: Feature Comparison
------------------------------------------------------------
  area                :   0.34% error (r=0.9998) [PASS]
  perimeter           :   0.52% error (r=0.9997) [PASS]
  eccentricity        :   0.18% error (r=0.9999) [PASS]
  solidity            :   0.09% error (r=0.9999) [PASS]
  intensity_mean      :   0.28% error (r=0.9998) [PASS]
  intensity_std       :   0.41% error (r=0.9997) [PASS]
Overall: PASS
```

#### 2D. Prediction Comparison

```python
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

def compare_predictions(matlab_pred_csv, python_pred_csv, ground_truth_csv, image_name):
    """Compare predictions against ground truth."""
    
    matlab_df = pd.read_csv(matlab_pred_csv)
    python_df = pd.read_csv(python_pred_csv)
    truth_df = pd.read_csv(ground_truth_csv)
    
    # Merge on region_id
    comparison = matlab_df.merge(python_df, on='region_id', suffixes=('_matlab', '_python'))
    comparison = comparison.merge(truth_df, on='region_id')
    
    # Get predictions
    matlab_pred = comparison['predicted_type_matlab']
    python_pred = comparison['predicted_type_python']
    truth = comparison['ground_truth_type']
    
    # Compare implementations
    agreement = accuracy_score(matlab_pred, python_pred)
    
    # Evaluate against ground truth
    matlab_accuracy = accuracy_score(truth, matlab_pred)
    python_accuracy = accuracy_score(truth, python_pred)
    
    print(f"\n{image_name}: Prediction Comparison")
    print("-" * 60)
    print(f"Agreement between MATLAB and Python: {agreement:.3%} (target: > 95%)")
    print(f"Accuracy vs. ground truth:")
    print(f"  MATLAB: {matlab_accuracy:.3%}")
    print(f"  Python: {python_accuracy:.3%}")
    
    print(f"\nConfusion matrix (Python vs. ground truth):")
    cm = confusion_matrix(truth, python_pred)
    print(cm)
    
    print(f"\nClassification report:")
    print(classification_report(truth, python_pred))
    
    if agreement > 0.95:
        print("Status: PASS")
    else:
        print("Status: FAIL")
    
    return agreement

# Compare all predictions
for i in range(1, 21):
    image_name = f'slide_{i:03d}_validation'
    compare_predictions(
        matlab_dir / f'{image_name}_predictions.csv',
        python_dir / f'{image_name}_predictions.csv',
        '/data/satinn/ground_truth_labels.csv',
        image_name
    )
```

**Output:**
```
slide_001_validation: Prediction Comparison
------------------------------------------------------------
Agreement between MATLAB and Python: 98.24% (target: > 95%)
Accuracy vs. ground truth:
  MATLAB: 96.45%
  Python: 96.51%

Confusion matrix (Python vs. ground truth):
[[215   8   0]
 [  7  78   1]
 [  0   2  12]]

Classification report:
              precision    recall  f1-score   support

      nucleus       0.968    0.964    0.966       223
    cytoplasm       0.883    0.911    0.897        86
     artifact       0.923    0.857    0.889        14

    accuracy                         0.965       323
   macro avg       0.925    0.911    0.917       323
weighted avg       0.965    0.965    0.965       323

Status: PASS
```

### Step 3: Summary Report

Create a comprehensive validation report:

```markdown
# SATINN Validation Report - Week 10

## Summary
- **Overall Status:** PASS
- **Images validated:** 20/20
- **Stages passing:** 4/4 (preprocessing, segmentation, features, predictions)

## Results by Stage

### Preprocessing
- Max pixel difference: 0-1 (all images)
- Mean error: < 0.05%
- Status: PASS

### Segmentation
- Jaccard index: 0.9501-0.9721 (all > 0.95)
- Region count difference: < 1%
- Status: PASS

### Features
- Mean relative error: 0.09-0.52% (well within 1% tolerance)
- Correlation with MATLAB: > 0.9995 (excellent)
- Status: PASS

### Predictions
- MATLAB-Python agreement: 97.8-99.2% (all > 95%)
- Accuracy vs. ground truth: 95.5-97.2%
- F1 score per class: > 0.88 (all classes)
- Status: PASS

## Discrepancies Identified

| Category | Count | Cause | Resolution |
|----------|-------|-------|-----------|
| Segmentation boundaries | ~3 per image | Watershed watershed starting point sensitivity | Documented; acceptable within Dice > 0.95 |
| Misclassified regions | 1-2 per image | Boundary regions with ambiguous features | Expected; consistent with human error rates |

## Validation Checklist

- [x] All 20 validation images processed
- [x] All outputs compared at each stage
- [x] Numerical tolerances met
- [x] Ground truth accuracy measured
- [x] Discrepancies documented
- [x] Root causes investigated
- [x] Python implementation approved for use

## Sign-Off

Python SATINN implementation is validated and equivalent to MATLAB reference.

**Validator:** Tobe  
**Date:** [Date]  
**Mentor Review:** [Mentor Name]
```

---

## How to Document and Investigate Discrepancies

### When Python Doesn't Match MATLAB

**Step 1: Isolate the problem**
- Which stage is failing? (preprocessing, segmentation, features, predictions)
- Is it a single image or all images?
- Is it systematic or random?

**Step 2: Compare outputs**
- Visualize images side-by-side
- Check parameter values (did MATLAB use different settings?)
- Look at any error messages or warnings

**Step 3: Review code**
- Check if algorithms are identical
- Look for differences in library implementations
- Verify parameter passing

**Example:** Segmentation Dice < 0.95

```python
# Debug script
import cv2
import numpy as np
from scipy.ndimage import label
import matplotlib.pyplot as plt

matlab_seg = cv2.imread('slide_001_matlab_segmented.tif', cv2.IMREAD_GRAYSCALE)
python_seg = cv2.imread('slide_001_python_segmented.tif', cv2.IMREAD_GRAYSCALE)

# Visualize side-by-side
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

axes[0].imshow(matlab_seg, cmap='tab20')
axes[0].set_title('MATLAB Segmentation')

axes[1].imshow(python_seg, cmap='tab20')
axes[1].set_title('Python Segmentation')

# Difference
diff = (matlab_seg > 0).astype(int) - (python_seg > 0).astype(int)
axes[2].imshow(diff, cmap='RdBu')
axes[2].set_title('Difference (Red=MATLAB only, Blue=Python only)')

plt.tight_layout()
plt.savefig('segmentation_comparison.png')

# Analyze boundary shifts
print(f"MATLAB regions: {np.max(matlab_seg)}")
print(f"Python regions: {np.max(python_seg)}")
print(f"Dice: {2*np.logical_and(matlab_seg>0, python_seg>0).sum() / (np.count_nonzero(matlab_seg) + np.count_nonzero(python_seg)):.4f}")
```

### Root Cause Analysis Template

```markdown
## Discrepancy Report: [Image Name] - [Stage]

**Problem:** [Brief description]

**Evidence:**
- Metric 1: [Value] (expected: [threshold])
- Metric 2: [Value] (expected: [threshold])

**Investigation:**
1. Compared [output A] to [output B]
2. Found difference in [specific aspect]
3. Checked [relevant code section]

**Root Cause:** [Why they differ]
- Potential causes: [list]
- Most likely: [chosen cause]

**Resolution:**
- [ ] Algorithm difference is intentional (document why)
- [ ] Bug in Python code (fix and re-validate)
- [ ] Bug in MATLAB code (revert to MATLAB output)
- [ ] Library difference (accept and document tolerance)

**Outcome:** [Resolution]
```

---

## Success Criteria and Sign-Off Process

### Stage Passing Criteria

- **Preprocessing:** All images, max pixel diff ≤ 1
- **Segmentation:** All images, Dice ≥ 0.95
- **Features:** All features, relative error < 1% (< 0.5% for intensity)
- **Predictions:** All images, accuracy ≥ 95%

### Final Sign-Off

Before declaring SATINN validated:

1. **Mentor review:** Mentor reviews report and validates findings
2. **Issue resolution:** All critical discrepancies have root causes documented
3. **Code quality:** Final code committed with validation scripts
4. **Documentation:** All deviations from reference documented

**Sign-off document:**
```
SATINN Python Implementation: APPROVED FOR USE

Weeks 1-9: Implemented complete pipeline
Week 10: Validation shows equivalence to MATLAB reference

Metrics:
  - Overall agreement: 97.8%
  - All validation checks passed
  - Discrepancies documented and acceptable

Approved by: [Mentor Name]
Date: [Date]
```

---

## Next Steps (Week 11-12)

- Use validated SATINN outputs for independent research
- Extend pipeline with novel analysis methods
- Share Python implementation with collaborators

## References

- Validation frameworks: https://github.com/slundberg/shap/blob/master/tests/
- Image comparison metrics: https://scikit-image.org/docs/stable/api/skimage.metrics.html
- Dice coefficient: https://en.wikipedia.org/wiki/S%C3%B8rensen%E2%80%93Dice_coefficient
