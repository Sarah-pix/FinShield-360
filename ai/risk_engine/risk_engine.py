def calculate_risk(
    amount,
    new_device,
    new_beneficiary,
    velocity,
    behavior_anomaly,
    network_risk
):
    score = 0

    # Transaction amount
    if amount > 50000:
        score += 20
    elif amount > 25000:
        score += 10

    # Device trust
    if new_device:
        score += 15

    # Beneficiary trust
    if new_beneficiary:
        score += 15

    # Transaction velocity
    if velocity >= 5:
        score += 15
    elif velocity >= 3:
        score += 8

    # Behavioral anomaly
    score += behavior_anomaly

    # Network security risk
    score += network_risk

    # Limit score
    score = min(score, 100)

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
        "status": status
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
