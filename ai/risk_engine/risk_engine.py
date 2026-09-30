def calculate_risk(
    amount,
    new_device,
    new_beneficiary,
    velocity,
    behavior_anomaly,
    network_risk
):
    score = 0
    factors = {}

    # Transaction amount
    if amount > 50000:
        factors["amount_risk"] = 20
    elif amount > 25000:
        factors["amount_risk"] = 10
    else:
        factors["amount_risk"] = 0

    score += factors["amount_risk"]

    # Device trust
    if new_device:
        factors["new_device"] = 15
    else:
        factors["new_device"] = 0

    score += factors["new_device"]

    # Beneficiary trust
    if new_beneficiary:
        factors["new_beneficiary"] = 15
    else:
        factors["new_beneficiary"] = 0

    score += factors["new_beneficiary"]

    # Transaction velocity
    if velocity >= 5:
        factors["velocity_risk"] = 15
    elif velocity >= 3:
        factors["velocity_risk"] = 8
    else:
        factors["velocity_risk"] = 0

    score += factors["velocity_risk"]

    # Behavioral anomaly
    factors["behavior_anomaly"] = behavior_anomaly
    score += behavior_anomaly

    # Network security risk
    factors["network_risk"] = network_risk
    score += network_risk

    # Limit score
    score = min(score, 100)

    # Decision
    if score >= 80:
        risk_level = "CRITICAL"
        decision = "BLOCK"
        status = "BLOCKED"

    elif score >= 60:
        risk_level = "HIGH"
        decision = "HOLD"
        status = "PENDING"

    elif score >= 30:
        risk_level = "MEDIUM"
        decision = "VERIFY"
        status = "PENDING"

    else:
        risk_level = "LOW"
        decision = "APPROVE"
        status = "COMPLETED"

    return {
        "riskScore": score,
        "riskLevel": risk_level,
        "decision": decision,
        "status": status,
        "factors": factors
    }


if __name__ == "__main__":

    result = calculate_risk(
        amount=50000,
        new_device=True,
        new_beneficiary=True,
        velocity=5,
        behavior_anomaly=15,
        network_risk=10
    )

    print("FINSHIELD RISK ENGINE")
    print("----------------------")

    print(f"Risk Score : {result['riskScore']}")
    print(f"Risk Level : {result['riskLevel']}")
    print(f"Decision   : {result['decision']}")
    print(f"Status     : {result['status']}")

    print("\nRisk Factors")
    print("------------")

    for factor, value in result["factors"].items():
        print(f"{factor:20} +{value}")
