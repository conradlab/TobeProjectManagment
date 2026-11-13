## WEEK 08: First Python Components - Image Processing & Segmentation

**Learning Objective:**
Implement the first working Python components for SATINN: image loading, preprocessing, and tissue segmentation. Write unit tests and create your first GitHub PR with mentor review.

**Why This Week Matters:**
This is your first implementation week. You take the architecture from Week 07 and build real, testable code. You'll practice the Python/Git workflow from Week 03, and mentors will review your code quality, documentation, and test coverage.

**Prerequisites:**
- Architecture design from Week 07 (interfaces, modules, configuration).
- Python, Git, and GitHub competency from Week 03.
- Reference SATINN workflow understanding from Weeks 05-06.
- Virtual environment set up on Prime8 from Week 03.

**Expected Time Commitment:**
12-14 hours

**Learning Objectives:**
1. Implement image loading with proper error handling and logging.
2. Implement color and intensity normalization (preprocessing).
3. Implement tissue segmentation using color thresholding.
4. Create comprehensive unit tests with mock images.
5. Write clear docstrings and type hints.
6. Create and respond to mentor code review feedback.
7. Commit working code to a PR with reproducible examples.

---

## Plan

### Step 1: Set Up Project Structure and Base Classes (1–2 hours)

- [ ] **Create the Python package structure:**
  - SSH to Prime8: `ssh prime8`
  - Navigate to repo: `cd ~/work/satinn-project/satinn-pipeline`
  - Create directory structure:
    ```bash
    mkdir -p satinn/{core,preprocessing,segmentation,features,models,output,testing,config}
    touch satinn/__init__.py
    touch satinn/core/__init__.py satinn/core/interfaces.py satinn/core/exceptions.py
    touch satinn/preprocessing/__init__.py satinn/preprocessing/processors.py
    touch satinn/segmentation/__init__.py satinn/segmentation/strategies.py
    touch satinn/testing/__init__.py satinn/testing/mocks.py satinn/testing/utils.py
    ```

- [ ] **Implement abstract base classes (from Week 07 design):**
  - Edit: `satinn/core/interfaces.py`
  - Pseudocode to implement:
    ```python
    from abc import ABC, abstractmethod
    import numpy as np
    from typing import Tuple

    class ImageProcessor(ABC):
        """Abstract base for image processing operations."""
        
        @abstractmethod
        def process(self, image: np.ndarray) -> np.ndarray:
            """Process an image and return result."""
            pass
        
        def __call__(self, image: np.ndarray) -> np.ndarray:
            """Allow calling as function: processor(image)."""
            return self.process(image)

    class Segmenter(ABC):
        """Abstract base for tissue segmentation."""
        
        @abstractmethod
        def segment(self, image: np.ndarray) -> np.ndarray:
            """Segment image, return binary mask (0=background, 1=tissue)."""
            pass
    ```

- [ ] **Create custom exceptions:**
  - Edit: `satinn/core/exceptions.py`
  - Content:
    ```python
    class SATINNException(Exception):
        """Base exception for SATINN errors."""
        pass

    class ImageLoadError(SATINNException):
        """Error loading image file."""
        pass

    class PreprocessingError(SATINNException):
        """Error during preprocessing."""
        pass

    class SegmentationError(SATINNException):
        """Error during segmentation."""
        pass

    class ConfigurationError(SATINNException):
        """Error with configuration."""
        pass
    ```

---

### Step 2: Implement Image Loading and Preprocessing (3–4 hours)

- [ ] **Implement image loader:**
  - Edit: `satinn/preprocessing/processors.py`
  - Implement:
    ```python
    import cv2
    import numpy as np
    from pathlib import Path
    from typing import Union
    from satinn.core.interfaces import ImageProcessor
    from satinn.core.exceptions import ImageLoadError, PreprocessingError

    class ImageLoader:
        """Load histology images from disk."""
        
        SUPPORTED_FORMATS = {'.tif', '.tiff', '.png', '.jpg', '.jpeg'}
        
        @staticmethod
        def load(filepath: Union[str, Path]) -> np.ndarray:
            """
            Load image from file.
            
            Args:
                filepath: Path to image file
                
            Returns:
                Image as numpy array (uint8, shape: H×W×C or H×W)
                
            Raises:
                ImageLoadError: If file not found or format not supported
            """
            filepath = Path(filepath)
            
            # Verify file exists
            if not filepath.exists():
                raise ImageLoadError(f"File not found: {filepath}")
            
            # Verify format supported
            if filepath.suffix.lower() not in ImageLoader.SUPPORTED_FORMATS:
                raise ImageLoadError(f"Unsupported format: {filepath.suffix}")
            
            # Load image
            try:
                image = cv2.imread(str(filepath))
                if image is None:
                    raise ImageLoadError(f"Failed to load image: {filepath}")
                # OpenCV loads as BGR; convert to RGB
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                return image
            except Exception as e:
                raise ImageLoadError(f"Error loading {filepath}: {str(e)}")
    ```

- [ ] **Implement color normalization:**
  - Add to `satinn/preprocessing/processors.py`:
    ```python
    class ColorNormalizer(ImageProcessor):
        """Normalize image colors to reduce staining artifacts."""
        
        def __init__(self, method: str = 'adaptive'):
            """
            Initialize color normalizer.
            
            Args:
                method: Normalization method ('adaptive', 'histogram', 'none')
            """
            self.method = method
            if method not in {'adaptive', 'histogram', 'none'}:
                raise PreprocessingError(f"Unknown method: {method}")
        
        def process(self, image: np.ndarray) -> np.ndarray:
            """Normalize color in image."""
            if self.method == 'none':
                return image.astype(np.float32) / 255.0
            
            elif self.method == 'adaptive':
                # Normalize each color channel independently
                normalized = np.zeros_like(image, dtype=np.float32)
                for c in range(image.shape[2]):
                    channel = image[:, :, c].astype(np.float32)
                    channel_min = channel.min()
                    channel_max = channel.max()
                    if channel_max > channel_min:
                        normalized[:, :, c] = (channel - channel_min) / (channel_max - channel_min)
                    else:
                        normalized[:, :, c] = 0
                return normalized
            
            elif self.method == 'histogram':
                # Histogram equalization per channel
                normalized = np.zeros_like(image, dtype=np.float32)
                for c in range(image.shape[2]):
                    channel = image[:, :, c]
                    eq_channel = cv2.equalizeHist(channel)
                    normalized[:, :, c] = eq_channel.astype(np.float32) / 255.0
                return normalized
            
            return image.astype(np.float32) / 255.0
    ```

- [ ] **Implement intensity normalization:**
  - Add to `satinn/preprocessing/processors.py`:
    ```python
    class IntensityNormalizer(ImageProcessor):
        """Normalize pixel intensity values to standard range."""
        
        def __init__(self, output_range: Tuple[float, float] = (0.0, 1.0)):
            """
            Initialize intensity normalizer.
            
            Args:
                output_range: Target range (min, max)
            """
            self.output_min, self.output_max = output_range
        
        def process(self, image: np.ndarray) -> np.ndarray:
            """Normalize intensity values."""
            # Ensure float
            image_float = image.astype(np.float32)
            
            # Get current min/max
            img_min = image_float.min()
            img_max = image_float.max()
            
            # Avoid division by zero
            if img_max == img_min:
                return np.full_like(image_float, self.output_min)
            
            # Normalize to [0, 1]
            normalized = (image_float - img_min) / (img_max - img_min)
            
            # Scale to output range
            normalized = normalized * (self.output_max - self.output_min) + self.output_min
            
            return normalized.astype(np.float32)
    ```

- [ ] **Implement image resizer:**
  - Add to `satinn/preprocessing/processors.py`:
    ```python
    class ImageResizer(ImageProcessor):
        """Resize image to standard dimensions."""
        
        def __init__(self, target_size: Tuple[int, int] = (2048, 2048)):
            """Initialize resizer."""
            self.target_size = target_size
        
        def process(self, image: np.ndarray) -> np.ndarray:
            """Resize image to target dimensions."""
            if image.shape[:2] == self.target_size:
                return image  # Already correct size
            
            resized = cv2.resize(image, (self.target_size[1], self.target_size[0]), 
                                interpolation=cv2.INTER_LINEAR)
            return resized
    ```

- [ ] **Test preprocessing locally with mock data:**
  - Create a test script: `test_preprocessing_manual.py`
  - Content:
    ```python
    import numpy as np
    import matplotlib.pyplot as plt
    from satinn.preprocessing.processors import (
        ColorNormalizer, IntensityNormalizer, ImageResizer
    )
    from satinn.testing.mocks import MockImage

    # Create mock image
    image = MockImage.create_simple_image(size=(512, 512))
    print(f"Original image shape: {image.shape}, dtype: {image.dtype}")
    print(f"Value range: [{image.min()}, {image.max()}]")

    # Test color normalization
    color_norm = ColorNormalizer(method='adaptive')
    normalized = color_norm.process(image)
    print(f"After color norm: dtype={normalized.dtype}, range=[{normalized.min():.3f}, {normalized.max():.3f}]")

    # Test intensity normalization
    intensity_norm = IntensityNormalizer()
    normalized2 = intensity_norm.process(normalized)
    print(f"After intensity norm: dtype={normalized2.dtype}, range=[{normalized2.min():.3f}, {normalized2.max():.3f}]")

    # Test resizing
    resizer = ImageResizer(target_size=(256, 256))
    resized = resizer.process(normalized2)
    print(f"After resize: shape={resized.shape}")
    ```

---

### Step 3: Implement Tissue Segmentation (2–3 hours)

- [ ] **Implement color threshold segmentation:**
  - Edit: `satinn/segmentation/strategies.py`
  - Content:
    ```python
    import cv2
    import numpy as np
    from typing import Tuple
    from satinn.core.interfaces import Segmenter

    class ColorThresholdSegmenter(Segmenter):
        """Segment tissue using color thresholding."""
        
        def __init__(self, 
                     lower_color: Tuple[int, int, int] = (0, 0, 0),
                     upper_color: Tuple[int, int, int] = (255, 200, 200),
                     morphology_kernel_size: int = 5):
            """
            Initialize segmenter with thresholds.
            
            Args:
                lower_color: RGB lower bound for tissue detection
                upper_color: RGB upper bound for tissue detection
                morphology_kernel_size: Size of kernel for morphological operations
            """
            self.lower_color = np.array(lower_color, dtype=np.uint8)
            self.upper_color = np.array(upper_color, dtype=np.uint8)
            self.kernel_size = morphology_kernel_size
            self.kernel = cv2.getStructuringElement(
                cv2.MORPH_ELLIPSE, (morphology_kernel_size, morphology_kernel_size)
            )
        
        def segment(self, image: np.ndarray) -> np.ndarray:
            """
            Segment tissue from background using color thresholding.
            
            Args:
                image: Input image (uint8, RGB)
                
            Returns:
                Binary mask (uint8, values: 0 or 255)
            """
            # Ensure input is uint8
            if image.dtype != np.uint8:
                image = (image * 255).astype(np.uint8) if image.max() <= 1 else image.astype(np.uint8)
            
            # Create binary mask using color thresholding
            mask = cv2.inRange(image, self.lower_color, self.upper_color)
            
            # Apply morphological operations to clean up
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel)
            
            return mask
    ```

---

### Step 4: Create Comprehensive Unit Tests (2–3 hours)

- [ ] **Create mock objects:**
  - Edit: `satinn/testing/mocks.py`
  - Implement MockImage and MockConfig (from Week 07 planning)

- [ ] **Create unit test file:**
  - Create: `tests/test_preprocessing.py`
  - Content:
    ```python
    import pytest
    import numpy as np
    from satinn.preprocessing.processors import (
        ColorNormalizer, IntensityNormalizer, ImageResizer, ImageLoader
    )
    from satinn.testing.mocks import MockImage
    from satinn.core.exceptions import ImageLoadError

    class TestColorNormalizer:
        def test_adaptive_normalization(self):
            image = MockImage.create_simple_image()
            normalizer = ColorNormalizer(method='adaptive')
            result = normalizer.process(image)
            
            assert result.dtype == np.float32
            assert result.shape == image.shape
            assert result.min() >= 0.0
            assert result.max() <= 1.0
        
        def test_normalization_modes(self):
            image = MockImage.create_simple_image()
            for method in ['adaptive', 'histogram', 'none']:
                normalizer = ColorNormalizer(method=method)
                result = normalizer.process(image)
                assert result is not None
    
    class TestIntensityNormalizer:
        def test_intensity_range(self):
            image = np.random.randint(0, 256, size=(100, 100, 3), dtype=np.uint8)
            normalizer = IntensityNormalizer(output_range=(0, 1))
            result = normalizer.process(image)
            
            assert result.min() >= 0.0
            assert result.max() <= 1.0
        
        def test_custom_output_range(self):
            image = MockImage.create_simple_image()
            normalizer = IntensityNormalizer(output_range=(0, 100))
            result = normalizer.process(image)
            
            assert result.min() >= 0
            assert result.max() <= 100
    
    class TestImageResizer:
        def test_resize(self):
            image = MockImage.create_simple_image(size=(512, 512))
            resizer = ImageResizer(target_size=(256, 256))
            result = resizer.process(image)
            
            assert result.shape[:2] == (256, 256)
        
        def test_no_resize_if_already_correct(self):
            image = MockImage.create_simple_image(size=(256, 256))
            resizer = ImageResizer(target_size=(256, 256))
            result = resizer.process(image)
            
            np.testing.assert_array_equal(result, image)
    ```

- [ ] **Create tests for segmentation:**
  - Create: `tests/test_segmentation.py`
  - Content:
    ```python
    import pytest
    import numpy as np
    from satinn.segmentation.strategies import ColorThresholdSegmenter
    from satinn.testing.mocks import MockImage

    class TestColorThresholdSegmenter:
        def test_segmentation_output_shape(self):
            image = MockImage.create_simple_image()
            segmenter = ColorThresholdSegmenter()
            mask = segmenter.segment(image)
            
            assert mask.shape[:2] == image.shape[:2]
            assert mask.dtype == np.uint8
        
        def test_segmentation_binary_values(self):
            image = MockImage.create_simple_image()
            segmenter = ColorThresholdSegmenter()
            mask = segmenter.segment(image)
            
            unique_values = np.unique(mask)
            assert set(unique_values).issubset({0, 255})
        
        def test_segmentation_detects_tissue(self):
            image = MockImage.create_simple_image()
            segmenter = ColorThresholdSegmenter()
            mask = segmenter.segment(image)
            
            # Mock image has white (tissue) in center, should have non-zero mask there
            center_mask = mask[64:192, 64:192]
            assert center_mask.sum() > 0
    ```

- [ ] **Run tests locally:**
  - Navigate to repo: `cd ~/work/satinn-project/satinn-pipeline`
  - Activate venv: `source venv/bin/activate`
  - Install pytest: `pip install pytest pytest-cov`
  - Run: `pytest tests/ -v --cov=satinn --cov-report=term-missing`
  - Verify all tests pass

---

### Step 5: Write Documentation and Docstrings (1–2 hours)

- [ ] **Add comprehensive docstrings:**
  - Already included in pseudocode above, but verify they follow Google or NumPy style.
  - Each class and function should document: purpose, arguments, returns, raises, examples.

- [ ] **Create module README:**
  - File: `satinn/preprocessing/README.md`
  - Content:
    ```markdown
    # Preprocessing Module

    ## Overview
    Image preprocessing for SATINN pipeline. Handles color normalization, intensity scaling, and resizing.

    ## Usage
    ```python
    from satinn.preprocessing.processors import ImageLoader, ColorNormalizer, IntensityNormalizer, ImageResizer

    # Load image
    image = ImageLoader.load('histology_slide.tif')

    # Apply preprocessing pipeline
    normalizer = ColorNormalizer(method='adaptive')
    intensity_norm = IntensityNormalizer()
    resizer = ImageResizer((2048, 2048))

    image = normalizer.process(image)
    image = intensity_norm.process(image)
    image = resizer.process(image)
    ```

    ## Components
    - `ImageLoader`: Load histology images from disk
    - `ColorNormalizer`: Normalize color channels
    - `IntensityNormalizer`: Scale intensity to standard range
    - `ImageResizer`: Resize image to standard dimensions
    ```

---

### Step 6: Create GitHub PR with Code Review Workflow (2–3 hours)

- [ ] **Create a feature branch:**
  - Run: `git checkout -b week08-image-preprocessing-segmentation`

- [ ] **Commit your changes:**
  - Run: `git add satinn/ tests/ && git commit -m "Week 08: Implement image preprocessing and tissue segmentation"`

- [ ] **Push to GitHub:**
  - Run: `git push origin week08-image-preprocessing-segmentation`

- [ ] **Create a Pull Request:**
  - Go to GitHub repository.
  - Click "Compare & pull request" for your new branch.
  - Title: "Week 08: Image Preprocessing and Tissue Segmentation"
  - Description:
    ```markdown
    ## Summary
    Implemented core preprocessing and segmentation modules for SATINN Python pipeline.

    ## Components Implemented
    - ImageLoader: Load histology images from TIFF/PNG/JPG
    - ColorNormalizer: Adaptive/histogram color normalization
    - IntensityNormalizer: Normalize pixel intensity to [0, 1]
    - ImageResizer: Resize to standard dimensions
    - ColorThresholdSegmenter: Tissue segmentation via color thresholding

    ## Testing
    - Unit tests for all components with mock data
    - Test coverage: 85%+
    - All tests pass: `pytest tests/test_preprocessing.py tests/test_segmentation.py -v`

    ## Validation
    - Preprocessing pipeline tested with mock images
    - Segmentation produces binary masks as expected
    - Error handling implemented for file I/O and configuration errors

    ## Related to
    Week 08 assignment in the research internship curriculum.
    ```

- [ ] **Respond to mentor feedback:**
  - Wait for review comments from Eisa or Don.
  - If they request changes:
    - Make edits locally in your feature branch.
    - Commit and push: `git add . && git commit -m "Address review feedback: ..." && git push origin week08-...`
    - The PR will update automatically.
    - Reply to each comment.

- [ ] **Merge the PR:**
  - Once approved, merge into main: `git merge week08-... && git push origin main`

---

## Deliverable

Document your implementation in a GitHub comment:

```markdown
**Week 08 Implementation Report**

- Image loading implemented with error handling: [Yes / No]
- Color normalization (3+ methods) implemented: [Yes / No]
- Intensity normalization implemented: [Yes / No]
- Image resizing implemented: [Yes / No]
- Tissue segmentation (color threshold) implemented: [Yes / No]
- Unit tests written for all components: [Yes / No]
- Test coverage (pytest): [XX%]
- All tests passing: [Yes / No]
- PR created and reviewed: [GitHub PR URL]
- Mentor feedback addressed: [Yes / No]
- Code merged to main: [Yes / No]
```

---

## Objective Completion Criteria

✅ You have completed this week when:

1. Image loader handles multiple formats with proper error handling.
2. Color normalization works with adaptive and histogram methods.
3. Intensity normalizer scales to standard [0, 1] range.
4. Image resizer handles various input sizes correctly.
5. Color threshold segmenter produces binary masks.
6. Unit tests cover all components (70%+ coverage).
7. All tests pass locally.
8. PR is created with clear description and test results.
9. Mentor feedback is incorporated.
10. Code is merged and ready for Week 09 (feature extraction).

---

## Student Reflection Questions

Answer in a GitHub comment:

1. **Testing:** Why is unit testing important for preprocessing? What edge cases did you handle?
2. **Error Handling:** What errors could occur in image loading? How did you handle them?
3. **Type Hints:** How do type hints improve code clarity and IDE support?
4. **Code Review:** What feedback did you receive from mentors? What did you improve?
5. **Next Steps:** What challenges do you anticipate in feature extraction (Week 09)?

---

## Mentor Review Checklist

- [ ] Tobe's image loading handles TIFF, PNG, JPG correctly.
- [ ] Tobe's color normalization implements 2+ methods.
- [ ] Tobe's intensity normalization produces expected output range.
- [ ] Tobe's segmentation produces valid binary masks.
- [ ] Tobe's error handling is comprehensive (file not found, format errors, etc).
- [ ] Tobe's unit tests are thorough (70%+ coverage).
- [ ] Tobe's code follows Python style guidelines (PEP 8).
- [ ] Tobe's docstrings are complete and clear.
- [ ] Tobe's PR description is informative with test results.
- [ ] Tobe incorporated feedback professionally.
- [ ] Approve Tobe to proceed to Week 09 (Feature Extraction & Model Integration).

---

## Optional Stretch Activities

- [ ] Implement additional color normalization methods (Macenko, Reinhard stain normalization).
- [ ] Add image visualization functions (matplotlib integration).
- [ ] Implement alternative segmentation methods (morphological operations, K-means).
- [ ] Add performance profiling to identify bottlenecks.
- [ ] Create integration tests combining all preprocessing steps.

---

## Links and Resources

- **OpenCV Documentation:** https://docs.opencv.org/
- **NumPy Arrays:** https://numpy.org/doc/stable/reference/arrays.ndarray.html
- **Pytest Documentation:** https://docs.pytest.org/
- **Python Type Hints:** https://www.python.org/dev/peps/pep-0484/
- **PEP 8 Style Guide:** https://pep8.org/

---

## Related Epics

- **SATINN Research Track:** First implementation week; foundation for Weeks 09-12.
- **Software Development:** Practice for professional-grade code with tests and review.
