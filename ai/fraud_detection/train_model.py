import os
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


# ============================================================
# Synthetic training data
#
# Features:
# 0 = transaction amount
# 1 = new device
# 2 = new beneficiary
# 3 = transaction velocity
# 4 = behavior anomaly
# 5 = network risk
# ============================================================

X = [
    [500, 0, 0, 1, 0, 5],
    [1000, 0, 0, 1, 5, 5],
    [2000, 0, 0, 2, 5, 10],
    [5000, 0, 0, 2, 10, 10],
    [10000, 0, 1, 2, 10, 10],
    [15000, 0, 1, 3, 15, 15],
    [25000, 1, 1, 3, 20, 20],
    [30000, 1, 1, 4, 20, 25],
    [40000, 1, 1, 5, 25, 25],
    [50000, 1, 1, 5, 30, 30],
    [75000, 1, 1, 6, 35, 35],
    [100000, 1, 1, 8, 40, 40],

    [800, 0, 0, 1, 0, 2],
    [1200, 0, 0, 1, 2, 5],
    [3000, 0, 0, 2, 3, 5],
    [7000, 0, 1, 2, 5, 10],
    [12000, 0, 1, 3, 10, 15],
    [20000, 1, 0, 3, 10, 15],
    [35000, 1, 1, 4, 20, 20],
    [60000, 1, 1, 6, 30, 30],

    [1500, 0, 0, 1, 0, 0],
    [2500, 0, 0, 1, 0, 5],
    [4500, 0, 0, 2, 5, 5],
    [9000, 0, 0, 2, 5, 10],
    [18000, 0, 1, 2, 10, 10],
    [22000, 1, 0, 3, 10, 15],
    [28000, 1, 1, 4, 15, 20],
    [45000, 1, 1, 5, 25, 25],
    [55000, 1, 1, 6, 30, 30],
    [90000, 1, 1, 7, 40, 40],
]


# 0 = legitimate
# 1 = suspicious/fraudulent

y = [
    0, 0, 0, 0, 0, 0,
    1, 1, 1, 1, 1, 1,

    0, 0, 0, 0, 0, 0,
    1, 1,

    0, 0, 0, 0, 0, 1,
    1, 1, 1, 1
]


# ============================================================
# Train model
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)


model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)


# ============================================================
# Evaluate
# ============================================================

predictions = model.predict(X_test)

print("\nFINSHIELD FRAUD MODEL")
print("=====================")

print(classification_report(
    y_test,
    predictions,
    zero_division=0
))


# ============================================================
# Save model
# ============================================================

model_path = os.path.join(
    os.path.dirname(__file__),
    "fraud_model.joblib"
)

joblib.dump(model, model_path)

print(f"Model saved to: {model_path}")
