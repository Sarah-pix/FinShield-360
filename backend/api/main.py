from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

from ai.risk_engine.risk_engine import calculate_risk
from ai.fraud_detection.fraud_detector import predict_fraud
from ai.financial_inclusion.inclusion_engine import calculate_inclusion_score
from ai.remittance.remittance_engine import calculate_remittance

from backend.drunix_client.drunix_client import (
    create_payment,
    get_all_payments
)


# ============================================================
# FINSHIELD 360 API
# ============================================================

app = FastAPI(
    title="FinShield 360 API",
    description="AI-Powered Financial Trust, Security & Intelligence Infrastructure",
    version="2.1.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST MODELS
# ============================================================

class PaymentRequest(BaseModel):
    payment_id: str
    sender: str
    receiver: str
    amount: float
    currency: str = "INR"

    new_device: bool = False
    new_beneficiary: bool = False
    velocity: int = 1
    behavior_anomaly: int = 0
    network_risk: int = 0


class FinancialInclusionRequest(BaseModel):
    transaction_consistency: float
    payment_regularity: float
    account_activity: float
    savings_behavior: float
    successful_transactions: float
    account_age_months: int


class RemittanceRequest(BaseModel):
    sender_country: str
    receiver_country: str
    amount: float
    exchange_rate: float
    transfer_fee: float
    purpose: str
    risk_score: int = 0


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "project": "FinShield 360",
        "description": "AI-Powered Financial Trust, Security & Intelligence Infrastructure",
        "version": "2.1.0",
        "features": [
            "Real-Time Payment Security",
            "Rule-Based Risk Engine",
            "ML Fraud Detection",
            "Drunix Blockchain Ledger",
            "Financial Inclusion Assessment",
            "Cross-Border Remittance"
        ],
        "status": "running"
    }


# ============================================================
# REAL-TIME PAYMENT SECURITY
# ============================================================

@app.post("/payment")
def process_payment(request: PaymentRequest):

    try:

        # Rule-based risk engine
        rule_result = calculate_risk(
            amount=request.amount,
            new_device=request.new_device,
            new_beneficiary=request.new_beneficiary,
            velocity=request.velocity,
            behavior_anomaly=request.behavior_anomaly,
            network_risk=request.network_risk
        )

        rule_score = rule_result["riskScore"]

        # ML fraud detection
        ml_result = predict_fraud(
            amount=request.amount,
            new_device=request.new_device,
            new_beneficiary=request.new_beneficiary,
            velocity=request.velocity,
            behavior_anomaly=request.behavior_anomaly,
            network_risk=request.network_risk
        )

        fraud_score = ml_result["fraud_score"]

        # Combined score
        combined_score = round(
            (rule_score * 0.60) +
            (fraud_score * 0.40)
        )

        # Strongest security signal
        decision_score = max(
            rule_score,
            fraud_score
        )

        # Final decision
        if decision_score >= 80:
            final_risk_level = "CRITICAL"
            final_decision = "BLOCK"
            final_status = "BLOCKED"

        elif decision_score >= 60:
            final_risk_level = "HIGH"
            final_decision = "HOLD"
            final_status = "PENDING"

        elif decision_score >= 30:
            final_risk_level = "MEDIUM"
            final_decision = "VERIFY"
            final_status = "PENDING"

        else:
            final_risk_level = "LOW"
            final_decision = "APPROVE"
            final_status = "COMPLETED"

        # Record payment on Drunix
        drunix_result = create_payment(
            payment_id=request.payment_id,
            sender=request.sender,
            receiver=request.receiver,
            amount=request.amount,
            currency=request.currency,
            risk_score=decision_score,
            risk_level=final_risk_level,
            decision=final_decision,
            status=final_status
        )

        if drunix_result.get("return_code", 0) != 0:
            raise HTTPException(
                status_code=500,
                detail={
                    "message": "Payment security analysis completed but Drunix recording failed",
                    "drunix_error": drunix_result.get("stderr", "")
                }
            )

        return {
            "message": "Payment processed successfully",

            "payment": {
                "payment_id": request.payment_id,
                "sender": request.sender,
                "receiver": request.receiver,
                "amount": request.amount,
                "currency": request.currency
            },

            "rule_engine": {
                "score": rule_score,
                "level": rule_result["riskLevel"],
                "decision": rule_result["decision"],
                "status": rule_result["status"],
                "factors": rule_result["factors"]
            },

            "ml_fraud_detection": {
                "fraud_score": fraud_score,
                "prediction": ml_result["prediction"]
            },

            "combined_score": {
                "score": combined_score,
                "rule_weight": "60%",
                "ml_weight": "40%"
            },

            "final_risk": {
                "score": decision_score,
                "level": final_risk_level,
                "decision": final_decision,
                "status": final_status,
                "highest_signal_score": decision_score,
                "explanation":
                    "The final security decision uses the strongest risk signal from the rule engine and ML fraud detector."
            },

            "drunix": {
                "recorded": True,
                "result": drunix_result.get("stdout", "")
            }
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Payment processing failed: {str(e)}"
        )


# ============================================================
# FINANCIAL INCLUSION
# ============================================================

@app.post("/financial-inclusion")
def assess_financial_inclusion(
    request: FinancialInclusionRequest
):

    try:

        result = calculate_inclusion_score(
            transaction_consistency=request.transaction_consistency,
            payment_regularity=request.payment_regularity,
            account_activity=request.account_activity,
            savings_behavior=request.savings_behavior,
            successful_transactions=request.successful_transactions,
            account_age_months=request.account_age_months
        )

        return {
            "message": "Financial inclusion assessment completed",
            "assessment": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Financial inclusion assessment failed: {str(e)}"
        )


# ============================================================
# CROSS-BORDER REMITTANCE
# ============================================================

@app.post("/remittance")
def process_remittance(
    request: RemittanceRequest
):

    try:

        result = calculate_remittance(
            sender_country=request.sender_country,
            receiver_country=request.receiver_country,
            amount=request.amount,
            exchange_rate=request.exchange_rate,
            transfer_fee=request.transfer_fee,
            purpose=request.purpose,
            risk_score=request.risk_score
        )

        return {
            "message": "Cross-border remittance assessed successfully",
            "remittance": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Remittance processing failed: {str(e)}"
        )


# ============================================================
# PAYMENT HISTORY
# ============================================================

@app.get("/payments")
def payments():

    try:

        result = get_all_payments()

        if result.get("return_code", 0) != 0:
            raise HTTPException(
                status_code=500,
                detail={
                    "message": "Unable to retrieve payment history",
                    "error": result.get("stderr", "")
                }
            )

        try:
            payments_data = json.loads(
                result.get("stdout", "[]")
            )

        except json.JSONDecodeError:
            payments_data = []

        return {
            "count": len(payments_data),
            "payments": payments_data
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Payment history failed: {str(e)}"
        )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",

        "components": {
            "api": "active",
            "risk_engine": "active",
            "ml_fraud_detection": "active",
            "financial_inclusion": "active",
            "cross_border_remittance": "active",
            "drunix": "connected"
        }
    }
