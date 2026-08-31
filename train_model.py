import pandas as pd
import joblib

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv(
    "dataset/transaction_risk_dataset_professional_1000.csv"
)

# ==========================================
# REMOVE UNNECESSARY COLUMNS
# ==========================================

df.drop(
    ["Transaction_ID", "Customer_ID"],
    axis=1,
    inplace=True
)

# ==========================================
# CONVERT DATE
# ==========================================

df["Transaction_Date"] = pd.to_datetime(
    df["Transaction_Date"],
    format="%d-%m-%Y"
)

df["Transaction_Day"] = df["Transaction_Date"].dt.day

df["Transaction_Month"] = df["Transaction_Date"].dt.month

# ==========================================
# CONVERT TIME
# ==========================================

df["Transaction_Time"] = pd.to_datetime(
    df["Transaction_Time"],
    format="%H:%M"
)

df["Transaction_Hour"] = df["Transaction_Time"].dt.hour

# ==========================================
# DROP OLD DATE/TIME COLUMNS
# ==========================================

df.drop(
    [
        "Transaction_Date",
        "Transaction_Time"
    ],
    axis=1,
    inplace=True
)

# ==========================================
# REMOVE TRANSACTION STATUS
# ==========================================

df.drop(
    ["Transaction_Status"],
    axis=1,
    inplace=True
)

# ==========================================
# LABEL ENCODING
# ==========================================

label_encoders = {}

categorical_columns = df.select_dtypes(
    include="object"
).columns

for column in categorical_columns:

    encoder = LabelEncoder()

    df[column] = encoder.fit_transform(
        df[column]
    )

    label_encoders[column] = encoder

# ==========================================
# SAVE LABEL ENCODERS
# ==========================================

joblib.dump(
    label_encoders,
    "models/label_encoders.pkl"
)

# ==========================================
# FEATURES & TARGET
# ==========================================

X = df.drop(
    "Risk_Level",
    axis=1
)

y = df["Risk_Level"]

# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# ==========================================
# CREATE RANDOM FOREST MODEL
# ==========================================

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42
)

# ==========================================
# TRAIN MODEL
# ==========================================

print("=" * 60)
print("TRAINING RANDOM FOREST MODEL...")
print("=" * 60)

model.fit(X_train, y_train)

print("\nModel Training Completed Successfully!")

# ==========================================
# MAKE PREDICTIONS
# ==========================================

y_pred = model.predict(X_test)

# ==========================================
# MODEL EVALUATION
# ==========================================

accuracy = accuracy_score(y_test, y_pred)

print("\n" + "=" * 60)
print("MODEL PERFORMANCE")
print("=" * 60)

print(f"\nAccuracy : {accuracy * 100:.2f}%")

print("\nConfusion Matrix:\n")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# ==========================================
# FEATURE IMPORTANCE
# ==========================================

importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\n" + "=" * 60)
print("TOP 10 IMPORTANT FEATURES")
print("=" * 60)

print(importance.head(10))

# ==========================================
# SAVE MODEL
# ==========================================

joblib.dump(
    model,
    "models/risk_model.pkl"
)

# ==========================================
# SAVE FEATURE LIST
# ==========================================

feature_columns = list(X.columns)

joblib.dump(
    feature_columns,
    "models/feature_columns.pkl"
)

# ==========================================
# TRAINING SUMMARY
# ==========================================

print("\n" + "=" * 60)
print("TRAINING COMPLETED SUCCESSFULLY")
print("=" * 60)

print(f"\nTotal Records : {len(df)}")
print(f"Training Records : {len(X_train)}")
print(f"Testing Records : {len(X_test)}")

print("\nModel Saved : models/risk_model.pkl")
print("Label Encoders Saved : models/label_encoders.pkl")
print("Feature List Saved : models/feature_columns.pkl")

print("\nFinal Features Used For Training:\n")

for i, feature in enumerate(feature_columns, start=1):
    print(f"{i}. {feature}")

print("\n" + "=" * 60)
print("Machine Learning Model Ready")
print("=" * 60)