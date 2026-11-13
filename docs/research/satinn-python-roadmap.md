# SATINN Python Implementation Roadmap

**Overview:** Complete visual and narrative map of how SATINN's Python reimplementation builds over 12 weeks.

## Computational Pipeline Overview

**Raw images → Preprocessed images → Segmented regions → Extracted features → Validated predictions**

Each stage produces outputs that feed into the next. The roadmap shows which weeks address each stage.

## Stage-by-Stage Breakdown with Weekly Assignments

### Stage 1: Image Acquisition and Preparation (Week 1-2)

**What happens:** Raw testis histology slides are acquired, stored, and indexed.

**Weeks 1-2 Deliverables:**
- Learn OHSU research computing (Prime8 cluster, SLURM job scheduling)
- Catalog dataset: How many images? What format? What resolution?
- Create data manifest with MD5 hashes

**Python modules involved:**
- Data I/O: `satinn.io` (load .tif files, verify checksums)
- Configuration: `satinn.config` (paths to raw images)

**Issue links:** #1 (Setup), #2 (Data acquisition)

**Data flow:**
```
Raw slides (physical) → Digitized .tif files → Data manifest
```

---

### Stage 2: Preprocessing (Weeks 3-4)

**What happens:** Raw images are normalized, enhanced, and prepared for segmentation.

**Purpose:** Remove noise, correct uneven lighting, standardize intensity.

**Weeks 3-4 Deliverables:**
- Implement Gaussian blur and histogram equalization
- Test on sample of 5 images
- Document parameter choices (kernel size, threshold)

**Python modules involved:**
- Image processing: `satinn.preprocessing`
  - Functions: `load_image()`, `normalize()`, `apply_gaussian_blur()`, `threshold()`
- Visualization: `satinn.visualize` (display before/after)

**Week 4 assignment:** Implement ML classification fundamentals (see docs/learning/machine-learning-foundations.md); will apply to cell classification in Week 9.

**Issue links:** #3 (Preprocessing pipeline)

**Data flow:**
```
Raw .tif files
    ↓ [normalize intensity: 0-255 range]
Normalized images
    ↓ [blur: remove noise with Gaussian kernel]
Blurred images
    ↓ [threshold: convert to binary (black/white)]
Binary preprocessed images
```

---

### Stage 3: Segmentation (Weeks 5-6)

**What happens:** Binary images are segmented into connected regions (potential cells).

**Purpose:** Identify individual cell boundaries in crowded tissue.

**Weeks 5-6 Deliverables:**
- Implement watershed segmentation (marker-controlled)
- Label connected components
- Test on preprocessed images from Week 4

**Python modules involved:**
- Segmentation: `satinn.segmentation`
  - Functions: `find_markers()`, `watershed_segment()`, `label_regions()`
- Post-processing: `satinn.morphology` (remove small regions, fill holes)

**Week 6 assignment:** Implement reproducible computational workflows (see docs/learning/scientific-reproducibility.md); document all segmentation parameters.

**Issue links:** #4 (Segmentation), #5 (Post-processing)

**Data flow:**
```
Binary preprocessed images
    ↓ [find markers: identify seed points for cells]
Marker images
    ↓ [watershed: grow regions from markers]
Segmented label maps (each pixel labeled 1-N for N regions)
    ↓ [morphology: remove artifacts, fill holes]
Final cleaned segmentations
```

---

### Stage 4: Feature Extraction (Weeks 7-8)

**What happens:** For each segmented region, compute morphological features.

**Purpose:** Create numerical descriptors that distinguish cell types.

**Features extracted (biological relevance):**
- **Area:** Total pixels in region (cell size)
- **Perimeter:** Boundary length (cell shape regularity)
- **Eccentricity:** How elongated is the cell (nuclei vs. cytoplasm)
- **Solidity:** (Area / Convex hull area) – presence of concavities
- **Intensity statistics:** Mean, std of pixel intensities (nuclear density)

**Weeks 7-8 Deliverables:**
- Implement feature extraction for each region
- Compute on segmented images from Week 6
- Export to .csv format with region IDs

**Python modules involved:**
- Features: `satinn.features`
  - Functions: `extract_features()`, `compute_morphology()`, `compute_intensity()`
- Data export: `satinn.io` (save as CSV, compatible with ML tools)

**Week 7 assignment:** Begin independent research (Specific Aims ideation); see docs/research/independent-research.md

**Week 8 assignment:** Learn literature review methods and computational validation; start reading SATINN-related papers

**Issue links:** #6 (Feature extraction), #7 (Feature validation)

**Data flow:**
```
Segmented label maps
    ↓ [extract properties from each region]
Feature table: region_id, area, perimeter, eccentricity, ...
    (rows = regions, columns = features)
```

**Example feature table:**
```
region_id | area | perimeter | eccentricity | solidity | intensity_mean
1         | 456  | 82        | 0.65         | 0.92     | 180
2         | 1240 | 145       | 0.80         | 0.88     | 215
3         | 89   | 38        | 0.45         | 0.98     | 145
```

---

### Stage 5: Cell Classification and Counting (Weeks 9-10)

**What happens:** Using extracted features, classify each region as nucleus or cytoplasm, then count cells.

**Purpose:** Tally Sertoli cells, germ cells, and other cell types of biological interest.

**Weeks 9-10 Deliverables:**
- Train classifier on labeled training set (labeled by pathologist)
- Apply to all regions
- Compare Python predictions to MATLAB reference implementation

**Python modules involved:**
- Classification: `satinn.classification`
  - Functions: `train_classifier()`, `predict_cell_type()`, `compute_metrics()`
- Validation: `satinn.validation` (compare to reference, compute error statistics)

**Week 9 assignment:** Implement ML classification and cross-validation (reviewed in Week 4); apply to cell classification

**Week 10 assignment:** Validate entire pipeline against reference MATLAB implementation; document discrepancies (see docs/research/satinn-validation-plan.md)

**Issue links:** #8 (Cell classification), #9 (Validation)

**Data flow:**
```
Feature table + training labels
    ↓ [train classifier on subset]
Trained model
    ↓ [apply to all regions]
Predictions: region_id, cell_type (nucleus vs. cytoplasm), confidence
    ↓ [count by type]
Cell counts: {nucleus: 245, cytoplasm: 1823, ...}
    ↓ [compare to MATLAB reference]
Validation report: % agreement, mean error, discrepancies
```

---

### Stage 6: Extension and Independent Research (Weeks 11-12)

**What happens:** Tobe extends SATINN pipeline with independent research question.

**Purpose:** Apply research skills beyond reimplementation; create novel contribution.

**Weeks 11-12 Deliverables:**
- Propose novel analysis (e.g., identify cell clusters, measure spatial distributions)
- Implement extension on top of validated SATINN pipeline
- Present results in research proposal or poster

**Python modules involved:**
- Extension code: `satinn.extensions.tobe_research` (depends on all above)
- Analysis: clustering, statistical testing, visualization

**Week 11 assignment:** Finalize independent research hypothesis and methodology

**Week 12 assignment:** Complete and present internship research findings

**Issue links:** #14 (Independent research ideation), #15 (Research proposal)

**Data flow:**
```
Validated SATINN outputs (cell counts, features)
    ↓ [apply novel analysis method]
New insights: spatial patterns, cell clusters, correlations, ...
    ↓ [create visualizations and statistical tests]
Research findings + poster/paper
```

---

## Module Dependency Graph

```
satinn/
├── io.py (load images, read/write features)
│   ├── preprocessing.py (uses io.load_image)
│   │   ├── visualization.py (display results)
│   │   └── segmentation.py (uses preprocessed images)
│   │       ├── morphology.py (post-process segments)
│   │       └── features.py (extract from regions)
│   │           ├── classification.py (uses feature table)
│   │           │   └── validation.py (compare predictions)
│   │           └── extensions/ (depends on all above)
│
├── config.py (centralized parameters)
│   └── [imported by all modules]
│
└── tests/ (unit and integration tests)
    ├── test_io.py
    ├── test_preprocessing.py
    ├── test_segmentation.py
    ├── test_features.py
    └── test_classification.py
```

**Key principle:** Each module can be tested independently, but depends on outputs of earlier stages.

---

## Success Criteria by Week

| Week | Stage | Success Criteria | Issue |
|------|-------|------------------|-------|
| 1-2 | Setup | Data acquired, manifest created, 1 sample image loaded | #1-2 |
| 3-4 | Preprocessing | 5 images preprocessed, parameter choices documented | #3 |
| 5-6 | Segmentation | Segmented regions labeled, post-processing applied | #4-5 |
| 7-8 | Features | Feature table exported (.csv), 10+ features per region | #6-7 |
| 9-10 | Classification | Predictions made, validated against reference (>95% agreement goal) | #8-9 |
| 11-12 | Extension | Independent research findings presented | #14-15 |

---

## GitHub Issues Mapped to Stages

| Issue # | Title | Stage | Week | Prerequisite |
|---------|-------|-------|------|--------------|
| #1 | Setup research environment | 1 | 1 | None |
| #2 | Catalog dataset and create manifest | 1 | 2 | #1 |
| #3 | Implement preprocessing pipeline | 2 | 3-4 | #2 |
| #4 | Implement segmentation (watershed) | 3 | 5-6 | #3 |
| #5 | Post-processing and morphology | 3 | 6 | #4 |
| #6 | Extract morphological features | 4 | 7-8 | #5 |
| #7 | Validate feature extraction | 4 | 8 | #6 |
| #8 | Implement cell classification | 5 | 9-10 | #6 |
| #9 | Validate against MATLAB reference | 5 | 10 | #8 |
| #10 | Create visualization dashboard | Ongoing | Any | Any |
| #11 | Performance optimization | Ongoing | Any | Any |
| #12 | Documentation and tutorials | Ongoing | Any | Any |
| #13 | Code quality and testing | Ongoing | Any | Any |
| #14 | Independent research ideation | 6 | 11 | #9 |
| #15 | Research proposal and presentation | 6 | 12 | #14 |

---

## How Python Modules Build on Each Other

### Example: Processing One Image End-to-End

```python
# Example workflow that uses all modules

from satinn.io import load_image
from satinn.preprocessing import preprocess_image
from satinn.segmentation import segment_image
from satinn.morphology import clean_segmentation
from satinn.features import extract_features
from satinn.classification import predict_cell_types
from satinn.validation import compare_to_reference

# Week 1-2: Load raw image (io module)
image = load_image('data/raw/slide_001.tif')

# Week 3-4: Preprocess (preprocessing module)
preprocessed = preprocess_image(image, kernel_size=5)

# Week 5-6: Segment (segmentation + morphology)
segmented = segment_image(preprocessed)
cleaned = clean_segmentation(segmented, min_area=20)

# Week 7-8: Extract features (features module)
features_df = extract_features(cleaned, image)
# Output: DataFrame with columns [region_id, area, perimeter, eccentricity, ...]

# Week 9: Classify (classification module)
predictions = predict_cell_types(features_df, model=trained_classifier)
# Output: DataFrame with columns [region_id, predicted_type, confidence]

# Week 10: Validate (validation module)
report = compare_to_reference(predictions, reference_predictions)
# Output: % agreement, confusion matrix, error analysis
```

---

## Data Flow Visualization

```
Physical slides
    ↓ (scanning at pathology core)
Raw .tif images
    ↓ (satinn.io)
Loaded into memory, checked against manifest
    ↓ (satinn.preprocessing)
Normalized, blurred, thresholded → Binary masks
    ↓ (satinn.segmentation)
Marker detection, watershed → Labeled regions
    ↓ (satinn.morphology)
Remove artifacts, clean boundaries → Final segments
    ↓ (satinn.features)
Extract properties → Feature table (CSV)
    ↓ (satinn.classification)
Apply trained model → Cell type predictions
    ↓ (satinn.validation)
Compare to reference → Validation report
    ↓ (satinn.extensions)
Apply independent research method → Novel findings
```

---

## Checklist for Each Week

Before moving to the next stage, verify:

- [ ] All code for this stage is in place and tested
- [ ] Unit tests pass for all new functions
- [ ] Integration with previous stage verified (can load outputs)
- [ ] Parameters are documented in `satinn/config.py`
- [ ] Commit message includes issue number (#N)
- [ ] README updated with stage completion
- [ ] Processed outputs from this week saved with date/parameter labels
- [ ] Any deviations from plan documented in issue comments

---

## References

- Week assignments linked in issue descriptions
- Technical documentation: `docs/research/satinn-architecture.md`
- Validation methodology: `docs/research/satinn-validation-plan.md`
- Learning materials: `docs/learning/` (machine learning, reproducibility, computing)
