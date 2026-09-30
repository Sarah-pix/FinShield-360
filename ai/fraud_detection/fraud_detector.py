import os
import joblib


MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "fraud_model.joblib"
)


model = joblib.load(MODEL_PATH)


def predict_fraud(
    amount,
    new_device,
    new_beneficiary,
    velocity,
    behavior_anomaly,
    network_risk
):
    features = [[
        amount,
        int(new_device),
        int(new_beneficiary),
        velocity,
        behavior_anomaly,
        network_risk
    ]]

    prediction = model.predict(features)[0]

    probabilities = model.predict_proba(features)[0]

    fraud_probability = probabilities[1]

    fraud_score = round(fraud_probability * 100)

    if prediction == 1:
        prediction_label = "SUSPICIOUS"
    else:
        prediction_label = "LEGITIMATE"

    return {
        "fraud_score": fraud_score,
        "prediction": prediction_label
    }


if __name__ == "__main__":

    result = predict_fraud(
        amount=50000,
        new_device=True,
        new_beneficiary=True,
        velocity=5,
        behavior_anomaly=15,
        network_risk=10
    )

    print("\nFINSHIELD ML FRAUD DETECTOR")
    print("===========================")
    print(f"Fraud Score : {result['fraud_score']}")
    print(f"Prediction  : {result['prediction']}")
