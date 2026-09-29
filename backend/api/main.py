from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from ai.risk_engine.risk_engine import calculate_risk

app = FastAPI(title="FinShield 360 Risk Engine")


class PaymentRequest(BaseModel):
    payment_id: str
    amount: float
    new_device: bool
    new_beneficiary: bool
    velocity: int
    behavior_anomaly: int
    network_risk: int


@app.get("/")
def home():
    return {
        "message": "FinShield 360 Risk Engine is running"
    }


@app.post("/risk")
def calculate_payment_risk(payment: PaymentRequest):

    result = calculate_risk(
        amount=payment.amount,
        new_device=payment.new_device,
        new_beneficiary=payment.new_beneficiary,
        velocity=payment.velocity,
        behavior_anomaly=payment.behavior_anomaly,
        network_risk=payment.network_risk
    )

    return {
        "payment_id": payment.payment_id,
        "risk_score": result["riskScore"],
        "risk_level": result["riskLevel"],
        "decision": result["decision"],
        "status": result["status"]
    }
