## WEEK 07: Modular Python Architecture Design

**Learning Objective:**
Design a clean, modular Python architecture for SATINN that separates concerns (image preprocessing, segmentation, feature extraction, model inference) and documents interfaces between modules.

**Why This Week Matters:**
Before writing code, you need a solid architecture. Good architecture makes code testable, reusable, and maintainable. This week focuses on planning: defining modules, their responsibilities, and how they communicate. A good design now prevents major refactoring later.

**Prerequisites:**
- Reference SATINN understanding from Week 05.
- Reference workflow execution and metrics from Week 06.
- Comfort with Python object-oriented programming basics (classes, methods, interfaces).
- Experience from Week 03 with module structure and imports.

**Expected Time Commitment:**
10-12 hours

**Learning Objectives:**
1. Define SATINN as a collection of independent modules.
2. Document the interface (inputs, outputs, parameters) for each module.
3. Create class hierarchies and abstract base classes for consistency.
4. Design configuration management (YAML/JSON configs for parameters).
5. Plan test stubs and mock objects for isolated testing.
6. Create architecture documentation with diagrams and pseudocode.
7. Get mentor feedback on the proposed design before implementation.

---

## Plan

### Step 1: Analyze Reference Implementation Structure (2–3 hours)

- [ ] **Map the reference codebase structure:**
  - SSH to Prime8: `ssh prime8`
  - Navigate to reference: `cd ~/work/satinn-project/satinn-ref`
  - Create a directory tree map:
    ```bash
    tree -I '__pycache__|*.pyc|.git' > ../codebase_structure.txt
    # or if tree is not available:
    find . -type f -name "*.py" | head -50
    ```
  - Identify main components:
    - File for image loading: `grep -l "imread\|open.*image" src/*.py`
    - File for preprocessing: `grep -l "normalize\|preprocess" src/*.py`
    - File for segmentation: `grep -l "segment\|threshold\|mask" src/*.py`
    - File for feature extraction: `grep -l "feature\|extract" src/*.py`
    - File for model/classification: `grep -l "model\|predict\|classify" src/*.py`

- [ ] **Document the reference architecture:**
  - For each major file/module, note:
    - What does it do?
    - What functions/classes does it define?
    - What are its inputs and outputs?
    - Does it have dependencies on other modules?
  - Example:
    ```markdown
    ## Reference SATINN Architecture

    ### Module: preprocessing.py
    - Functions:
      - `normalize_image(image, method='adaptive')`
      - `resize_image(image, target_size)`
    - Dependencies: cv2, numpy
    - Input: Raw image (uint8 array)
    - Output: Normalized image (float32 array, range [0, 1])

    ### Module: segmentation.py
    - Classes:
      - `TissueSegmenter` (abstract)
      - `ColorThresholdSegmenter` (implementation)
    - Input: Normalized image
    - Output: Binary mask (0=background, 255=tissue)
    ```

- [ ] **Identify design patterns:**
  - Does the reference use classes or functions?
  - Are there abstract base classes or interfaces?
  - How are parameters passed (direct args, config dictionaries, config files)?
  - How is the pipeline orchestrated (function calls, pipeline class, step-by-step)?

---

### Step 2: Define Module Boundaries and Responsibilities (2–3 hours)

- [ ] **List all SATINN modules you will implement:**
  - File: `architecture_modules.md`
  - Document:
    ```markdown
    # SATINN Python Implementation: Module Design

    ## Core Modules

    ### Module 1: Image Loading & Preprocessing
    **Responsibility:** Read histology images, normalize color and intensity, resize
    - Input: File path (TIFF, PNG, or similar)
    - Output: Normalized image array (float32, range [0, 1])
    - Key functions:
      - `load_image(filepath) -> ndarray`
      - `normalize_color(image) -> ndarray` (remove stain artifacts)
      - `normalize_intensity(image) -> ndarray` (scale intensity)
      - `resize_to_standard(image, target_size) -> ndarray`
    - Dependencies: cv2, PIL, numpy

    ### Module 2: Tissue Segmentation
    **Responsibility:** Identify tissue pixels vs. background/whitespace
    - Input: Preprocessed image
    - Output: Binary segmentation mask (0=background, 1=tissue)
    - Key classes:
      - `SegmentationStrategy` (abstract base class)
      - `ColorThresholdSegmentation` (implementation)
      - `KMeansSegmentation` (alternative implementation)
    - Hyperparameters: color thresholds, morphological operations
    - Dependencies: cv2, numpy, scipy

    ### Module 3: Feature Extraction
    **Responsibility:** Compute morphological, texture, and spatial features for tissue regions
    - Input: Preprocessed image + segmentation mask
    - Output: Feature matrix (n_regions × n_features)
    - Key classes:
      - `FeatureExtractor` (abstract)
      - `MorphologicalFeatures` (size, shape, circularity, solidity)
      - `TextureFeatures` (intensity variance, gradient, GLCM)
      - `SpatialFeatures` (neighbor relationships, density)
    - Hyperparameters: region size, feature window size
    - Dependencies: scikit-image, numpy, scipy

    ### Module 4: Model Inference
    **Responsibility:** Load trained model and make predictions on features
    - Input: Feature matrix + trained model
    - Output: Predictions/classifications for each region
    - Key classes:
      - `Model` (abstract interface for different model types)
      - `SKLearnModel` (scikit-learn classifier wrapper)
      - `MATLABModel` (interface to MATLAB-based models)
      - `NeuralNetworkModel` (optional: TensorFlow/PyTorch)
    - Responsibilities: Load model file, apply to features, return predictions
    - Dependencies: joblib, sklearn, tensorflow (optional)

    ### Module 5: Postprocessing & Output
    **Responsibility:** Format predictions, create output visualizations, save results
    - Input: Predictions, segmentation mask, original image
    - Output: Labeled image, CSV with region predictions, metrics
    - Key functions:
      - `create_prediction_map(predictions, segmentation_mask)`
      - `visualize_predictions(image, prediction_map, overlay=True)`
      - `save_predictions(predictions, output_path)`
      - `compute_metrics(predictions, ground_truth) -> dict`
    - Dependencies: cv2, matplotlib, numpy, pandas

    ### Module 6: Configuration Management
    **Responsibility:** Load and manage pipeline parameters from config files
    - Input: YAML/JSON config file
    - Output: Configuration object
    - Key classes:
      - `Config` (dataclass or dict wrapper)
      - `ConfigLoader` (YAML/JSON parsing)
    - Usage: `config = load_config('satinn_config.yaml')`
    - Dependencies: pyyaml, json

    ### Module 7: Pipeline Orchestration
    **Responsibility:** Coordinate execution of all modules in correct order
    - Input: Config file + image path
    - Output: Final predictions
    - Key class:
      - `SATINNPipeline`:
        - `__init__(config)`
        - `load_image(filepath)`
        - `preprocess()`
        - `segment()`
        - `extract_features()`
        - `predict()`
        - `postprocess()`
        - `run(image_path) -> results`
    - Responsibilities: Error handling, logging, progress reporting
    - Dependencies: All other modules

    ### Module 8: Validation & Testing
    **Responsibility:** Compare Python implementation against reference
    - Input: Python output + reference output
    - Output: Comparison metrics (absolute/relative differences)
    - Key functions:
      - `load_reference_output(filepath)`
      - `compare_numeric_outputs(output1, output2, tolerance)`
      - `compare_predictions(pred1, pred2, metric='accuracy')`
      - `generate_validation_report()`
    - Dependencies: numpy, scipy
    ```

- [ ] **Define dependencies between modules:**
  - Create a dependency graph:
    ```
    Image File
        ↓ [ImageLoader]
    Raw Image
        ↓ [Preprocessing]
    Preprocessed Image
        ├→ [Segmentation] → Segmentation Mask
        └→ [FeatureExtractor] → Feature Matrix
            ↓ [ModelInference]
        Predictions
            ↓ [Postprocessing]
        Final Output (visualizations, CSV, metrics)
    ```

---

### Step 3: Design Class Hierarchies and Interfaces (2–3 hours)

- [ ] **Create abstract base classes (ABCs):**
  - File: `satinn/core/interfaces.py`
  - Example pseudocode:
    ```python
    from abc import ABC, abstractmethod
    import numpy as np

    class ImageProcessor(ABC):
        """Abstract base for image processing steps."""
        
        @abstractmethod
        def process(self, image: np.ndarray) -> np.ndarray:
            """Process image and return result."""
            pass

    class Segmenter(ABC):
        """Abstract base for segmentation strategies."""
        
        @abstractmethod
        def segment(self, image: np.ndarray) -> np.ndarray:
            """Segment image, return binary mask."""
            pass

    class FeatureExtractor(ABC):
        """Abstract base for feature extraction."""
        
        @abstractmethod
        def extract(self, image: np.ndarray, mask: np.ndarray) -> np.ndarray:
            """Extract features from masked region, return feature vector."""
            pass

    class ModelInterface(ABC):
        """Abstract base for prediction models."""
        
        @abstractmethod
        def load(self, model_path: str):
            """Load trained model from file."""
            pass
        
        @abstractmethod
        def predict(self, features: np.ndarray) -> np.ndarray:
            """Make predictions on feature matrix."""
            pass

    class PipelineStep(ABC):
        """Generic pipeline step."""
        
        @abstractmethod
        def execute(self, input_data):
            """Execute this step on input data."""
            pass
    ```

- [ ] **Document inheritance hierarchy:**
  - File: `architecture_class_hierarchy.md`
  - Example:
    ```markdown
    ## Class Hierarchy

    ### ImageProcessor (ABC)
    ├── ColorNormalizer (implements ImageProcessor)
    ├── IntensityNormalizer (implements ImageProcessor)
    └── Resizer (implements ImageProcessor)

    ### Segmenter (ABC)
    ├── ColorThresholdSegmenter (implements Segmenter)
    ├── KMeansSegmenter (implements Segmenter)
    └── NeuralNetworkSegmenter (implements Segmenter, requires TensorFlow)

    ### FeatureExtractor (ABC)
    ├── MorphologicalExtractor (implements FeatureExtractor)
    ├── TextureExtractor (implements FeatureExtractor)
    └── SpatialExtractor (implements FeatureExtractor)

    ### ModelInterface (ABC)
    ├── SKLearnModel (implements ModelInterface)
    ├── MATLABModel (implements ModelInterface)
    └── TensorFlowModel (implements ModelInterface, optional)
    ```

---

### Step 4: Design Configuration and Parameter Management (1–2 hours)

- [ ] **Create a configuration schema:**
  - File: `satinn/config/satinn_config_schema.md`
  - Example:
    ```yaml
    # satinn_config.yaml
    # SATINN Pipeline Configuration

    pipeline:
      name: "SATINN Research Pipeline"
      version: "1.0.0"

    preprocessing:
      normalize_color: true
      color_method: "adaptive"  # or "histogram_equalization"
      normalize_intensity: true
      intensity_range: [0, 1]
      target_size: [2048, 2048]

    segmentation:
      strategy: "color_threshold"  # or "kmeans", "neural_network"
      color_threshold:
        lower: [0, 0, 0]
        upper: [255, 255, 255]
        morphology:
          operation: "close"  # or "open", "erode", "dilate"
          kernel_size: 5

    feature_extraction:
      morphological:
        enabled: true
        region_size: 100  # pixels
        features:
          - "area"
          - "perimeter"
          - "circularity"
          - "solidity"
          - "eccentricity"
      texture:
        enabled: true
        window_size: 50
        features:
          - "mean_intensity"
          - "std_intensity"
          - "entropy"
      spatial:
        enabled: true
        max_distance: 200  # pixels for neighbor analysis

    model:
      type: "sklearn"  # or "matlab", "tensorflow"
      model_path: "/path/to/trained_model.pkl"
      model_type: "LogisticRegression"  # or "RandomForest", "SVM", etc.

    output:
      save_prediction_map: true
      save_features_csv: true
      save_metrics_json: true
      visualization:
        overlay_predictions: true
        color_scheme: "viridis"  # or "grayscale", "hot", etc.

    validation:
      compare_with_reference: false
      reference_path: null
      tolerance_absolute: 0.001
      tolerance_relative: 0.01
    ```

- [ ] **Design configuration class:**
  - File: `satinn/core/config.py`
  - Pseudocode:
    ```python
    from dataclasses import dataclass
    import yaml
    from typing import Dict, List, Any

    @dataclass
    class PreprocessConfig:
        normalize_color: bool
        color_method: str
        normalize_intensity: bool
        target_size: tuple

    @dataclass
    class SegmentationConfig:
        strategy: str
        params: Dict[str, Any]

    @dataclass
    class SATINNConfig:
        preprocessing: PreprocessConfig
        segmentation: SegmentationConfig
        # ... more configs ...

        @classmethod
        def from_yaml(cls, filepath: str) -> 'SATINNConfig':
            """Load config from YAML file."""
            with open(filepath) as f:
                data = yaml.safe_load(f)
            return cls(**data)

        def to_yaml(self, filepath: str):
            """Save config to YAML file."""
            with open(filepath, 'w') as f:
                yaml.dump(self.__dict__, f)
    ```

---

### Step 5: Create Architecture Documentation with Diagrams (2–3 hours)

- [ ] **Create a comprehensive architecture document:**
  - File: `ARCHITECTURE.md`
  - Content:
    ```markdown
    # SATINN Python Implementation Architecture

    ## Overview
    The SATINN Python implementation is organized as a modular pipeline with the following 
    design principles:
    - Each module is independently testable
    - Modules communicate through well-defined interfaces
    - Configuration is externalized (YAML files)
    - Extensibility through inheritance and abstract base classes

    ## Module Dependency Graph
    [Include ASCII diagram or refer to diagram file]

    ## Key Design Patterns
    1. **Abstract Base Classes (ABC):** Define interfaces for pluggable implementations
    2. **Strategy Pattern:** Pluggable algorithms (e.g., SegmentationStrategy)
    3. **Factory Pattern:** Create instances based on config (e.g., SegmenterFactory)
    4. **Pipeline Pattern:** Orchestrate steps through SATINNPipeline class
    5. **Configuration Pattern:** Externalize parameters to YAML/JSON

    ## Data Flow
    ```
    Input Image File
        ↓ (ImageLoader)
    Raw Image (numpy array, uint8)
        ↓ (Preprocessing: ColorNormalizer + IntensityNormalizer)
    Preprocessed Image (float32, [0,1])
        ├→ (Segmentation)
        │  ↓
        │  Binary Mask (uint8, 0/1)
        │
        └→ (FeatureExtraction using mask)
           ↓
           Feature Matrix (n_regions × n_features)
               ↓ (ModelInference)
               Predictions (n_regions)
                   ↓ (Postprocessing)
                   Final Output:
                   - Prediction map (image)
                   - Features CSV
                   - Metrics JSON
    ```

    ## Error Handling Strategy
    - Input validation at each module entry
    - Informative error messages with context
    - Graceful degradation where possible (e.g., skip texture features if computation fails)
    - Logging of all major steps

    ## Testing Strategy
    - Unit tests for each module in isolation (using mock inputs)
    - Integration tests for pipeline steps (using real reference data)
    - Validation tests comparing against reference implementation
    ```

- [ ] **Create a visual architecture diagram:**
  - Use draw.io, Lucidchart, or create ASCII diagram.
  - Save as: `ARCHITECTURE_DIAGRAM.png` or `ARCHITECTURE_DIAGRAM.txt`
  - Include: modules, data flow, dependencies, configuration

- [ ] **Create sequence diagrams for key workflows:**
  - File: `WORKFLOW_SEQUENCE.md`
  - Pseudocode:
    ```
    User → Pipeline
        │ Load config
        │ Load image
        │ Preprocess (color + intensity norm)
        │ Segment (identify tissue)
        │ Extract features (morphological + texture + spatial)
        │ Predict (apply model to features)
        │ Postprocess (create visualizations + save outputs)
        └ Return results
    ```

---

### Step 6: Design Test Strategy and Mock Objects (1–2 hours)

- [ ] **Define test stubs for isolated testing:**
  - File: `satinn/testing/mocks.py`
  - Pseudocode:
    ```python
    import numpy as np

    class MockImage:
        """Create fake image data for testing."""
        @staticmethod
        def create_simple_image(size=(256, 256)):
            """Create a simple test image."""
            image = np.zeros(size + (3,), dtype=np.uint8)
            # Create a white square in center (tissue-like)
            image[64:192, 64:192] = 255
            return image

        @staticmethod
        def create_segmentation_mask(size=(256, 256)):
            """Create a mock segmentation mask."""
            mask = np.zeros(size, dtype=np.uint8)
            mask[64:192, 64:192] = 1
            return mask

    class MockModel:
        """Mock trained model for testing."""
        def predict(self, features):
            """Return deterministic predictions for testing."""
            n_samples = features.shape[0]
            # Alternate between class 0 and 1
            return np.array([i % 2 for i in range(n_samples)])

    class MockConfig:
        """Create a minimal test configuration."""
        def __init__(self):
            self.preprocessing = {'normalize': True}
            self.segmentation = {'strategy': 'color_threshold'}
            # ... other config ...
    ```

- [ ] **Define test plan:**
  - File: `TEST_PLAN.md`
  - Example:
    ```markdown
    # Test Strategy

    ## Unit Tests
    - Test each ImageProcessor independently
    - Test Segmenter with mock images
    - Test FeatureExtractor with mock masks
    - Test Model.predict with mock features

    ## Integration Tests
    - Test preprocessing pipeline (color → intensity normalization)
    - Test segmentation + feature extraction together
    - Test full pipeline on small reference dataset

    ## Validation Tests
    - Compare Python output with reference implementation
    - Verify numerical tolerances (e.g., features within 1% of reference)
    - Verify prediction accuracy (e.g., >90% match with reference)

    ## Performance Tests
    - Measure processing time per image
    - Monitor memory usage for large images
    - Profile bottlenecks using cProfile
    ```

---

### Step 7: Get Mentor Feedback and Iterate (1–2 hours)

- [ ] **Prepare architecture review package:**
  - Combine all documents:
    - `architecture_modules.md` (module responsibilities)
    - `architecture_class_hierarchy.md` (class design)
    - `ARCHITECTURE.md` (comprehensive guide)
    - `ARCHITECTURE_DIAGRAM.png` (visual)
    - `satinn_config_schema.md` (configuration)
    - `TEST_PLAN.md` (testing approach)

- [ ] **Email mentors for feedback:**
  - Subject: "Architecture Review for SATINN Python Implementation (Week 07)"
  - Content: "I have designed the modular architecture for SATINN Python reimplementation. Please review the attached documents and provide feedback on: (1) Module boundaries, (2) Class design, (3) Configuration approach, (4) Any missing components or dependencies."
  - Attach or link: All documents above.

- [ ] **Incorporate mentor feedback:**
  - Schedule a meeting or await async feedback.
  - Document changes: "Mentor feedback suggested: [Change 1], [Change 2]"
  - Update architecture documents accordingly.

- [ ] **Commit final architecture:**
  - Run: `git add ARCHITECTURE.md ARCHITECTURE_DIAGRAM.* architecture_*.md satinn_config_schema.md TEST_PLAN.md satinn/core/interfaces.py satinn/core/config.py satinn/testing/mocks.py`
  - Run: `git commit -m "Week 07: SATINN Python architecture design, interfaces, configuration schema, and test strategy"`
  - Run: `git push origin main`

---

## Deliverable

Document your architecture design in a GitHub comment or document:

```markdown
**Week 07 Architecture Design Completion**

- Core modules defined and documented: [8 modules]
- Module responsibilities clearly specified: [Yes / No]
- Abstract base classes designed for extensibility: [Yes / No]
- Class hierarchy documented with inheritance: [Yes / No]
- Configuration schema created (YAML): [Yes / No]
- Configuration loader class designed: [Yes / No]
- Pipeline orchestration class designed: [Yes / No]
- Data flow diagrams created: [Yes / No]
- Test strategy and mock objects planned: [Yes / No]
- Mentor feedback incorporated: [Yes / No]
```

---

## Objective Completion Criteria

✅ You have completed this week when:

1. You have defined 6-8 core modules with clear responsibilities.
2. You have documented interfaces (inputs, outputs) for each module.
3. You have designed abstract base classes for key module types.
4. You have created a class hierarchy with inheritance relationships.
5. You have designed configuration management (YAML schema + loader).
6. You have created architecture documentation with diagrams and pseudocode.
7. You have outlined a test strategy with mock objects.
8. You have received mentor feedback and incorporated improvements.
9. You are ready to implement the first modules (Week 08).

---

## Student Reflection Questions

Answer in a GitHub comment or your learning journal:

1. **Module Design:** How did you decide where module boundaries should be?
2. **Extensibility:** How would your design handle adding a new segmentation algorithm?
3. **Configuration:** Why externalize configuration to YAML rather than hardcoding parameters?
4. **Testing:** How would you test the segmentation module in isolation?
5. **Challenges:** What architectural decisions are you uncertain about?

---

## Mentor Review Checklist

- [ ] Tobe has defined clear module responsibilities aligned with SATINN algorithm.
- [ ] Tobe's module interfaces (inputs/outputs) are well-documented.
- [ ] Tobe has designed appropriate abstract base classes.
- [ ] Tobe's class hierarchy is extensible and follows Python best practices.
- [ ] Tobe's configuration management design is practical and flexible.
- [ ] Tobe's pipeline orchestration design is clear and testable.
- [ ] Tobe's documentation includes diagrams and pseudocode.
- [ ] Tobe has designed a comprehensive test strategy.
- [ ] Tobe's architecture is implementable without major redesign.
- [ ] Approve Tobe to begin implementation (Week 08: First Python Components).

---

## Optional Stretch Activities

- [ ] Research software architecture patterns (Strategy, Factory, Pipeline) and document examples.
- [ ] Create a UML class diagram using a tool like yEd or Lucidchart.
- [ ] Design API documentation (using Sphinx or similar) for your modules.
- [ ] Create a development roadmap: which modules to implement in which weeks.
- [ ] Design database schema for storing results (if persistence is needed).

---

## Links and Resources

- **Python Abstract Base Classes:** https://docs.python.org/3/library/abc.html
- **Design Patterns:** https://en.wikipedia.org/wiki/Software_design_pattern
- **YAML Tutorial:** https://en.wikipedia.org/wiki/YAML
- **Architecture Documentation Tools:** https://www.draw.io/, https://www.lucidchart.com/
- **Python Best Practices:** https://pep8.org/, https://google.github.io/styleguide/pyguide.html

---

## Related Epics

- **SATINN Research Track:** Week 07 architecture determines the quality and maintainability of weeks 08-12 implementation.
- **Software Engineering:** Demonstrates best practices in software design and documentation.
