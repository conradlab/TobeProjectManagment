## WEEK 11: Alternative Machine Learning Approaches

**Learning Objective:**
Explore and implement alternative machine learning approaches to SATINN (supervised and unsupervised), compare their performance against the reference SATINN implementation, and propose a controlled experimental evaluation.

**Why This Week Matters:**
SATINN is one approach to a problem; other algorithms might work better. This week develops your scientific thinking: you'll test hypotheses about whether different ML methods could improve on SATINN's performance. You'll design rigorous experiments to compare approaches fairly.

**Prerequisites:**
- Complete SATINN Python implementation and validation from Weeks 08-10.
- Machine learning foundations from Week 04.
- Understanding of evaluation metrics and experimental design.

**Expected Time Commitment:**
12-14 hours

**Learning Objectives:**
1. Implement at least one supervised learning alternative (e.g., Random Forest, SVM).
2. Implement at least one unsupervised learning alternative (e.g., clustering, self-supervised learning).
3. Compare alternatives against SATINN using consistent metrics.
4. Analyze computational cost (time, memory) for each approach.
5. Identify annotation requirements for each method.
6. Design a controlled experiment for fair comparison.
7. Document findings and propose next steps.

---

## Plan

### Step 1: Implement Supervised Alternative (3–4 hours)

- [ ] **Choose a supervised alternative:**
  - Options: Random Forest Classifier, Support Vector Machine (SVM), Gradient Boosting
  - Recommended: Random Forest (robust, handles mixed feature types)

- [ ] **Implement Random Forest wrapper:**
  - Create: `satinn/alternative_models/random_forest_approach.py`
  - Content:
    ```python
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import StandardScaler
    import joblib

    class RandomForestSATINN:
        """Alternative SATINN implementation using Random Forest."""
        
        def __init__(self, n_estimators: int = 200, max_depth: int = 20):
            """Initialize Random Forest classifier."""
            self.classifier = RandomForestClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                random_state=42,
                n_jobs=-1
            )
            self.scaler = StandardScaler()
            self.is_trained = False
        
        def train(self, features: np.ndarray, labels: np.ndarray):
            """Train on features and labels."""
            # Scale features
            features_scaled = self.scaler.fit_transform(features)
            
            # Train classifier
            self.classifier.fit(features_scaled, labels)
            self.is_trained = True
            
            # Get feature importances
            self.feature_importances = self.classifier.feature_importances_
        
        def predict(self, features: np.ndarray) -> np.ndarray:
            """Make predictions."""
            if not self.is_trained:
                raise RuntimeError("Model not trained yet")
            
            features_scaled = self.scaler.transform(features)
            return self.classifier.predict(features_scaled)
        
        def predict_proba(self, features: np.ndarray) -> np.ndarray:
            """Get prediction probabilities."""
            if not self.is_trained:
                raise RuntimeError("Model not trained yet")
            
            features_scaled = self.scaler.transform(features)
            return self.classifier.predict_proba(features_scaled)
        
        def get_feature_importance(self) -> np.ndarray:
            """Return feature importance scores."""
            return self.feature_importances
        
        def save(self, filepath: str):
            """Save trained model."""
            joblib.dump({
                'classifier': self.classifier,
                'scaler': self.scaler,
            }, filepath)
        
        def load(self, filepath: str):
            """Load trained model."""
            data = joblib.load(filepath)
            self.classifier = data['classifier']
            self.scaler = data['scaler']
            self.is_trained = True
    ```

- [ ] **Implement SVM alternative:**
  - Create: `satinn/alternative_models/svm_approach.py`
  - Content:
    ```python
    import numpy as np
    from sklearn.svm import SVC
    from sklearn.preprocessing import StandardScaler
    import joblib

    class SVMSATINN:
        """Alternative SATINN implementation using Support Vector Machine."""
        
        def __init__(self, kernel: str = 'rbf', C: float = 1.0):
            """Initialize SVM classifier."""
            self.classifier = SVC(kernel=kernel, C=C, probability=True, random_state=42)
            self.scaler = StandardScaler()
            self.is_trained = False
        
        def train(self, features: np.ndarray, labels: np.ndarray):
            """Train on features and labels."""
            features_scaled = self.scaler.fit_transform(features)
            self.classifier.fit(features_scaled, labels)
            self.is_trained = True
        
        def predict(self, features: np.ndarray) -> np.ndarray:
            """Make predictions."""
            if not self.is_trained:
                raise RuntimeError("Model not trained yet")
            
            features_scaled = self.scaler.transform(features)
            return self.classifier.predict(features_scaled)
        
        def predict_proba(self, features: np.ndarray) -> np.ndarray:
            """Get prediction probabilities."""
            if not self.is_trained:
                raise RuntimeError("Model not trained yet")
            
            features_scaled = self.scaler.transform(features)
            return self.classifier.predict_proba(features_scaled)
        
        def save(self, filepath: str):
            joblib.dump({'classifier': self.classifier, 'scaler': self.scaler}, filepath)
        
        def load(self, filepath: str):
            data = joblib.load(filepath)
            self.classifier = data['classifier']
            self.scaler = data['scaler']
            self.is_trained = True
    ```

---

### Step 2: Implement Unsupervised Alternative (2–3 hours)

- [ ] **Implement clustering-based approach:**
  - Create: `satinn/alternative_models/clustering_approach.py`
  - Content:
    ```python
    import numpy as np
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler

    class ClusteringSATINN:
        """Unsupervised clustering-based tissue analysis."""
        
        def __init__(self, n_clusters: int = 3):
            """Initialize clustering model."""
            self.n_clusters = n_clusters
            self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            self.scaler = StandardScaler()
            self.is_trained = False
        
        def train(self, features: np.ndarray):
            """Learn clusters (unsupervised - no labels needed)."""
            features_scaled = self.scaler.fit_transform(features)
            self.kmeans.fit(features_scaled)
            self.is_trained = True
        
        def predict(self, features: np.ndarray) -> np.ndarray:
            """Assign clusters to new samples."""
            if not self.is_trained:
                raise RuntimeError("Model not trained yet")
            
            features_scaled = self.scaler.transform(features)
            return self.kmeans.predict(features_scaled)
        
        def get_centroids(self) -> np.ndarray:
            """Return cluster centroids (in feature space)."""
            return self.kmeans.cluster_centers_
        
        def analyze_clusters(self, features: np.ndarray) -> dict:
            """Analyze cluster statistics."""
            if not self.is_trained:
                raise RuntimeError("Model not trained yet")
            
            clusters = self.predict(features)
            
            stats = {}
            for cluster_id in range(self.n_clusters):
                cluster_mask = clusters == cluster_id
                cluster_features = features[cluster_mask]
                
                stats[cluster_id] = {
                    'size': np.sum(cluster_mask),
                    'mean': np.mean(cluster_features, axis=0),
                    'std': np.std(cluster_features, axis=0),
                }
            
            return stats
    ```

- [ ] **Implement self-supervised learning alternative:**
  - Create: `satinn/alternative_models/self_supervised_approach.py`
  - Pseudocode:
    ```python
    class SelfSupervisedSATINN:
        """
        Self-supervised learning approach: learn representations without labels.
        
        Strategy: Use augmented feature perturbations to learn invariant representations,
        then cluster or classify based on learned representations.
        """
        
        def __init__(self):
            # Implementation: Feature noise perturbation + autoencoder
            # Could use contrastive learning or other self-supervised techniques
            pass
    ```

---

### Step 3: Create Comparison Framework (2–3 hours)

- [ ] **Implement comparison metrics:**
  - Create: `satinn/comparison/experiments.py`
  - Content:
    ```python
    import numpy as np
    import time
    from typing import Dict, List
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

    class ExperimentComparison:
        """Compare different ML approaches on SATINN problem."""
        
        def __init__(self, approaches: Dict):
            """
            Initialize with dictionary of approaches.
            
            Args:
                approaches: {'satinn': model1, 'random_forest': model2, ...}
            """
            self.approaches = approaches
            self.results = {}
        
        def evaluate_supervised(self, test_features: np.ndarray, 
                               test_labels: np.ndarray) -> Dict:
            """
            Evaluate all supervised approaches.
            
            Returns:
                Dictionary with metrics for each approach
            """
            results = {}
            
            for name, model in self.approaches.items():
                # Make predictions
                start_time = time.time()
                predictions = model.predict(test_features)
                inference_time = time.time() - start_time
                
                # Compute metrics
                accuracy = accuracy_score(test_labels, predictions)
                precision = precision_score(test_labels, predictions, average='weighted')
                recall = recall_score(test_labels, predictions, average='weighted')
                f1 = f1_score(test_labels, predictions, average='weighted')
                
                cm = confusion_matrix(test_labels, predictions)
                
                results[name] = {
                    'accuracy': accuracy,
                    'precision': precision,
                    'recall': recall,
                    'f1_score': f1,
                    'confusion_matrix': cm,
                    'inference_time_ms': inference_time * 1000,
                }
            
            self.results = results
            return results
        
        def evaluate_unsupervised(self, test_features: np.ndarray,
                                 true_labels: np.ndarray = None) -> Dict:
            """
            Evaluate unsupervised approaches.
            
            Returns:
                Dictionary with clustering metrics
            """
            from sklearn.metrics import silhouette_score, davies_bouldin_score
            
            results = {}
            
            for name, model in self.approaches.items():
                if not hasattr(model, 'predict'):
                    continue
                
                # Get cluster assignments
                clusters = model.predict(test_features)
                
                # Compute metrics
                silhouette = silhouette_score(test_features, clusters)
                davies_bouldin = davies_bouldin_score(test_features, clusters)
                
                # If ground truth available, compute alignment
                if true_labels is not None:
                    from sklearn.metrics import adjusted_rand_score
                    ari = adjusted_rand_score(true_labels, clusters)
                else:
                    ari = None
                
                results[name] = {
                    'silhouette_score': silhouette,
                    'davies_bouldin_index': davies_bouldin,
                    'adjusted_rand_index': ari,
                    'n_clusters': len(np.unique(clusters)),
                }
            
            return results
        
        def estimate_computational_cost(self, test_features: np.ndarray) -> Dict:
            """
            Estimate computational cost (memory, time) for each approach.
            """
            import tracemalloc
            
            costs = {}
            
            for name, model in self.approaches.items():
                # Memory usage
                tracemalloc.start()
                predictions = model.predict(test_features[:100])  # Sample
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                
                costs[name] = {
                    'memory_mb': peak / 1024 / 1024,
                    'prediction_time_per_sample_ms': (peak / len(test_features[:100])),
                }
            
            return costs
    ```

---

### Step 4: Run Comparative Experiments (2–3 hours)

- [ ] **Create experiment script:**
  - File: `experiments/compare_approaches.py`
  - Pseudocode:
    ```python
    import numpy as np
    from satinn.pipeline import SATINNPipeline
    from satinn.alternative_models.random_forest_approach import RandomForestSATINN
    from satinn.alternative_models.svm_approach import SVMSATINN
    from satinn.alternative_models.clustering_approach import ClusteringSATINN
    from satinn.comparison.experiments import ExperimentComparison

    # Load training and test data
    train_features = np.load('data/train_features.npy')
    train_labels = np.load('data/train_labels.npy')
    test_features = np.load('data/test_features.npy')
    test_labels = np.load('data/test_labels.npy')

    # Initialize models
    satinn_model = ...  # Load pre-trained SATINN model
    rf_model = RandomForestSATINN()
    svm_model = SVMSATINN()
    clustering_model = ClusteringSATINN()

    # Train alternative models
    rf_model.train(train_features, train_labels)
    svm_model.train(train_features, train_labels)
    clustering_model.train(train_features)  # Unsupervised

    # Compare
    approaches = {
        'SATINN (Reference)': satinn_model,
        'Random Forest': rf_model,
        'SVM': svm_model,
        'K-Means Clustering': clustering_model,
    }

    comparison = ExperimentComparison(approaches)
    supervised_results = comparison.evaluate_supervised(test_features, test_labels)
    unsupervised_results = comparison.evaluate_unsupervised(test_features, test_labels)
    computational_costs = comparison.estimate_computational_cost(test_features)

    # Print results
    print("=== SUPERVISED LEARNING COMPARISON ===")
    for name, metrics in supervised_results.items():
        print(f"\n{name}:")
        print(f"  Accuracy: {metrics['accuracy']:.3f}")
        print(f"  Precision: {metrics['precision']:.3f}")
        print(f"  Recall: {metrics['recall']:.3f}")
        print(f"  F1-Score: {metrics['f1_score']:.3f}")

    print("\n=== UNSUPERVISED LEARNING METRICS ===")
    for name, metrics in unsupervised_results.items():
        print(f"\n{name}:")
        print(f"  Silhouette Score: {metrics['silhouette_score']:.3f}")
        print(f"  Davies-Bouldin Index: {metrics['davies_bouldin_index']:.3f}")
    ```

---

### Step 5: Design Controlled Experiment for Fair Comparison (2–3 hours)

- [ ] **Document experimental design:**
  - File: `EXPERIMENTAL_DESIGN.md`
  - Content:
    ```markdown
    # Comparative ML Experiment Design

    ## Research Question
    Can alternative ML approaches (Random Forest, SVM, clustering) perform better than 
    SATINN on testis histology classification?

    ## Hypotheses
    - H1: Random Forest achieves better accuracy than SATINN (due to better feature selection)
    - H2: Unsupervised clustering can identify meaningful tissue subtypes without labels
    - H3: Ensemble methods outperform single-model SATINN

    ## Experimental Setup

    ### Data Partitioning
    - Training set: 60% (500 regions), stratified by class
    - Validation set: 20% (170 regions), for hyperparameter tuning
    - Test set: 20% (170 regions), held-out for final evaluation
    - No data leakage between sets

    ### Baseline
    - SATINN: Reference implementation trained on original data
    - Metrics: Accuracy, Precision, Recall, F1-Score

    ### Treatments (Alternative Approaches)
    1. Random Forest Classifier
       - Hyperparameters: n_estimators=200, max_depth=20, tuned on validation set
    
    2. Support Vector Machine (SVM)
       - Kernel: RBF (most flexible for non-linear boundaries)
       - C parameter: Tuned via GridSearchCV
    
    3. K-Means Clustering (Unsupervised)
       - n_clusters: 3 (matching SATINN's number of tissue classes)
       - Metrics: Silhouette score, alignment with ground truth

    ### Hyperparameter Tuning
    - Method: Grid Search or Random Search on validation set
    - Optimization metric: F1-Score (balanced for precision/recall)
    - Constraint: No tuning on test set

    ### Evaluation Protocol
    - Primary metric: F1-Score (handles class imbalance)
    - Secondary metrics: Accuracy, Precision, Recall
    - Statistical significance: Compute 95% CI using bootstrap
    - Computational cost: Memory and time per prediction

    ### Reproducibility
    - Random seed: 42 (set for all models)
    - Data splits: Save indices to enable reproduction
    - Model checkpoints: Save trained models for re-evaluation

    ## Expected Outcomes
    1. Quantitative comparison of all approaches
    2. Identify which features are most predictive (feature importance from RF)
    3. Determine if unsupervised clustering reveals tissue subtypes
    4. Computational cost-benefit analysis
    5. Recommendation for best approach or ensemble strategy

    ## Limitations
    - Training data limited to reference dataset (may not generalize)
    - Unsupervised approaches evaluated only on existing ground truth
    - Feature engineering fixed (not optimized per model type)
    ```

---

### Step 6: Document Findings and Create Report (2 hours)

- [ ] **Create comprehensive comparison report:**
  - File: `ALTERNATIVE_APPROACHES_REPORT.md`
  - Content:
    ```markdown
    # Alternative ML Approaches for SATINN: Comparative Study

    ## Executive Summary
    This report evaluates Random Forest, SVM, and K-Means clustering against the 
    reference SATINN implementation on testis histology classification.

    ## Results

    ### Supervised Learning Approaches
    
    | Approach | Accuracy | Precision | Recall | F1-Score | Time/Sample (ms) |
    |----------|----------|-----------|--------|----------|-----------------|
    | SATINN Reference | 0.923 | 0.918 | 0.925 | 0.921 | 2.3 |
    | Random Forest | 0.935 | 0.930 | 0.937 | 0.934 | 1.8 |
    | SVM (RBF) | 0.918 | 0.915 | 0.920 | 0.917 | 3.5 |

    ### Key Findings
    
    **Winner: Random Forest**
    - Accuracy improved by 1.2% over SATINN
    - Faster inference (1.8 ms vs 2.3 ms per sample)
    - Feature importance analysis reveals key discriminators
    
    **SVM Performance:**
    - Slightly lower accuracy (-0.5%) but comparable
    - Slower inference due to kernel computation
    - Robust to feature scaling (StandardScaler applied)
    
    **Unsupervised Clustering:**
    - Silhouette Score: 0.67 (moderate cluster quality)
    - Adjusted Rand Index: 0.74 (good agreement with ground truth)
    - Valuable for discovering tissue subtypes without labels

    ### Feature Importance (Random Forest)
    Top 5 discriminative features:
    1. Circularity (0.18)
    2. Mean Intensity (0.15)
    3. Solidity (0.13)
    4. Entropy (0.11)
    5. Area (0.09)

    ## Recommendations

    1. **Production Use:** Random Forest provides best accuracy/speed tradeoff
    2. **Alternative:** Consider ensemble (SATINN + RF + SVM) for robustness
    3. **Future Work:** Test on new datasets to verify generalization
    4. **Unsupervised:** K-Means clustering useful for exploratory analysis

    ## Conclusion
    While SATINN provides a solid baseline, Random Forest achieves statistically 
    significant improvements in accuracy and speed on the reference dataset.
    Further validation on independent datasets recommended before adoption.
    ```

---

### Step 7: Create PR with Experimental Results (1 hour)

- [ ] **Prepare PR:**
  - Branch: `git checkout -b week11-alternative-approaches`
  - Add: Alternative model implementations, comparison framework, experiment scripts, reports
  - Commit: `git add satinn/alternative_models/ satinn/comparison/ experiments/ ALTERNATIVE_* EXPERIMENTAL_DESIGN.md`
  - Commit message: "Week 11: Alternative ML approaches, comparative experiments, and findings"
  - Push and create PR

---

## Deliverable

```markdown
**Week 11 Alternative Approaches Report**

- Supervised alternative #1 (Random Forest) implemented: [Yes / No]
- Supervised alternative #2 (SVM) implemented: [Yes / No]
- Unsupervised alternative (Clustering) implemented: [Yes / No]
- Self-supervised approach explored: [Yes / No]
- Comparison framework created: [Yes / No]
- Experiments run on test data: [Yes / No]
- Computational cost analysis completed: [Yes / No]
- Experimental design documented: [Yes / No]
- Comparative report written with results: [Yes / No]
- Statistical analysis (confidence intervals) included: [Yes / No]
```

---

## Objective Completion Criteria

✅ You have completed this week when:

1. At least 2 supervised alternatives are implemented and trained.
2. At least 1 unsupervised alternative is implemented.
3. All approaches are evaluated on consistent test data.
4. Computational costs (time, memory) are documented.
5. Experimental design prevents data leakage and ensures fair comparison.
6. Results show clear performance differences with statistical justification.
7. Feature importance and findings are documented.
8. Recommendations for next steps are provided.

---

## Student Reflection Questions

1. **Model Comparison:** Which alternative performed best and why?
2. **Trade-offs:** Is accuracy worth the computational cost difference?
3. **Generalization:** Do you expect these results to hold on new data?
4. **Ensemble:** Would combining multiple approaches improve results?
5. **Next Steps:** What would you do to further improve performance?

---

## Mentor Review Checklist

- [ ] Alternative models are properly trained on training data only.
- [ ] Evaluation is performed on held-out test set.
- [ ] Metrics are computed correctly (accuracy, precision, recall, F1).
- [ ] Computational costs are realistic and measured.
- [ ] Experimental design prevents data leakage.
- [ ] Results show clear performance differences.
- [ ] Report includes statistical significance testing.
- [ ] Recommendations are based on results, not prior assumptions.
- [ ] Code is reproducible with saved random seeds.
- [ ] Approve Tobe to proceed to Week 12 (Final Presentation).

---

## Optional Stretch Activities

- [ ] Implement ensemble methods (voting, stacking) combining multiple models.
- [ ] Perform cross-validation (k-fold) for more robust performance estimates.
- [ ] Hyperparameter optimization using Bayesian optimization.
- [ ] Explain individual predictions using SHAP values.
- [ ] Test approaches on second dataset to assess generalization.

---

## Links and Resources

- **Scikit-learn Model Comparison:** https://scikit-learn.org/stable/modules/model_evaluation.html
- **Hyperparameter Tuning:** https://scikit-learn.org/stable/modules/grid_search.html
- **Feature Importance:** https://scikit-learn.org/stable/auto_examples/inspection/plot_permutation_importance.html
- **Statistical Testing:** https://en.wikipedia.org/wiki/Statistical_hypothesis_testing

---

## Related Epics

- **SATINN Research Track:** Week 11 explores extensions and improvements to baseline.
