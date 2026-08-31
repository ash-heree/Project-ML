import os
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Load Dataset
# -------------------------------
df = pd.read_csv("dataset/transaction_risk_dataset_professional_1000.csv")

# Create reports folder
os.makedirs("reports", exist_ok=True)

print("=" * 50)
print("DATASET INFORMATION")
print("=" * 50)

print("\nDataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nData Types:")
print(df.dtypes)

print("\nStatistical Summary:")
print(df.describe())

# -------------------------------
# Risk Level Distribution
# -------------------------------
plt.figure(figsize=(7,5))
df["Risk_Level"].value_counts().plot(kind="bar")
plt.title("Risk Level Distribution")
plt.xlabel("Risk Level")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("reports/risk_level_distribution.png")
plt.show()

# -------------------------------
# Payment Method Distribution
# -------------------------------
plt.figure(figsize=(8,5))
df["Payment_Method"].value_counts().plot(kind="bar")
plt.title("Payment Method Distribution")
plt.xlabel("Payment Method")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("reports/payment_method_distribution.png")
plt.show()

# -------------------------------
# Device Type Distribution
# -------------------------------
plt.figure(figsize=(7,5))
df["Device_Type"].value_counts().plot(kind="bar")
plt.title("Device Type Distribution")
plt.xlabel("Device Type")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("reports/device_type_distribution.png")
plt.show()

# -------------------------------
# Location Distribution
# -------------------------------
plt.figure(figsize=(10,5))
df["Location"].value_counts().plot(kind="bar")
plt.title("Location Distribution")
plt.xlabel("City")
plt.ylabel("Transactions")
plt.tight_layout()
plt.savefig("reports/location_distribution.png")
plt.show()

# -------------------------------
# Transaction Amount Histogram
# -------------------------------
plt.figure(figsize=(8,5))
plt.hist(df["Transaction_Amount"], bins=30)
plt.title("Transaction Amount Distribution")
plt.xlabel("Transaction Amount")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("reports/transaction_amount_distribution.png")
plt.show()

print("\nEDA Completed Successfully!")
print("\nGraphs saved inside 'reports' folder.")