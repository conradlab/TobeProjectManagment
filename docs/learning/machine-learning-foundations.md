# Machine Learning Foundations

**Target Week:** Week 4  
**Learning Objective:** Understand core ML concepts and practical model evaluation  
**Time Estimate:** 3-4 hours reading + practice  

## Core ML Paradigms

### Supervised vs. Unsupervised Learning

**Supervised Learning** uses labeled training data to predict outputs.
- **Classification:** predict discrete categories (e.g., "cell type A" vs. "cell type B")
- **Regression:** predict continuous values (e.g., cell count, feature intensity)

In SATINN's Python implementation, you'll use classification to assign cell types from segmented regions and regression to estimate morphological features.

**Unsupervised Learning** finds patterns without labels.
- **Clustering:** group similar data points (e.g., k-means for cell grouping)
- **Dimensionality reduction:** simplify high-dimensional features (e.g., PCA)

## Classification vs. Regression

| Aspect | Classification | Regression |
|--------|---|---|
| **Output** | Discrete class labels | Continuous numerical values |
| **Use case** | "Is this a Sertoli cell?" | "What is this cell's diameter?" |
| **Evaluation** | Accuracy, precision, recall, F1 | MSE, RMSE, R² score |
| **SATINN example** | Classify segmented regions as nucleus vs. cytoplasm | Predict sperm count from image features |

## Train/Test Split Workflow

**Why split data?** A model trained and tested on the same data will overfit—it memorizes patterns that don't generalize to new data.

**Typical split:** 80% training, 20% testing (or 70/30 for smaller datasets).

```python
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

# Load example dataset
X, y = load_iris(return_X_y=True)

# Split into 80% train, 20% test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Training samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")

# Train model on training data only
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

# Evaluate on test data (unseen during training)
train_accuracy = clf.score(X_train, y_train)
test_accuracy = clf.score(X_test, y_test)

print(f"Train accuracy: {train_accuracy:.3f}")
print(f"Test accuracy: {test_accuracy:.3f}")
```

**Important:** Always use `random_state` for reproducibility (SATINN requirement—see Week 6).

## Cross-Validation

**Train/test split** uses one fold; **cross-validation** uses multiple folds to get more reliable estimates.

**K-fold cross-validation:** Split data into k equal parts, train k models (each time holding one fold for testing), average the results.

```python
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier

# 5-fold cross-validation
scores = cross_val_score(
    RandomForestClassifier(random_state=42),
    X, y, cv=5, scoring='accuracy'
)

print(f"Cross-validation scores: {scores}")
print(f"Mean: {scores.mean():.3f}, Std: {scores.std():.3f}")
# Output: Mean: 0.967, Std: 0.033
```

Use cross-validation when:
- Dataset is small (< 1000 samples)
- You need confidence intervals on model performance
- You're tuning hyperparameters

## Evaluation Metrics

### Confusion Matrix

For binary classification, visualize true positives (TP), false positives (FP), true negatives (TN), false negatives (FN):

```
           Predicted
           Positive  Negative
Actual  P    TP        FN
        N    FP        TN
```

```python
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# Example: classify cells as Sertoli (1) or not (0)
y_true = [1, 1, 0, 1, 0, 0, 1, 0]
y_pred = [1, 1, 0, 0, 0, 0, 1, 1]

cm = confusion_matrix(y_true, y_pred)
print(cm)
# [[4 1]
#  [1 2]]

# Visualize
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Not Sertoli', 'Sertoli'])
disp.plot()
plt.show()
```

### Precision

**What fraction of predicted positives are actually positive?**

Precision = TP / (TP + FP)

- Use when false positives are costly (e.g., mistakenly classifying a cell type leads to wasted experimental effort)
- High precision = low false positive rate

### Recall (Sensitivity)

**What fraction of actual positives did we find?**

Recall = TP / (TP + FN)

- Use when false negatives are costly (e.g., missing cells of interest)
- High recall = low false negative rate

### F1 Score

**Harmonic mean of precision and recall.**

F1 = 2 × (Precision × Recall) / (Precision + Recall)

- Single-number summary when precision and recall matter equally
- Ranges 0-1; higher is better

```python
from sklearn.metrics import classification_report

y_true = [1, 1, 0, 1, 0, 0, 1, 0]
y_pred = [1, 1, 0, 0, 0, 0, 1, 1]

print(classification_report(y_true, y_pred, target_names=['Not Sertoli', 'Sertoli']))

#               precision    recall  f1-score   support
#
#   Not Sertoli       0.80      0.80      0.80         5
#       Sertoli       0.67      0.67      0.67         3
#
#     accuracy                           0.75         8
#    macro avg       0.73      0.73      0.73         8
# weighted avg       0.75      0.75      0.75         8
```

## Practical Scikit-learn Example

**Task:** Build a cell classification pipeline (nucleus vs. cytoplasm) from image features.

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

# Example synthetic data: 100 regions, 5 morphological features
np.random.seed(42)
X = np.random.randn(100, 5)  # Features: area, eccentricity, intensity, etc.
y = np.random.randint(0, 2, 100)  # Labels: 0=cytoplasm, 1=nucleus

# Create pipeline (standardize → classify)
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(n_estimators=50, random_state=42))
])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Cross-validation on training set
cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='f1_weighted')
print(f"CV F1 scores: {cv_scores}")
print(f"Mean F1: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")

# Train on full training set
pipeline.fit(X_train, y_train)

# Evaluate on test set
y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred, target_names=['cytoplasm', 'nucleus']))

# Feature importance from Random Forest
feature_names = ['area', 'eccentricity', 'intensity', 'solidity', 'aspect_ratio']
importances = pipeline.named_steps['classifier'].feature_importances_
for name, imp in zip(feature_names, importances):
    print(f"{name}: {imp:.3f}")
```

## Common Pitfalls and Solutions

### 1. Data Leakage
**Problem:** Preprocessing (normalization, feature selection) is done before splitting.
```python
# WRONG: Leakage! Statistics calculated on all data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # Fit on all data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2)

# RIGHT: Fit scaler only on training data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)  # Transform only, don't fit
```

### 2. Imbalanced Classes
**Problem:** Dataset has many negatives, few positives (e.g., rare cell types). Accuracy is misleading.
```python
# Check class distribution
from collections import Counter
print(Counter(y))  # {0: 950, 1: 50}  <- highly imbalanced

# Solution 1: Use stratified split
train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Solution 2: Use class weights
RandomForestClassifier(class_weight='balanced', random_state=42)

# Solution 3: Use appropriate metrics (F1, precision-recall) not just accuracy
```

### 3. Overfitting
**Problem:** Model fits training data perfectly but fails on test data.
```python
# Red flag: huge gap between train and test accuracy
print(f"Train accuracy: 0.99")
print(f"Test accuracy: 0.65")  # Major overfitting!

# Solutions:
# - Simplify model (fewer trees, higher min_samples_split)
# - Get more training data
# - Use cross-validation to detect early
# - Add regularization (L1/L2 penalty)
```

### 4. Forgetting to Commit Random Seed
**Problem:** Results are not reproducible (SATINN requirement).
```python
# WRONG: Different results every run
model = RandomForestClassifier()

# RIGHT: Always include random_state
model = RandomForestClassifier(random_state=42)
```

## Next Steps

- **Assignment (Week 4):** Implement a simple classifier on a provided dataset, compute all metrics, explain precision vs. recall in your domain.
- **Prepare for Week 6:** Ensure your code is reproducible with fixed random seeds.
- **For SATINN:** This foundation will support the segmentation and cell classification modules (Weeks 7-9).

## References

- Scikit-learn docs: https://scikit-learn.org/stable/
- Confusion Matrix Guide: https://en.wikipedia.org/wiki/Confusion_matrix
- F1 Score Intuition: https://towardsdatascience.com/the-f1-score-explained-348db94e869c
