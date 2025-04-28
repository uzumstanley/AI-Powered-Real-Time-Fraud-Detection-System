## Model Selection  
1. **Logistic Regression**  
   A strong baseline that models the probability of fraud as a Bernoulli outcome; highly interpretable and fast to train—ideal for low-latency inference on BitNet’s architecture.  
2. **Decision Trees**  
   Capture non-linear feature interactions (e.g., large transaction AND unusual location) without feature scaling, though they can overfit without pruning.  
3. **Random Forests**  
   An ensemble of decision trees that reduces overfitting and handles high-dimensional data well, achieving strong accuracy in many fraud benchmarks.  
4. **XGBoost**  
   Gradient-boosted trees that optimize both speed and predictive power; consistently outperforms other algorithms on fraud datasets when properly tuned .

## Training  
1. **Data Preparation**  
   - Exclude identifiers (TransactionID, DeviceID, etc.) and normalize features like `log_transaction_amount` and `deviation_from_user_avg`.  
2. **Handling Class Imbalance**  
   - **SMOTE** synthetic oversampling to augment the minority (fraud) class, preventing the model from ignoring rare events.  
   - **Class Weights**: use `class_weight='balanced'` or compute weights via `compute_class_weight` to penalize misclassification of fraud more heavily.  
3. **Cross-Validation**  
   - **Stratified k-Fold**: preserves the fraud/non-fraud ratio in each fold, ensuring robust performance estimates on imbalanced data.

## Evaluation  
1. **Threshold-Dependent Metrics**  
   - **Precision**: proportion of flagged transactions that are truly fraudulent.  
   - **Recall**: fraction of actual frauds correctly detected.  
   - **F1-Score**: harmonic mean of precision and recall, balancing false positives and false negatives.  
2. **Threshold-Independent Metrics**  
   - **ROC-AUC**: ability of the model to rank fraud higher than non-fraud across all thresholds.  
   - **PR-AUC**: more informative than ROC-AUC under extreme class imbalance, focusing on performance in the rare-event regime.  
3. **Confusion Matrix & Classification Report**  
   - Use scikit-learn’s `classification_report` to get per-class precision, recall, and F1, and analyze error types.  
