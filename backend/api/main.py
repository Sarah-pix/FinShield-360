from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ai.risk_engine.risk_engine import calculate_risk
from ai.fraud_detection.fraud_detector import predict_fraud
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
    version="1.0.0"
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
# PAYMENT REQUEST MODEL
# ============================================================

class PaymentRequest(BaseModel):

    payment_id: str
    sender: str
    receiver: str
    amount: float
    currency: str

    new_device: bool
    new_beneficiary: bool

    velocity: int
    behavior_anomaly: int
    network_risk: int


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "FinShield 360 API is running",
        "version": "1.0.0",
        "services": [
            "Rule-Based Risk Engine",
            "ML Fraud Detection",
            "Drunix Blockchain",
            "Payment Security API"
        ]
    }


# ============================================================
# RISK ENDPOINT
# ============================================================

@app.post("/risk")
def calculate_payment_risk(payment: PaymentRequest):

    rule_result = calculate_risk(
        amount=payment.amount,
        new_device=payment.new_device,
        new_beneficiary=payment.new_beneficiary,
        velocity=payment.velocity,
        behavior_anomaly=payment.behavior_anomaly,
        network_risk=payment.network_risk
    )

    return {
        "score": rule_result["riskScore"],
        "level": rule_result["riskLevel"],
        "decision": rule_result["decision"],
        "status": rule_result["status"],
        "factors": rule_result["factors"]
    }


# ============================================================
# PAYMENT PROCESSING
# ============================================================

@app.post("/payment")
def process_payment(payment: PaymentRequest):

    # ========================================================
    # STEP 1 — RULE-BASED RISK ENGINE
    # ========================================================

    rule_result = calculate_risk(
        amount=payment.amount,
        new_device=payment.new_device,
        new_beneficiary=payment.new_beneficiary,
        velocity=payment.velocity,
        behavior_anomaly=payment.behavior_anomaly,
        network_risk=payment.network_risk
    )

    rule_score = int(rule_result["riskScore"])


    # ========================================================
    # STEP 2 — ML FRAUD DETECTION
    # ========================================================

    ml_result = predict_fraud(
        amount=payment.amount,
        new_device=payment.new_device,
        new_beneficiary=payment.new_beneficiary,
        velocity=payment.velocity,
        behavior_anomaly=payment.behavior_anomaly,
        network_risk=payment.network_risk
    )

    fraud_score = int(round(ml_result["fraud_score"]))


    # ========================================================
    # STEP 3 — WEIGHTED COMBINED SCORE
    #
    # Rule Engine = 60%
    # ML Model    = 40%
    # ========================================================

    combined_score = round(
        (0.60 * rule_score) +
        (0.40 * fraud_score)
    )

    combined_score = min(combined_score, 100)


    # ========================================================
    # STEP 4 — DECISION-DRIVING SCORE
    #
    # We don't want a strong security signal to disappear
    # because it is averaged with a weaker signal.
    #
    # Example:
    # Rule Engine = 33
    # ML          = 5
    # Combined    = 22
    #
    # Decision-driving score = 33
    # ========================================================

    decision_score = max(
        rule_score,
        fraud_score
    )

    decision_score = min(
        decision_score,
        100
    )


    # ========================================================
    # STEP 5 — FINAL SECURITY DECISION
    # ========================================================

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


    # ========================================================
    # STEP 6 — RECORD PAYMENT ON DRUNIX
    #
    # IMPORTANT:
    # Drunix stores the decision-driving score.
    # ========================================================

    drunix_result = create_payment(
        payment_id=payment.payment_id,
        sender=payment.sender,
        receiver=payment.receiver,
        amount=payment.amount,
        currency=payment.currency,
        risk_score=decision_score,
        risk_level=final_level,
        decision=final_decision,
        status=final_status
    )


    # ========================================================
    # STEP 7 — HANDLE DRUNIX ERROR
    # ========================================================

    if drunix_result["return_code"] != 0:

        error_message = (
            drunix_result.get("stderr")
            or drunix_result.get("stdout")
            or "Unknown Drunix transaction error"
        )

        raise HTTPException(
            status_code=500,
            detail={
                "message": "Drunix transaction failed",
                "error": error_message
            }
        )


    # ========================================================
    # STEP 8 — FINAL API RESPONSE
    # ========================================================

    return {

        "message": "Payment processed successfully",


        # ----------------------------------------------------
        # PAYMENT INFORMATION
        # ----------------------------------------------------

        "payment": {

            "payment_id": payment.payment_id,

            "sender": payment.sender,

            "receiver": payment.receiver,

            "amount": payment.amount,

            "currency": payment.currency

        },


        # ----------------------------------------------------
        # RULE ENGINE RESULT
        # ----------------------------------------------------

        "rule_engine": {

            "score": rule_score,

            "level": rule_result["riskLevel"],

            "decision": rule_result["decision"],

            "status": rule_result["status"],

            "factors": rule_result["factors"]

        },


        # ----------------------------------------------------
        # ML FRAUD DETECTION RESULT
        # ----------------------------------------------------

        "ml_fraud_detection": {

            "fraud_score": fraud_score,

            "prediction": ml_result["prediction"]

        },


        # ----------------------------------------------------
        # WEIGHTED COMBINED SCORE
        # ----------------------------------------------------

        "combined_score": {

            "score": combined_score,

            "rule_weight": "60%",

            "ml_weight": "40%"

        },


        # ----------------------------------------------------
        # FINAL SECURITY DECISION
        # ----------------------------------------------------

        "final_risk": {

            "score": decision_score,

            "level": final_level,

            "decision": final_decision,

            "status": final_status,

            "highest_signal_score": decision_score,

            "explanation": (
                "The final security decision uses the strongest "
                "risk signal from the rule engine and ML fraud detector."
            )

        },


        # ----------------------------------------------------
        # DRUNIX BLOCKCHAIN
        # ----------------------------------------------------

        "drunix": {

            "recorded": True,

            "result": (
                drunix_result.get("stdout", "").strip()
            )

        }

    }


# ============================================================
# GET ALL PAYMENTS FROM DRUNIX
# ============================================================

@app.get("/payments")
def payments():

    result = get_all_payments()


    # --------------------------------------------------------
    # HANDLE QUERY ERROR
    # --------------------------------------------------------

    if result["return_code"] != 0:

        error_message = (
            result.get("stderr")
            or result.get("stdout")
            or "Unable to retrieve payments"
        )

        raise HTTPException(
            status_code=500,
            detail={
                "message": "Unable to retrieve payments from Drunix",
                "error": error_message
            }
        )


    # --------------------------------------------------------
    # PARSE BLOCKCHAIN RESPONSE
    # --------------------------------------------------------

    try:

        import json

        payment_data = json.loads(
            result["stdout"]
        )

    except Exception:

        payment_data = []


    # --------------------------------------------------------
    # RETURN HISTORY
    # --------------------------------------------------------

    return {

        "count": len(payment_data),

        "payments": payment_data

    }
