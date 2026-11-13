# Experiment Log Template

**Purpose:** Record experimental sessions for reproducibility and tracking  
**Use this template:** Each time you run SATINN pipeline or analysis  

---

## Experiment Log Entry

### Header
- **Date:** YYYY-MM-DD
- **Time:** HH:MM start - HH:MM end
- **Week:** [Week number]
- **Stage:** [preprocessing/segmentation/features/classification/analysis]
- **Researcher:** Tobe

### Objective
What are you trying to accomplish in this session? (1-2 sentences)

Example: "Apply preprocessing to all 20 validation images and verify outputs match MATLAB reference."

---

### Input Data
- **Dataset:** [e.g., validation_set_Week10]
- **Number of images:** [e.g., 20]
- **Image format:** TIFF, 2048×2048, 8-bit grayscale
- **Data location:** `/data/satinn/validation_set_Week10/`
- **Data integrity check:** MD5 hashes verified: ✓ (or ✗ and describe issue)

---

### Parameters Used
Document every parameter (or link to config file). Example:

```yaml
PREPROCESSING:
  gaussian_kernel_size: 5
  gaussian_sigma: 0
  threshold_method: 'otsu'
  clahe_enabled: false

RANDOM_SEED: 42
```

Or link: "See `config_validation.yaml` (commit: abc1234)"

---

### Procedure
What did you do? (Step-by-step or link to code)

Example:
1. Loaded all 20 images from validation_set_Week10
2. Applied preprocessing pipeline to each image
3. Saved preprocessed images to `/data/users/username/python_outputs/`
4. Logged processing time per image
5. Ran validation comparison script (see validation_compare.py)

---

### Outputs
- **Number of images processed:** [e.g., 20/20]
- **Output location:** `/data/users/username/python_outputs/`
- **Output files:** 
  - `slide_001_validated_preprocessed.tif` ... `slide_020_validated_preprocessed.tif`
  - `preprocessing_log.txt`
  - `validation_summary.json`

### Output Summary
```json
{
  "total_images": 20,
  "successful": 20,
  "failed": 0,
  "total_time_seconds": 127.3,
  "mean_time_per_image": 6.4,
  "preprocessing_method": "gaussian_blur + otsu_threshold",
  "random_seed": 42
}
```

---

### Key Results
What were the main findings? (Copy relevant metrics)

**Example for preprocessing validation:**
```
PREPROCESSING VALIDATION RESULTS
All 20 images compared to MATLAB reference:
  Max pixel difference: 0-1 (all images)
  Mean pixel difference: 0.034
  Status: PASS (within tolerance ± 1 pixel)
```

**Example for segmentation:**
```
SEGMENTATION RESULTS
All 20 validation images segmented:
  Mean Dice coefficient: 0.9612
  Mean Jaccard index: 0.9241
  Region counts: MATLAB avg 1287, Python avg 1289 (0.2% difference)
  Status: PASS (Dice > 0.95 for all images)
```

---

### Observations and Notes
Any unexpected findings? Issues encountered? Solutions applied?

Example:
```
- Image slide_015 had lower Dice (0.91) than others; investigated:
  * Cause: Very low contrast in original image
  * MATLAB used adaptive thresholding here; Python used Otsu
  * Solution: Add adaptive threshold option to preprocessing
  
- Processing time ranged 5-8 seconds per image
  * Slower images had more regions (more complex segmentation)
  * Performance is acceptable for batch processing
  
- All outputs successfully saved and logged
```

---

### Blockers or Issues
If something didn't work:
- **Issue:** [Description]
- **Error message:** [If applicable]
- **Attempted solution:** [What you tried]
- **Resolution:** [How it was fixed or action for next session]
- **Impact:** [Does this affect downstream work?]

Example:
```
Issue: Image slide_012 failed to segment
Error: "watershed: unsupported parameter type"
Cause: Input image had int32 instead of uint8 dtype
Solution: Added dtype conversion in preprocessing module
Impact: None (was preprocessing bug, now fixed)
```

---

### Code and Commits
Link to relevant code:
- **Script used:** `satinn/preprocess_images.py` (commit: abc1234)
- **Config file:** `config_validation.yaml` (commit: abc1234)
- **Validation script:** `validation/compare_preprocessing.py` (commit: abc1234)

**Git commit for this session's outputs:**
```bash
git add data/preprocessed_validation_set/ logs/preprocessing_log.txt
git commit -m "Validate preprocessing on 20 validation images

- All images preprocessed with parameters: kernel=5, threshold=otsu
- Validation: Dice > 0.95 for all images vs MATLAB reference
- Max pixel difference: 1 (acceptable)
- Processing time: 127 seconds total
- Issue: #5"
```

---

### Next Steps
What should happen next? Any follow-up experiments?

Example:
```
- PASS: Preprocessing stage complete and validated
- Next: Proceed to segmentation validation (Week 6)
- Action: Run segmentation pipeline on preprocessed images from this session
```

---

## Example: Complete Experiment Log Entry

```
====================================================================
EXPERIMENT LOG: Preprocessing Validation Session
====================================================================

Header
Date:      2024-10-22
Time:      14:30 - 15:45
Week:      6
Stage:     Preprocessing validation
Researcher: Tobe

Objective
Validate that Python preprocessing produces outputs equivalent to 
MATLAB reference on validation dataset. Target: all images with 
max pixel difference ≤ 1, mean error < 0.1%.

Input Data
Dataset:   validation_set_Week10
Count:     20 images
Format:    TIFF, 2048×2048, 8-bit grayscale
Location:  /data/satinn/validation_set_Week10/
MD5 check: ✓ All hashes verified against MANIFEST.md

Parameters Used
See config_validation.yaml (commit: 3f8a5c7)
Key settings:
  - Gaussian blur: kernel=5, sigma=0
  - Threshold: otsu (automatic)
  - CLAHE: disabled
  - Random seed: 42

Procedure
1. Pulled latest SATINN code (commit: 3f8a5c7)
2. Activated environment: conda activate satinn-dev
3. Ran preprocessing on all 20 images:
   python -m satinn.preprocess \
     --input-dir /data/satinn/validation_set_Week10 \
     --output-dir ./python_outputs \
     --config config_validation.yaml
4. Ran validation comparison script:
   python validation/compare_preprocessing.py \
     --matlab-dir /data/satinn/reference_outputs \
     --python-dir ./python_outputs
5. Generated validation report

Outputs
Location: /data/users/tobe/satinn_work/session_20241022/
Files:
  - python_outputs/slide_001_preprocessed.tif to slide_020_preprocessed.tif
  - preprocessing_log.txt (127 seconds total, 6.4 sec/image)
  - validation_report.txt

Output Summary
{
  "total_images": 20,
  "successful": 20,
  "failed": 0,
  "total_time_seconds": 127.3,
  "mean_time_per_image": 6.4,
  "max_pixel_diff": 1,
  "mean_pixel_diff": 0.034,
  "pixels_exceeding_tolerance": 0,
  "validation_status": "PASS"
}

Key Results
Preprocessing validation PASSED for all 20 images:
  - Max pixel difference: 1 (within tolerance of ±1)
  - Mean pixel difference: 0.034 (well under 0.1%)
  - All processing completed successfully
  - Processing time: ~6.4 seconds per image (reasonable)

Detailed results per image:
  slide_001: max_diff=1, mean_diff=0.012
  slide_002: max_diff=1, mean_diff=0.008
  ...
  slide_020: max_diff=1, mean_diff=0.031

Observations and Notes
- Preprocessing outputs match MATLAB very closely
- Slight differences in pixel values (±1) are expected and acceptable
- All images processed without errors
- Preprocessing is ready for downstream stages

Blockers or Issues
None. All images processed successfully.

Code and Commits
Scripts used:
  - satinn/preprocess_images.py (commit: 3f8a5c7)
  - config_validation.yaml (commit: 3f8a5c7)
  - validation/compare_preprocessing.py (commit: 3f8a5c7)

Commit for this session:
  git add python_outputs/ logs/preprocessing_log.txt
  git commit -m "Validate preprocessing on 20 validation images
  
  - All images preprocessed with kernel=5, threshold=otsu
  - Validation: max pixel diff=1, mean diff=0.034
  - Status: PASS (all images)
  - Processing time: 127 seconds
  - Issue: #3"

Next Steps
- PASS: Preprocessing stage validated, ready to proceed
- Next: Segmentation validation (Week 6)
- Action: Process preprocessed images through segmentation pipeline
- Timeline: Complete segmentation by end of Week 6
```

---

## Tips for Effective Experiment Logs

1. **Complete immediately after session** – Don't wait; details fade
2. **Include exact file paths** – Future you will search for this data
3. **Copy actual output, not summaries** – Machine-readable logs are more useful
4. **Link to code commits** – Reproducibility depends on knowing exactly which code ran
5. **Record both success and failure** – Failed experiments teach you what to avoid
6. **Use timestamps** – Helps with performance analysis
7. **Note any deviations from plan** – Essential for understanding results
8. **Be specific about parameters** – Magic numbers should be documented

---

## Version Control Note

After completing an experiment session:

1. **Save log to file** (e.g., `logs/experiment_20241022_preprocessing.txt`)
2. **Add to Git:**
   ```bash
   git add logs/experiment_20241022_preprocessing.txt
   git add data/outputs_from_this_session/
   git commit -m "Session 2024-10-22: Preprocessing validation

   - See logs/experiment_20241022_preprocessing.txt for details
   - Outputs in data/outputs_from_this_session/
   - Status: [PASS/FAIL]"
   ```
3. **Push to GitHub:**
   ```bash
   git push origin main
   ```

This creates an auditable history of your work.

---

## Searching Your Logs Later

If you need to find old experiments:

```bash
# Find all logs
ls logs/experiment_*.txt

# Find logs for specific stage
grep -l "Stage: segmentation" logs/experiment_*.txt

# Find passing experiments
grep "PASS" logs/experiment_*.txt

# Show timeline of preprocessing validation
grep -h "Date:" logs/experiment_*preprocessing*.txt
```

---

## Template Checklist

Before finishing each session, verify you've completed:

- [ ] Header filled in (date, time, week, stage)
- [ ] Objective is clear
- [ ] Input data documented (location, count, format)
- [ ] Parameters explicitly listed (no magic numbers)
- [ ] Procedure is reproducible (could someone else repeat it?)
- [ ] Outputs are documented (location, files, format)
- [ ] Key results summarized (metrics, status)
- [ ] Observations recorded (unexpected findings, issues)
- [ ] Blockers documented (if any)
- [ ] Code/commits linked
- [ ] Next steps specified
- [ ] Log saved to file
- [ ] Changes committed to Git

---

## References

- Lab notebook best practices: https://www.nih.gov/grants-funding/grants-guidance/grant-application-process/electronic-research-administration/ther-commons
- Research reproducibility: https://www.protocols.io/
- Git workflow: https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository
