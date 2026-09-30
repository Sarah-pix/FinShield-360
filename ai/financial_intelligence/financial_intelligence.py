def calculate_financial_health(
    payment_risk_score,
    inclusion_score,
    remittance_risk_score,
    tokenized_asset_value,
    savings_behavior,
    successful_transactions
):
    """
    FinShield 360 Financial Intelligence Engine.

    Combines security, financial inclusion, remittance,
    asset and transaction signals into a financial health
    assessment.

    Prototype only — not a credit or lending decision.
    """

    # Security health
    security_score = max(0, 100 - payment_risk_score)

    # Remittance health
    remittance_score = max(0, 100 - remittance_risk_score)

    # Asset score
    if tokenized_asset_value >= 1000000:
        asset_score = 100
    elif tokenized_asset_value >= 500000:
        asset_score = 80
    elif tokenized_asset_value > 0:
        asset_score = 60
    else:
        asset_score = 40

    # Transaction health
    transaction_score = (
        (savings_behavior * 0.50) +
        (successful_transactions * 0.50)
    )

    # Overall financial health
    health_score = (
        security_score * 0.25 +
        inclusion_score * 0.25 +
        remittance_score * 0.15 +
        asset_score * 0.15 +
        transaction_score * 0.20
    )

    health_score = round(
        min(max(health_score, 0), 100),
        2
    )

    # Category
    if health_score >= 80:
        category = "EXCELLENT"
    elif health_score >= 65:
        category = "HEALTHY"
    elif health_score >= 50:
        category = "STABLE"
    elif health_score >= 35:
        category = "NEEDS_ATTENTION"
    else:
        category = "HIGH_RISK"

    # Personalized recommendations
    recommendations = []

    if payment_risk_score >= 60:
        recommendations.append(
            "Review high-risk payment activity and strengthen account security."
        )

    if inclusion_score < 50:
        recommendations.append(
            "Build a more consistent financial transaction history."
        )

    if remittance_risk_score >= 60:
        recommendations.append(
            "Review international transfer activity before processing further remittances."
        )

    if savings_behavior < 50:
        recommendations.append(
            "Consider improving regular savings behavior."
        )

    if successful_transactions < 70:
        recommendations.append(
            "Maintain a higher rate of successful financial transactions."
        )

    if tokenized_asset_value == 0:
        recommendations.append(
            "Explore suitable asset ownership or investment opportunities."
        )

    if not recommendations:
        recommendations.append(
            "Maintain current financial activity and security practices."
        )

    return {
        "financialHealthScore": health_score,
        "category": category,

        "componentScores": {
            "securityScore": round(security_score, 2),
            "inclusionScore": round(inclusion_score, 2),
            "remittanceScore": round(remittance_score, 2),
            "assetScore": round(asset_score, 2),
            "transactionScore": round(transaction_score, 2)
        },

        "recommendations": recommendations,

        "disclaimer":
            "This is a prototype financial intelligence assessment and "
            "must not be used as a lending, credit, investment or eligibility decision."
    }


if __name__ == "__main__":

    result = calculate_financial_health(
        payment_risk_score=20,
        inclusion_score=78,
        remittance_risk_score=15,
        tokenized_asset_value=10000000,
        savings_behavior=70,
        successful_transactions=90
    )

    print("\nFINSHIELD 360 FINANCIAL INTELLIGENCE")
    print("====================================")
    print(
        f"Financial Health Score: "
        f"{result['financialHealthScore']}/100"
    )
    print(f"Category: {result['category']}")

    print("\nRecommendations:")

    for recommendation in result["recommendations"]:
        print(f"- {recommendation}")
