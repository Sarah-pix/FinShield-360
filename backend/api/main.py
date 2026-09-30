import json
import os
import sys

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ---------------------------------------------------------
# Project path
# ---------------------------------------------------------

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# ---------------------------------------------------------
# FinShield modules
# ---------------------------------------------------------

from ai.risk_engine.risk_engine import calculate_risk
from ai.financial_inclusion.inclusion_engine import calculate_inclusion_score
from ai.fraud_detection.fraud_detector import predict_fraud

from backend.drunix_client.drunix_client import (
    create_payment,
    get_all_payments,
)

# ---------------------------------------------------------
# FastAPI
# ---------------------------------------------------------

app = FastAPI(
    title="FinShield 360 API",
    description=(
        "AI-powered financial security, fraud detection, "
        "real-time payment risk analysis and financial inclusion API"
    ),
    version="2.0.0",
)

# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# Payment Request
# ---------------------------------------------------------

class PaymentRequest(BaseModel):
    payment_id: str
    sender: str
    receiver: str
    amount: float = Field(gt=0)
    currency: str = "INR"

    new_device: bool = False
    new_beneficiary: bool = False
    velocity: int = Field(default=1, ge=0)

    behavior_anomaly: int = Field(default=0, ge=0, le=100)
    network_risk: int = Field(default=0, ge=0, le=100)


# ---------------------------------------------------------
# Financial Inclusion Request
# ---------------------------------------------------------

class FinancialInclusionRequest(BaseModel):
    transaction_consistency: float = Field(ge=0, le=100)
    payment_regularity: float = Field(ge=0, le=100)
    account_activity: float = Field(ge=0, le=100)
    savings_behavior: float = Field(ge=0, le=100)
    successful_transactions: float = Field(ge=0, le=100)
    account_age_months: int = Field(ge=0)


# ---------------------------------------------------------
# Root
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "project": "FinShield 360",
        "description": (
            "AI-Powered Financial Trust, Security & "
            "Intelligence Infrastructure"
        ),
        "version": "2.0.0",
        "features": [
            "Real-Time Payment Security",
            "Rule-Based Risk Engine",
            "ML Fraud Detection",
            "Drunix Blockchain Ledger",
            "Financial Inclusion Assessment",
        ],
        "status": "running",
    }


# ---------------------------------------------------------
# Risk Analysis
# ---------------------------------------------------------

@app.post("/risk")
def risk_analysis(request: PaymentRequest):

    result = calculate_risk(
        amount=request.amount,
        new_device=request.new_device,
        new_beneficiary=request.new_beneficiary,
        velocity=request.velocity,
        behavior_anomaly=request.behavior_anomaly,
        network_risk=request.network_risk,
    )

    return {
        "payment_id": request.payment_id,
        "risk": result,
    }


# ---------------------------------------------------------
# Payment Processing
# ---------------------------------------------------------

@app.post("/payment")
def process_payment(request: PaymentRequest):

    # -----------------------------------------------------
    # 1. Rule-based risk engine
    # -----------------------------------------------------

    rule_result = calculate_risk(
        amount=request.amount,
        new_device=request.new_device,
        new_beneficiary=request.new_beneficiary,
        velocity=request.velocity,
        behavior_anomaly=request.behavior_anomaly,
        network_risk=request.network_risk,
    )

    rule_score = int(rule_result["riskScore"])

    # -----------------------------------------------------
    # 2. ML fraud detection
    # -----------------------------------------------------

    ml_result = predict_fraud(
        amount=request.amount,
        new_device=request.new_device,
        new_beneficiary=request.new_beneficiary,
        velocity=request.velocity,
        behavior_anomaly=request.behavior_anomaly,
        network_risk=request.network_risk,
    )

    fraud_score = int(
        ml_result.get("fraud_score", 0)
    )

    fraud_score = max(
        0,
        min(fraud_score, 100)
    )

    prediction = ml_result.get(
        "prediction",
        "UNKNOWN"
    )

    # -----------------------------------------------------
    # 3. Combined score
    # -----------------------------------------------------

    combined_score = round(
        (0.60 * rule_score)
        + (0.40 * fraud_score)
    )

    # -----------------------------------------------------
    # 4. Final security decision
    #
    # Strongest signal is used.
    # -----------------------------------------------------

    decision_score = max(
        rule_score,
        fraud_score
    )

    if decision_score >= 80:

        final_level = "CRITICAL"
        final_decision = "BLOCK"
        final_status = "BLOCKED"

    elif decision_score >= 60:

        final_level = "HIGH"
        final_decision = "HOLD"
        final_status = "PENDING"

    elif decision_score >= 30:

        final_level = "MEDIUM"
        final_decision = "VERIFY"
        final_status = "PENDING"

    else:

        final_level = "LOW"
        final_decision = "APPROVE"
        final_status = "COMPLETED"

    # -----------------------------------------------------
    # 5. Record payment on Drunix
    # -----------------------------------------------------

    drunix_result = create_payment(
        payment_id=request.payment_id,
        sender=request.sender,
        receiver=request.receiver,
        amount=request.amount,
        currency=request.currency,
        risk_score=decision_score,
        risk_level=final_level,
        decision=final_decision,
        status=final_status,
    )

    if drunix_result.get("return_code", 0) != 0:

        raise HTTPException(
            status_code=500,
            detail={
                "message": (
                    "Payment risk analysis succeeded, "
                    "but Drunix recording failed."
                ),
                "drunix": drunix_result,
            },
        )

    # -----------------------------------------------------
    # 6. Response
    # -----------------------------------------------------

    return {
        "message": "Payment processed successfully",

        "payment": {
            "payment_id": request.payment_id,
            "sender": request.sender,
            "receiver": request.receiver,
            "amount": request.amount,
            "currency": request.currency,
        },

        "rule_engine": {
            "score": rule_score,
            "level": rule_result["riskLevel"],
            "decision": rule_result["decision"],
            "status": rule_result["status"],
            "factors": rule_result["factors"],
        },

        "ml_fraud_detection": {
            "fraud_score": fraud_score,
            "prediction": prediction,
        },

        "combined_score": {
            "score": combined_score,
            "rule_weight": "60%",
            "ml_weight": "40%",
        },

        "final_risk": {
            "score": decision_score,
            "level": final_level,
            "decision": final_decision,
            "status": final_status,
            "highest_signal_score": decision_score,
            "explanation": (
                "The final security decision uses the strongest "
                "risk signal from the rule engine and ML fraud detector."
            ),
        },

        "drunix": {
            "recorded": True,
            "result": drunix_result.get("stdout", ""),
        },
    }


# ---------------------------------------------------------
# FINANCIAL INCLUSION
# ---------------------------------------------------------

@app.post("/financial-inclusion")
def financial_inclusion(
    request: FinancialInclusionRequest
):

    result = calculate_inclusion_score(
        transaction_consistency=request.transaction_consistency,
        payment_regularity=request.payment_regularity,
        account_activity=request.account_activity,
        savings_behavior=request.savings_behavior,
        successful_transactions=request.successful_transactions,
        account_age_months=request.account_age_months,
    )

    return {
        "message": "Financial inclusion assessment completed",

        "assessment": result,

        "profile": {
            "transaction_consistency": request.transaction_consistency,
            "payment_regularity": request.payment_regularity,
            "account_activity": request.account_activity,
            "savings_behavior": request.savings_behavior,
            "successful_transactions": request.successful_transactions,
            "account_age_months": request.account_age_months,
        },
    }


# ---------------------------------------------------------
# Get All Payments
# ---------------------------------------------------------

@app.get("/payments")
def payments():

    result = get_all_payments()

    if result.get("return_code", 0) != 0:

        raise HTTPException(
            status_code=500,
            detail={
                "message": "Unable to query Drunix payments",
                "error": result.get("stderr", ""),
            },
        )

    raw_output = result.get("stdout", "").strip()

    if not raw_output:
        return []

    try:
        return json.loads(raw_output)

    except json.JSONDecodeError:

        raise HTTPException(
            status_code=500,
            detail={
                "message": "Invalid JSON returned by Drunix",
                "raw_output": raw_output,
            },
        )


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "FinShield 360 API",
        "components": {
            "risk_engine": "active",
            "ml_fraud_detection": "active",
            "financial_inclusion": "active",
            "drunix": "connected",
        },
    }
