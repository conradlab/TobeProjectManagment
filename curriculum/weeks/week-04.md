## WEEK 04: Machine Learning Foundations

**Learning Objective:**
Understand core machine learning concepts including supervised and unsupervised learning, classification and regression tasks, and model evaluation metrics. Apply these concepts to a real dataset using scikit-learn.

**Why This Week Matters:**
Machine learning powers modern biomedical image analysis. Before you implement SATINN, you need to understand how models learn from data, how to evaluate their performance, and what metrics tell us whether a model is working. This week builds the conceptual foundation for weeks 05-12.

**Prerequisites:**
- Python virtual environment and packages from Week 03 (numpy, pandas, scikit-learn, jupyter).
- Access to Prime8 and your work directory.
- Comfortable with Python syntax and basic pandas operations.

**Expected Time Commitment:**
10-12 hours

**Learning Objectives:**
1. Distinguish between supervised and unsupervised learning paradigms.
2. Understand classification and regression as supervised learning tasks.
3. Interpret confusion matrices and understand metrics: precision, recall, F1-score.
4. Train a classifier on the Iris dataset and evaluate its performance.
5. Visualize decision boundaries and feature relationships.
6. Document your model's behavior and limitations.

---

## Plan

### Step 1: Machine Learning Concepts (2–3 hours)

- [ ] **Read about machine learning paradigms:**
  - Read: https://scikit-learn.org/stable/supervised_learning.html (supervised learning overview)
  - Read: https://scikit-learn.org/stable/unsupervised_learning.html (unsupervised learning overview)
  - Key concepts:
    - **Supervised Learning:** Model learns from labeled data (input + expected output).
    - **Classification:** Predicting discrete categories (e.g., "tumor" or "normal").
    - **Regression:** Predicting continuous values (e.g., tumor size in mm).
    - **Unsupervised Learning:** Model learns from unlabeled data (find hidden patterns).
    - **Clustering:** Grouping similar samples without labels.

- [ ] **Understand the supervised learning workflow:**
  1. Collect labeled data (features and labels).
  2. Split data into training and testing sets.
  3. Train a model on the training set.
  4. Evaluate the model on the testing set.
  5. Adjust hyperparameters and iterate.

- [ ] **Learn evaluation metrics for classification:**
  - Read: https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics
  - **Confusion Matrix:** Table showing true positives, true negatives, false positives, false negatives.
    - True Positive (TP): Model predicted "yes", actually "yes".
    - True Negative (TN): Model predicted "no", actually "no".
    - False Positive (FP): Model predicted "yes", actually "no" (Type I error).
    - False Negative (FN): Model predicted "no", actually "yes" (Type II error).
  - **Accuracy:** (TP + TN) / (TP + TN + FP + FN) — overall correctness (can be misleading with imbalanced data).
  - **Precision:** TP / (TP + FP) — of the samples predicted "yes", how many were correct?
  - **Recall (Sensitivity):** TP / (TP + FN) — of the actual "yes" samples, how many did we find?
  - **F1-Score:** Harmonic mean of precision and recall (balances both metrics).

- [ ] **Understand the bias-variance tradeoff:**
  - Read: https://scikit-learn.org/stable/auto_examples/model_selection/plot_bias_variance.html
  - **Bias:** Error from oversimplified models (underfitting).
  - **Variance:** Error from overly complex models (overfitting).
  - Goal: Find the sweet spot between bias and variance.

---

### Step 2: Iris Dataset Classification (2–3 hours)

- [ ] **Load and explore the Iris dataset:**
  - Create a Jupyter notebook: `jupyter notebook` (on Prime8, you may need to use port forwarding or download results)
  - Alternatively, create a Python script in your repository.
  - Write Python code:
    ```python
    import numpy as np
    import pandas as pd
    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    import matplotlib.pyplot as plt

    # Load the Iris dataset
    iris = load_iris()
    X = iris.data  # Features (4 features per flower)
    y = iris.target  # Target (3 species: 0, 1, 2)

    print("Dataset shape:", X.shape)
    print("Number of classes:", len(np.unique(y)))
    print("Feature names:", iris.feature_names)
    print("Target names:", iris.target_names)

    # Create a DataFrame for easier visualization
    df = pd.DataFrame(X, columns=iris.feature_names)
    df['target'] = y
    df['species'] = df['target'].map({0: 'setosa', 1: 'versicolor', 2: 'virginica'})
    print("\nFirst 5 samples:")
    print(df.head())
    ```

- [ ] **Visualize feature distributions:**
  - Add to your script:
    ```python
    # Plot feature distributions by species
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    features = iris.feature_names
    for i, ax in enumerate(axes.flat):
        for species_idx, species_name in enumerate(iris.target_names):
            mask = y == species_idx
            ax.hist(X[mask, i], alpha=0.5, label=species_name, bins=10)
        ax.set_xlabel(features[i])
        ax.set_ylabel('Frequency')
        ax.set_title(f'Distribution of {features[i]}')
        ax.legend()
    plt.tight_layout()
    plt.savefig('iris_feature_distributions.png')
    print("Saved iris_feature_distributions.png")
    ```

---

### Step 3: Train a Classifier (2 hours)

- [ ] **Train a logistic regression classifier:**
  - Add to your script:
    ```python
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training set size: {len(X_train)}")
    print(f"Testing set size: {len(X_test)}")

    # Standardize features (important for many algorithms)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train a logistic regression classifier
    clf = LogisticRegression(max_iter=200, random_state=42)
    clf.fit(X_train_scaled, y_train)

    # Make predictions
    y_pred_train = clf.predict(X_train_scaled)
    y_pred_test = clf.predict(X_test_scaled)

    # Evaluate on training set
    train_accuracy = accuracy_score(y_train, y_pred_train)
    print(f"\nTraining accuracy: {train_accuracy:.3f}")

    # Evaluate on testing set
    test_accuracy = accuracy_score(y_test, y_pred_test)
    print(f"Testing accuracy: {test_accuracy:.3f}")
    ```

- [ ] **Understand the confusion matrix:**
  - Add to your script:
    ```python
    # Confusion matrix for test set
    cm = confusion_matrix(y_test, y_pred_test)
    print("\nConfusion Matrix (test set):")
    print(cm)
    print("Rows: true labels, Columns: predicted labels")

    # Classification report
    print("\nClassification Report (test set):")
    print(classification_report(y_test, y_pred_test, target_names=iris.target_names))
    ```

- [ ] **Visualize the confusion matrix:**
  - Add to your script:
    ```python
    from sklearn.metrics import ConfusionMatrixDisplay

    # Plot confusion matrix
    ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=iris.target_names).plot()
    plt.title('Confusion Matrix: Iris Classification')
    plt.tight_layout()
    plt.savefig('confusion_matrix_iris.png')
    print("Saved confusion_matrix_iris.png")
    ```

---

### Step 4: Model Evaluation and Interpretation (2 hours)

- [ ] **Extract and interpret model parameters:**
  - Add to your script:
    ```python
    # Understand model parameters
    print("\nModel weights (coefficients):")
    for i, species_name in enumerate(iris.target_names):
        print(f"\n{species_name}:")
        for j, feature_name in enumerate(iris.feature_names):
            print(f"  {feature_name}: {clf.coef_[i][j]:.3f}")
    print(f"\nBias (intercept) for each class: {clf.intercept_}")
    ```

- [ ] **Analyze misclassifications:**
  - Add to your script:
    ```python
    # Find misclassified samples
    misclassified_idx = np.where(y_test != y_pred_test)[0]
    print(f"\nTotal misclassified samples: {len(misclassified_idx)}")
    if len(misclassified_idx) > 0:
        for idx in misclassified_idx[:5]:  # Print first 5 misclassified
            true_label = iris.target_names[y_test[idx]]
            pred_label = iris.target_names[y_pred_test[idx]]
            print(f"Sample {idx}: True={true_label}, Predicted={pred_label}")
            print(f"  Features: {X_test[idx]}")
    ```

- [ ] **Compare with other classifiers:**
  - Add to your script:
    ```python
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.svm import SVC

    classifiers = [
        ('Logistic Regression', LogisticRegression(max_iter=200, random_state=42)),
        ('Random Forest', RandomForestClassifier(n_estimators=100, random_state=42)),
        ('SVM', SVC(kernel='rbf', random_state=42)),
    ]

    print("\n\nComparing classifiers:")
    for name, clf in classifiers:
        clf.fit(X_train_scaled, y_train)
        train_acc = clf.score(X_train_scaled, y_train)
        test_acc = clf.score(X_test_scaled, y_test)
        print(f"{name}:")
        print(f"  Training accuracy: {train_acc:.3f}")
        print(f"  Testing accuracy: {test_acc:.3f}")
    ```

---

### Step 5: Unsupervised Learning with Clustering (1–2 hours)

- [ ] **Apply clustering to the Iris dataset (without using labels):**
  - Add to your script:
    ```python
    from sklearn.cluster import KMeans

    # Use only the features, not the labels
    X_for_clustering = X

    # Train K-Means with 3 clusters (we happen to know there are 3 species)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(X_for_clustering)

    # Compare clustering with true labels
    from sklearn.metrics import adjusted_rand_score, homogeneity_score

    ari = adjusted_rand_score(y, cluster_labels)
    homogeneity = homogeneity_score(y, cluster_labels)

    print("\nUnsupervised Clustering (K-Means):")
    print(f"Adjusted Rand Index (similarity to true labels): {ari:.3f}")
    print(f"Homogeneity Score: {homogeneity:.3f}")
    print("Note: These scores tell us how well the unsupervised clusters align with true species.")
    ```

- [ ] **Visualize clusters:**
  - Add to your script:
    ```python
    # Plot first two features, colored by clustering result
    plt.figure(figsize=(10, 5))
    
    plt.subplot(1, 2, 1)
    scatter1 = plt.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis', label='True labels')
    plt.xlabel(iris.feature_names[0])
    plt.ylabel(iris.feature_names[1])
    plt.title('True Species Labels')
    
    plt.subplot(1, 2, 2)
    scatter2 = plt.scatter(X[:, 0], X[:, 1], c=cluster_labels, cmap='viridis', label='K-Means clusters')
    plt.xlabel(iris.feature_names[0])
    plt.ylabel(iris.feature_names[1])
    plt.title('K-Means Clustering Results')
    
    plt.tight_layout()
    plt.savefig('clustering_comparison.png')
    print("Saved clustering_comparison.png")
    ```

---

### Step 6: Document Your Analysis (1–2 hours)

- [ ] **Create a comprehensive report:**
  - Create a file: `ml_foundations_report.md`
  - Content:
    ```markdown
    # Machine Learning Foundations Report

    ## Objective
    Understand core machine learning concepts and apply them to the Iris dataset.

    ## Dataset Overview
    - **Name:** Iris
    - **Samples:** 150 flowers
    - **Features:** 4 (sepal length, sepal width, petal length, petal width)
    - **Classes:** 3 (setosa, versicolor, virginica)
    - **Train/Test Split:** 80/20

    ## Supervised Learning: Classification

    ### Logistic Regression Results
    - Training Accuracy: [INSERT YOUR RESULT]
    - Testing Accuracy: [INSERT YOUR RESULT]
    - Confusion Matrix: See confusion_matrix_iris.png
    - Precision (per class): [INSERT FROM classification_report]
    - Recall (per class): [INSERT FROM classification_report]
    - F1-Score (per class): [INSERT FROM classification_report]

    ### Interpretation
    - Which class was easiest to classify? Why might that be?
    - Which class was hardest? What features cause confusion?
    - Did the model overfit (training >> testing accuracy)?

    ### Comparison with Other Classifiers
    - Logistic Regression: [RESULT]
    - Random Forest: [RESULT]
    - SVM: [RESULT]
    - **Best model:** [NAME] with [ACCURACY] test accuracy

    ## Unsupervised Learning: Clustering

    ### K-Means Results
    - Number of clusters: 3
    - Adjusted Rand Index: [INSERT YOUR RESULT]
    - Homogeneity Score: [INSERT YOUR RESULT]

    ### Interpretation
    - Did the clustering match the true species labels?
    - What does a high/low ARI score indicate?

    ## Key Takeaways
    1. [YOUR INSIGHT]
    2. [YOUR INSIGHT]
    3. [YOUR INSIGHT]

    ## Questions for Future Work
    1. How would we handle imbalanced datasets (unequal class sizes)?
    2. How do we choose hyperparameters (e.g., max_iter for logistic regression)?
    3. How does feature scaling affect model performance?
    ```

- [ ] **Commit your work:**
  - Run: `cd ~/work/satinn-project/satinn-pipeline`
  - Run: `git add ml_foundations_report.md iris_*.png confusion_matrix_iris.png clustering_comparison.png`
  - Run: `git add iris_classification.py` (or your script filename)
  - Run: `git commit -m "Week 04: Machine learning foundations with Iris classification and clustering"`
  - Run: `git push origin main` (or your current branch)

---

## Deliverable

Document your ML learning in a GitHub comment or document:

```markdown
**Week 04 Machine Learning Report**

- Iris dataset loaded and explored: [Yes / No]
- Supervised classification model trained: [Yes / No]
- Model accuracy (training/testing): [TRAIN/TEST]
- Confusion matrix computed and visualized: [Yes / No]
- Top classification metric (precision/recall/F1): [BEST]
- Classifiers compared (≥2 models): [Yes / No]
- Unsupervised clustering applied (K-Means): [Yes / No]
- Cluster quality metrics computed: [ARI, Homogeneity]
- Visualization plots saved: [Yes / No]
- Analysis report written: [Yes / No]
```

---

## Objective Completion Criteria

✅ You have completed this week when:

1. You can load and explore the Iris dataset using scikit-learn.
2. You understand supervised vs. unsupervised learning paradigms.
3. You have trained a classification model and evaluated it with accuracy and confusion matrix.
4. You understand precision, recall, and F1-score and can interpret them.
5. You have compared multiple classifiers and documented their performance.
6. You have applied K-Means clustering to the same dataset.
7. You have created visualizations: feature distributions, confusion matrix, clustering comparison.
8. You have written a comprehensive report explaining your findings.

---

## Student Reflection Questions

Answer in your report or in a GitHub comment:

1. **Classification:** What is the difference between precision and recall? When would you prioritize one over the other?
2. **Overfitting:** Your training accuracy is probably higher than testing accuracy. Why?
3. **Features:** Which features (sepal/petal length/width) were most important for classification?
4. **Clustering:** Why might clustering fail to perfectly match true species, even though the data is well-separated?
5. **Application:** How would these concepts apply to SATINN (distinguishing normal vs. pathological testis tissue)?

---

## Mentor Review Checklist

- [ ] Tobe has loaded and explored the Iris dataset.
- [ ] Tobe has trained a supervised classification model.
- [ ] Tobe's model achieves >90% test accuracy (typical for Iris).
- [ ] Tobe has computed and visualized confusion matrix.
- [ ] Tobe has interpreted precision, recall, and F1-score correctly.
- [ ] Tobe has compared multiple classifiers with documented results.
- [ ] Tobe has applied unsupervised clustering (K-Means).
- [ ] Tobe has created clear, labeled visualizations.
- [ ] Tobe's report demonstrates understanding of ML concepts.
- [ ] Tobe has answered reflection questions thoughtfully.
- [ ] Approve Tobe to proceed to Week 05 (Understanding SATINN).

---

## Optional Stretch Activities

- [ ] Experiment with different train/test split ratios (70/30, 90/10) and document the effect.
- [ ] Use GridSearchCV to find optimal hyperparameters for one classifier.
- [ ] Apply dimensionality reduction (PCA) and visualize the data in 2D.
- [ ] Create a pipeline that combines scaling, feature selection, and classification.
- [ ] Test the trained model on new (made-up) flower measurements and document predictions.

---

## Links and Resources

- **Scikit-learn Classification:** https://scikit-learn.org/stable/supervised_learning.html
- **Confusion Matrix Explanation:** https://en.wikipedia.org/wiki/Confusion_matrix
- **Classification Metrics:** https://scikit-learn.org/stable/modules/model_evaluation.html
- **Iris Dataset:** https://en.wikipedia.org/wiki/Iris_flower_data_set
- **Bias-Variance Tradeoff:** https://scikit-learn.org/stable/auto_examples/model_selection/plot_bias_variance.html

---

## Related Epics

- **SATINN Research Track:** Understanding these concepts is essential for weeks 05-12 (tissue classification).
- **Independent Research Epic:** ML foundations apply to any machine learning project.
