## WEEK 09: Feature Extraction & Model Integration

**Learning Objective:**
Implement feature extraction modules (morphological, texture, spatial) and integrate trained model inference to complete the SATINN computational pipeline from image to predictions.

**Why This Week Matters:**
Feature extraction is the bridge between raw images and machine learning models. Well-designed features make models work better. This week combines Weeks 08 (preprocessing/segmentation) with model inference to create a functioning end-to-end pipeline.

**Prerequisites:**
- Image preprocessing and segmentation from Week 08.
- ML foundations and model evaluation from Week 04.
- Reference SATINN feature list from Week 05.
- Access to a trained model (from reference implementation or mentors).

**Expected Time Commitment:**
12-14 hours

**Learning Objectives:**
1. Implement morphological feature extraction (size, shape, circularity).
2. Implement texture feature extraction (intensity, gradient, pattern).
3. Implement spatial feature extraction (neighbor relationships).
4. Load and integrate a trained machine learning model.
5. Create feature + model integration tests.
6. Write configuration system for model parameters.
7. Create documentation with feature definitions and examples.

---

## Plan

### Step 1: Implement Morphological Feature Extraction (3–4 hours)

- [ ] **Implement morphological features module:**
  - Create: `satinn/features/morphological.py`
  - Content:
    ```python
    import numpy as np
    from scipy import ndimage
    from typing import Dict
    from satinn.core.interfaces import FeatureExtractor

    class MorphologicalFeatures(FeatureExtractor):
        """Extract morphological features from tissue regions."""
        
        def __init__(self, region_size: int = 100):
            """
            Initialize morphological feature extractor.
            
            Args:
                region_size: Size of analysis regions (pixels)
            """
            self.region_size = region_size
        
        def extract(self, image: np.ndarray, mask: np.ndarray) -> np.ndarray:
            """
            Extract morphological features from segmented tissue.
            
            Args:
                image: Preprocessed image
                mask: Binary segmentation mask
                
            Returns:
                Feature matrix (n_regions × n_features)
            """
            # Label connected components
            labeled, n_regions = ndimage.label(mask)
            
            features = []
            feature_names = []
            
            for region_id in range(1, n_regions + 1):
                region_mask = (labeled == region_id)
                
                # Area
                area = np.sum(region_mask)
                
                # Centroid
                cy, cx = ndimage.center_of_mass(region_mask)
                
                # Perimeter (approximated)
                perimeter = self._compute_perimeter(region_mask)
                
                # Circularity = 4π·Area/Perimeter²
                if perimeter > 0:
                    circularity = (4 * np.pi * area) / (perimeter ** 2)
                else:
                    circularity = 0
                
                # Solidity = Area / Convex Hull Area
                solidity = self._compute_solidity(region_mask)
                
                # Eccentricity (elongation)
                eccentricity = self._compute_eccentricity(region_mask)
                
                features.append([area, perimeter, circularity, solidity, eccentricity])
            
            feature_names = ['area', 'perimeter', 'circularity', 'solidity', 'eccentricity']
            
            return np.array(features, dtype=np.float32)
        
        @staticmethod
        def _compute_perimeter(mask: np.ndarray) -> float:
            """Approximate perimeter using Sobel operator."""
            sx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
            sy = sx.T
            
            grad_x = ndimage.convolve(mask.astype(np.float32), sx)
            grad_y = ndimage.convolve(mask.astype(np.float32), sy)
            
            perimeter = np.sum(np.sqrt(grad_x**2 + grad_y**2))
            return perimeter
        
        @staticmethod
        def _compute_solidity(mask: np.ndarray) -> float:
            """Compute solidity (area / convex hull area)."""
            try:
                from scipy.spatial import ConvexHull
                # Get coordinates of object pixels
                coords = np.argwhere(mask)
                if len(coords) < 4:
                    return 1.0
                hull = ConvexHull(coords)
                hull_area = hull.volume  # In 2D, volume is actually area
                object_area = np.sum(mask)
                return object_area / hull_area if hull_area > 0 else 1.0
            except:
                return 1.0
        
        @staticmethod
        def _compute_eccentricity(mask: np.ndarray) -> float:
            """Compute eccentricity (elongation) of region."""
            coords = np.argwhere(mask)
            if len(coords) < 3:
                return 0.0
            
            # Principal component analysis
            centered = coords - coords.mean(axis=0)
            cov = np.cov(centered.T)
            eigenvalues = np.linalg.eigvals(cov)
            eigenvalues = np.sort(eigenvalues)[::-1]
            
            if eigenvalues[0] > 0:
                eccentricity = np.sqrt(1 - (eigenvalues[1] / eigenvalues[0]))
            else:
                eccentricity = 0.0
            
            return eccentricity
    ```

---

### Step 2: Implement Texture Feature Extraction (2–3 hours)

- [ ] **Implement texture features module:**
  - Create: `satinn/features/texture.py`
  - Content:
    ```python
    import numpy as np
    from scipy import ndimage
    from skimage.feature import greycomatrix, greycoprops

    class TextureFeatures:
        """Extract texture features from tissue regions."""
        
        def __init__(self, window_size: int = 50):
            """Initialize texture feature extractor."""
            self.window_size = window_size
        
        def extract(self, image: np.ndarray, mask: np.ndarray) -> np.ndarray:
            """
            Extract texture features from masked tissue regions.
            
            Args:
                image: Preprocessed image (float32, [0, 1])
                mask: Binary segmentation mask
                
            Returns:
                Feature matrix (n_regions × n_features)
            """
            # Label connected components
            labeled, n_regions = ndimage.label(mask)
            
            features = []
            
            for region_id in range(1, n_regions + 1):
                region_mask = (labeled == region_id)
                
                # Get region properties
                y_coords, x_coords = np.where(region_mask)
                if len(y_coords) == 0:
                    continue
                
                # Extract region
                y_min, y_max = y_coords.min(), y_coords.max()
                x_min, x_max = x_coords.min(), x_coords.max()
                region_image = image[y_min:y_max+1, x_min:x_max+1]
                region_submask = region_mask[y_min:y_max+1, x_min:x_max+1]
                
                # Compute features
                mean_intensity = np.mean(image[region_mask])
                std_intensity = np.std(image[region_mask])
                entropy = self._compute_entropy(image[region_mask])
                gradient = self._compute_gradient_energy(region_image, region_submask)
                
                features.append([mean_intensity, std_intensity, entropy, gradient])
            
            return np.array(features, dtype=np.float32)
        
        @staticmethod
        def _compute_entropy(region: np.ndarray) -> float:
            """Compute Shannon entropy of region."""
            # Histogram-based entropy
            hist, _ = np.histogram(region, bins=256, range=(0, 1))
            hist = hist / hist.sum()
            entropy = -np.sum(hist[hist > 0] * np.log2(hist[hist > 0]))
            return entropy
        
        @staticmethod
        def _compute_gradient_energy(image: np.ndarray, mask: np.ndarray) -> float:
            """Compute gradient-based edge energy."""
            # Sobel operators
            sx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
            sy = sx.T
            
            grad_x = ndimage.convolve(image, sx)
            grad_y = ndimage.convolve(image, sy)
            
            gradient_mag = np.sqrt(grad_x**2 + grad_y**2)
            energy = np.sum(gradient_mag[mask])
            
            return energy
    ```

---

### Step 3: Implement Spatial Feature Extraction (1–2 hours)

- [ ] **Implement spatial features module:**
  - Create: `satinn/features/spatial.py`
  - Content:
    ```python
    import numpy as np
    from scipy import ndimage
    from scipy.spatial.distance import cdist

    class SpatialFeatures:
        """Extract spatial relationships and density features."""
        
        def __init__(self, max_distance: float = 200.0):
            """Initialize spatial feature extractor."""
            self.max_distance = max_distance
        
        def extract(self, image: np.ndarray, mask: np.ndarray) -> np.ndarray:
            """
            Extract spatial features between tissue regions.
            
            Args:
                image: Preprocessed image
                mask: Binary segmentation mask
                
            Returns:
                Feature matrix (n_regions × n_features)
            """
            labeled, n_regions = ndimage.label(mask)
            
            features = []
            
            for region_id in range(1, n_regions + 1):
                region_mask = (labeled == region_id)
                
                # Centroid
                cy, cx = ndimage.center_of_mass(region_mask)
                
                # Distance to nearest neighbor
                nearest_distance = self._nearest_neighbor_distance(
                    labeled, region_id, n_regions
                )
                
                # Local density (regions within max_distance)
                local_density = self._local_density(
                    labeled, region_id, n_regions, (cy, cx)
                )
                
                # Tissue fraction in local neighborhood
                tissue_fraction = self._tissue_fraction(
                    mask, (cy, cx), self.max_distance
                )
                
                features.append([nearest_distance, local_density, tissue_fraction])
            
            return np.array(features, dtype=np.float32)
        
        def _nearest_neighbor_distance(self, labeled: np.ndarray, region_id: int, 
                                     n_regions: int) -> float:
            """Compute distance to nearest neighboring region."""
            region_mask = (labeled == region_id)
            y1, x1 = ndimage.center_of_mass(region_mask)
            
            min_dist = float('inf')
            for other_id in range(1, n_regions + 1):
                if other_id == region_id:
                    continue
                other_mask = (labeled == other_id)
                y2, x2 = ndimage.center_of_mass(other_mask)
                dist = np.sqrt((y1 - y2)**2 + (x1 - x2)**2)
                min_dist = min(min_dist, dist)
            
            return min_dist if min_dist != float('inf') else -1
        
        def _local_density(self, labeled: np.ndarray, region_id: int, 
                          n_regions: int, center: tuple) -> int:
            """Count regions within max_distance."""
            cy, cx = center
            region_mask = (labeled == region_id)
            
            count = 0
            for other_id in range(1, n_regions + 1):
                if other_id == region_id:
                    continue
                other_mask = (labeled == other_id)
                y2, x2 = ndimage.center_of_mass(other_mask)
                dist = np.sqrt((cy - y2)**2 + (cx - x2)**2)
                if dist <= self.max_distance:
                    count += 1
            
            return count
        
        def _tissue_fraction(self, mask: np.ndarray, center: tuple, radius: float) -> float:
            """Compute fraction of tissue in circular neighborhood."""
            cy, cx = center
            y, x = np.ogrid[:mask.shape[0], :mask.shape[1]]
            
            circle_mask = ((y - cy)**2 + (x - cx)**2) <= radius**2
            
            tissue_in_circle = np.sum(mask[circle_mask])
            total_in_circle = np.sum(circle_mask)
            
            return tissue_in_circle / total_in_circle if total_in_circle > 0 else 0
    ```

---

### Step 4: Implement Model Interface and Loading (2–3 hours)

- [ ] **Create model interface:**
  - Create: `satinn/models/interface.py`
  - Content:
    ```python
    from abc import ABC, abstractmethod
    import numpy as np

    class Model(ABC):
        """Abstract interface for trained models."""
        
        @abstractmethod
        def load(self, model_path: str):
            """Load model from file."""
            pass
        
        @abstractmethod
        def predict(self, features: np.ndarray) -> np.ndarray:
            """Make predictions on feature matrix."""
            pass
        
        @abstractmethod
        def predict_proba(self, features: np.ndarray) -> np.ndarray:
            """Get prediction probabilities (if applicable)."""
            pass
    ```

- [ ] **Implement scikit-learn model wrapper:**
  - Create: `satinn/models/sklearn_model.py`
  - Content:
    ```python
    import joblib
    import numpy as np
    from satinn.models.interface import Model

    class SKLearnModel(Model):
        """Wrapper for scikit-learn trained models."""
        
        def __init__(self, model_path: str = None):
            """Initialize with optional model path."""
            self.model = None
            if model_path:
                self.load(model_path)
        
        def load(self, model_path: str):
            """Load scikit-learn model from pickle file."""
            try:
                self.model = joblib.load(model_path)
                print(f"Model loaded from {model_path}")
            except Exception as e:
                raise RuntimeError(f"Failed to load model: {e}")
        
        def predict(self, features: np.ndarray) -> np.ndarray:
            """Make predictions."""
            if self.model is None:
                raise RuntimeError("Model not loaded")
            return self.model.predict(features)
        
        def predict_proba(self, features: np.ndarray) -> np.ndarray:
            """Get prediction probabilities."""
            if self.model is None:
                raise RuntimeError("Model not loaded")
            if hasattr(self.model, 'predict_proba'):
                return self.model.predict_proba(features)
            else:
                raise NotImplementedError("Model does not support predict_proba")
    ```

---

### Step 5: Create Complete Feature Extraction Pipeline (2–3 hours)

- [ ] **Implement combined feature extractor:**
  - Create: `satinn/features/__init__.py`
  - Content:
    ```python
    import numpy as np
    from satinn.features.morphological import MorphologicalFeatures
    from satinn.features.texture import TextureFeatures
    from satinn.features.spatial import SpatialFeatures

    class FeatureExtractor:
        """Combine all feature extractors into unified pipeline."""
        
        def __init__(self, include_morphological: bool = True,
                    include_texture: bool = True,
                    include_spatial: bool = True):
            """Initialize with feature selection."""
            self.extractors = []
            self.feature_names = []
            
            if include_morphological:
                self.extractors.append(MorphologicalFeatures())
                self.feature_names.extend(['area', 'perimeter', 'circularity', 'solidity', 'eccentricity'])
            
            if include_texture:
                self.extractors.append(TextureFeatures())
                self.feature_names.extend(['mean_intensity', 'std_intensity', 'entropy', 'gradient'])
            
            if include_spatial:
                self.extractors.append(SpatialFeatures())
                self.feature_names.extend(['nearest_distance', 'local_density', 'tissue_fraction'])
        
        def extract(self, image: np.ndarray, mask: np.ndarray) -> np.ndarray:
            """Extract all configured features."""
            all_features = []
            
            for extractor in self.extractors:
                features = extractor.extract(image, mask)
                all_features.append(features)
            
            # Concatenate features horizontally
            combined = np.hstack(all_features) if all_features else np.array([])
            return combined
        
        def get_feature_names(self) -> list:
            """Get names of all extracted features."""
            return self.feature_names
    ```

---

### Step 6: Create Tests for Feature Extraction (2 hours)

- [ ] **Create tests:**
  - Create: `tests/test_features.py`
  - Content:
    ```python
    import pytest
    import numpy as np
    from satinn.features import FeatureExtractor
    from satinn.testing.mocks import MockImage

    class TestFeatureExtraction:
        def test_morphological_features_shape(self):
            image = MockImage.create_simple_image()
            mask = MockImage.create_segmentation_mask()
            
            extractor = FeatureExtractor(
                include_morphological=True,
                include_texture=False,
                include_spatial=False
            )
            features = extractor.extract(image, mask)
            
            assert features.shape[1] == 5  # 5 morphological features
            assert features.dtype == np.float32
        
        def test_texture_features_shape(self):
            image = MockImage.create_simple_image().astype(np.float32) / 255
            mask = MockImage.create_segmentation_mask()
            
            extractor = FeatureExtractor(
                include_morphological=False,
                include_texture=True,
                include_spatial=False
            )
            features = extractor.extract(image, mask)
            
            assert features.shape[1] == 4  # 4 texture features
        
        def test_combined_features_shape(self):
            image = MockImage.create_simple_image().astype(np.float32) / 255
            mask = MockImage.create_segmentation_mask()
            
            extractor = FeatureExtractor(
                include_morphological=True,
                include_texture=True,
                include_spatial=True
            )
            features = extractor.extract(image, mask)
            
            # 5 morphological + 4 texture + 3 spatial = 12
            assert features.shape[1] == 12
            assert features.shape[0] > 0  # At least one region
        
        def test_feature_names(self):
            extractor = FeatureExtractor()
            names = extractor.get_feature_names()
            
            assert len(names) == 12
            assert 'area' in names
            assert 'circularity' in names
            assert 'entropy' in names
    ```

- [ ] **Run tests:**
  - Run: `pytest tests/test_features.py -v`

---

### Step 7: Document and Create PR (2 hours)

- [ ] **Create feature extraction documentation:**
  - File: `satinn/features/FEATURE_DEFINITIONS.md`
  - Content:
    ```markdown
    # SATINN Feature Definitions

    ## Morphological Features (5 features)
    
    ### 1. Area
    - Definition: Number of pixels in the region
    - Unit: pixels
    - Range: [1, ∞]
    - Biological meaning: Size of tissue region
    
    ### 2. Perimeter
    - Definition: Approximate perimeter of region boundary
    - Unit: pixels
    - Range: [0, ∞]
    - Biological meaning: Boundary complexity
    
    ### 3. Circularity
    - Definition: 4π·Area/Perimeter² (ratio)
    - Unit: dimensionless
    - Range: [0, 1], 1 = perfect circle
    - Biological meaning: Shape regularity
    
    ### 4. Solidity
    - Definition: Area / Convex hull area
    - Unit: dimensionless
    - Range: [0, 1], 1 = fully convex
    - Biological meaning: Concavity/compactness
    
    ### 5. Eccentricity
    - Definition: Elongation measure from PCA
    - Unit: dimensionless
    - Range: [0, 1], 0 = circular, 1 = highly elongated
    - Biological meaning: Shape anisotropy
    
    ## Texture Features (4 features)
    
    ### 6. Mean Intensity
    - Definition: Average pixel intensity in region
    - Unit: [0, 1]
    - Biological meaning: Staining intensity
    
    ### 7. Std Intensity
    - Definition: Standard deviation of pixel intensity
    - Unit: [0, 1]
    - Biological meaning: Intensity heterogeneity
    
    ### 8. Entropy
    - Definition: Shannon entropy of pixel intensity distribution
    - Unit: bits
    - Range: [0, 8]
    - Biological meaning: Pattern complexity
    
    ### 9. Gradient Energy
    - Definition: Sum of edge magnitudes (Sobel gradient)
    - Unit: arbitrary
    - Range: [0, ∞]
    - Biological meaning: Boundary sharpness/edges
    
    ## Spatial Features (3 features)
    
    ### 10. Nearest Neighbor Distance
    - Definition: Distance to closest other region
    - Unit: pixels
    - Range: [0, ∞]
    - Biological meaning: Local isolation/clustering
    
    ### 11. Local Density
    - Definition: Count of neighboring regions within max_distance
    - Unit: count
    - Range: [0, ∞]
    - Biological meaning: Regional clustering
    
    ### 12. Tissue Fraction
    - Definition: Fraction of tissue in circular neighborhood
    - Unit: ratio
    - Range: [0, 1]
    - Biological meaning: Local tissue concentration
    ```

- [ ] **Create another PR:**
  - Branch: `git checkout -b week09-feature-extraction-model`
  - Commit: `git add satinn/features/ satinn/models/ tests/test_features.py && git commit -m "Week 09: Feature extraction and model integration"`
  - Push and create PR with detailed description

---

## Deliverable

```markdown
**Week 09 Feature Extraction & Model Integration**

- Morphological features implemented (5 features): [Yes / No]
- Texture features implemented (4 features): [Yes / No]
- Spatial features implemented (3 features): [Yes / No]
- Combined feature extractor created: [Yes / No]
- Model interface defined: [Yes / No]
- SKLearn model wrapper implemented: [Yes / No]
- Unit tests for features (70%+ coverage): [Yes / No]
- Feature definitions documented: [Yes / No]
- PR created and reviewed: [GitHub PR URL]
- Model successfully loads and predicts: [Yes / No]
```

---

## Objective Completion Criteria

✅ You have completed this week when:

1. Morphological, texture, and spatial features are implemented.
2. Feature extraction produces correct output shapes.
3. Model interface is abstract and extensible.
4. SKLearn model wrapper loads and predicts correctly.
5. Unit tests cover all feature extractors.
6. Feature definitions are documented with biological meanings.
7. PR is created with clear test results.
8. Model integration works end-to-end (features → predictions).

---

## Student Reflection Questions

1. **Feature Engineering:** Why are different types of features (morphological, texture, spatial) important?
2. **Model Integration:** How does the model interface design help you add new model types later?
3. **Validation:** How would you validate that extracted features match the reference implementation?
4. **Next Steps:** What remains to complete the full pipeline?

---

## Mentor Review Checklist

- [ ] Tobe implemented all 12 SATINN features (5 morphological + 4 texture + 3 spatial).
- [ ] Feature extraction produces correct numerical ranges and data types.
- [ ] Model interface is well-designed and extensible.
- [ ] SKLearn wrapper loads and predicts successfully.
- [ ] Unit tests have 70%+ coverage with mock data.
- [ ] Feature definitions include biological meanings.
- [ ] Code follows Python best practices.
- [ ] PR description includes feature list and validation approach.
- [ ] Approve Tobe to proceed to Week 10 (Validation).

---

## Links and Resources

- **Scikit-image Morphology:** https://scikit-image.org/docs/dev/api/skimage.morphology.html
- **GLCM Texture Features:** https://en.wikipedia.org/wiki/Co-occurrence_matrix
- **Feature Engineering:** https://en.wikipedia.org/wiki/Feature_engineering
- **SciPy ndimage:** https://docs.scipy.org/doc/scipy/reference/ndimage.html

---

## Related Epics

- **SATINN Research Track:** Features are core to model performance; weeks 10-11 validate feature quality.
