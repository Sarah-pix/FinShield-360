def calculate_inclusion_score(
    transaction_consistency,
    payment_regularity,
    account_activity,
    savings_behavior,
    successful_transactions,
    account_age_months
):
    score = 0
    factors = {}

    # Transaction consistency: 0-100
    factors["transaction_consistency"] = transaction_consistency * 0.20
    score += factors["transaction_consistency"]

    # Payment regularity: 0-100
    factors["payment_regularity"] = payment_regularity * 0.20
    score += factors["payment_regularity"]

    # Account activity: 0-100
    factors["account_activity"] = account_activity * 0.15
    score += factors["account_activity"]

    # Savings behavior: 0-100
    factors["savings_behavior"] = savings_behavior * 0.15
    score += factors["savings_behavior"]

    # Successful transactions: 0-100
    factors["successful_transactions"] = successful_transactions * 0.20
    score += factors["successful_transactions"]

    # Account age contribution
    age_score = min(account_age_months / 60 * 100, 100)
    factors["account_age"] = age_score * 0.10
    score += factors["account_age"]

    score = round(min(score, 100), 2)

    if score >= 70:
        category = "ELIGIBLE"
        recommendation = "ACCESS_SUPPORT"
    elif score >= 50:
        category = "REVIEW"
        recommendation = "MANUAL_REVIEW"
    else:
        category = "LIMITED"
        recommendation = "BUILD_FINANCIAL_HISTORY"

    return {
        "inclusionScore": score,
        "category": category,
        "recommendation": recommendation,
        "factors": {
            key: round(value, 2)
            for key, value in factors.items()
        }
    }
