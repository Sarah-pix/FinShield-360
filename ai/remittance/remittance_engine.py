def calculate_remittance(
    sender_country,
    receiver_country,
    amount,
    exchange_rate,
    transfer_fee,
    purpose,
    risk_score
):
    """
    Cross-Border Remittance Assessment Engine
    """

    # Currency conversion
    converted_amount = amount * exchange_rate

    # Amount after transfer fee
    final_amount = max(converted_amount - transfer_fee, 0)

    # Basic compliance/risk assessment
    if risk_score >= 80:
        risk_level = "CRITICAL"
        decision = "BLOCK"
        status = "BLOCKED"

    elif risk_score >= 60:
        risk_level = "HIGH"
        decision = "HOLD"
        status = "PENDING"

    elif risk_score >= 30:
        risk_level = "MEDIUM"
        decision = "VERIFY"
        status = "PENDING"

    else:
        risk_level = "LOW"
        decision = "APPROVE"
        status = "COMPLETED"

    return {
        "senderCountry": sender_country,
        "receiverCountry": receiver_country,
        "amount": amount,
        "exchangeRate": exchange_rate,
        "transferFee": transfer_fee,
        "convertedAmount": round(converted_amount, 2),
        "finalAmount": round(final_amount, 2),
        "purpose": purpose,
        "riskScore": risk_score,
        "riskLevel": risk_level,
        "decision": decision,
        "status": status
    }
