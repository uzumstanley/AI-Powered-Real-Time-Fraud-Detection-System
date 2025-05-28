import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, roc_auc_score, roc_curve
import joblib
import os
import matplotlib.pyplot as plt

# Paths
DATA_PATH = '/Users/mac/Desktop/FRAUD DETECTION/bank_transactions_featured.csv'
OUTPUT_DIR = '/Users/mac/Desktop/FRAUD DETECTION/app/model/artifacts'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load Dataset
df = pd.read_csv(DATA_PATH, parse_dates=['TransactionDate', 'PreviousTransactionDate'])

# Feature Selection
drop_cols = ['TransactionID', 'AccountID', 'TransactionDate', 'PreviousTransactionDate', 'DeviceID', 'IP Address', 'MerchantID']
X = df.drop(columns=drop_cols)

# Scale numerical features
numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
scaler = StandardScaler()
X_numeric = pd.DataFrame(scaler.fit_transform(X[numeric_cols]), columns=numeric_cols)

# One-hot encode categorical features
cat_cols = ['TransactionType', 'Location', 'Channel', 'CustomerOccupation', 'user_primary_location']
encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
X_cat = pd.DataFrame(encoder.fit_transform(X[cat_cols]), columns=encoder.get_feature_names_out(cat_cols))

# Combine features
X_combined = pd.concat([X_numeric, X_cat], axis=1)

# Train Isolation Forest
iso = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
iso.fit(X_combined)
scores = -iso.decision_function(X_combined)
threshold = np.percentile(scores, 95)
df['is_fraud'] = (scores >= threshold).astype(int)

# Save Isolation Forest and Encoder
joblib.dump(iso, os.path.join(OUTPUT_DIR, 'isolation_forest.pkl'))
joblib.dump(encoder, os.path.join(OUTPUT_DIR, 'onehot_encoder.pkl'))

# Prepare for supervised training
y = df['is_fraud']
X_train, X_test, y_train, y_test = train_test_split(X_combined, y, test_size=0.3, stratify=y, random_state=42)

# Train XGBoost
neg, pos = (y_train == 0).sum(), (y_train == 1).sum()
scale_pos_weight = neg / pos
xgb = XGBClassifier(scale_pos_weight=scale_pos_weight, random_state=42)
xgb.fit(X_train, y_train)

# Save XGBoost model
joblib.dump(xgb, os.path.join(OUTPUT_DIR, 'xgb_model.pkl'))

# Evaluate
y_pred = xgb.predict(X_test)
y_prob = xgb.predict_proba(X_test)[:, 1]
report = classification_report(y_test, y_pred)
auc = roc_auc_score(y_test, y_prob)

# Save report and ROC curve
with open(os.path.join(OUTPUT_DIR, 'classification_report.txt'), 'w') as f:
    f.write(report + f"\nROC-AUC: {auc:.4f}\n")

fpr, tpr, _ = roc_curve(y_test, y_prob)
plt.plot(fpr, tpr, label=f'XGBoost (AUC = {auc:.4f})')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend()
plt.savefig(os.path.join(OUTPUT_DIR, 'roc_curve.png'))