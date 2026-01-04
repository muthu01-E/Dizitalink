from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import uuid4
import os

from .database import subscriptions_collection

router = APIRouter()


class CreateSubscription(BaseModel):
    name: str | None = None
    email: str | None = None
    upi_id: str | None = None
    plan: str = Field(default="premium")
    amount: int = Field(default=999)
    selected_app: str | None = None


@router.get("/api/subscriptions")
def list_subscriptions():
    """Return all subscriptions from the database (simple list)."""
    docs = list(subscriptions_collection.find({}, {"_id": 0}).sort("created_at", -1))
    return {"subscriptions": docs, "count": len(docs)}


@router.post("/api/subscriptions")
def create_subscription(item: CreateSubscription):
    """Create a subscription and return UPI payment links/QR data.

    This endpoint stores a subscription entry with status 'pending' and
    returns the UPI URL that the frontend can turn into a QR or deeplink.
    """
    merchant_upi = os.getenv("MERCHANT_UPI", "merchant@upi")
    merchant_name = os.getenv("MERCHANT_NAME", "Dizitalink")

    if item.amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount")

    sub_id = str(uuid4())
    created_at = datetime.utcnow().isoformat()

    # upi payload (raw UPI URI)
    upi_uri = f"upi://pay?pa={merchant_upi}&pn={merchant_name}&am={item.amount}&tn={sub_id}&cu=INR"

    # provide app-specific deep links where applicable
    deeplinks = {
        "default": upi_uri,
        "PhonePe": upi_uri.replace("upi://", "phonepe://"),
        "Paytm": upi_uri.replace("upi://", "paytmmp://"),
        "GPay": upi_uri.replace("upi://", "tez://upi/"),
    }

    doc = {
        "id": sub_id,
        "name": item.name,
        "email": item.email,
        "upi_id": item.upi_id,
        "plan": item.plan,
        "amount": item.amount,
        "selected_app": item.selected_app,
        "status": "pending",
        "created_at": created_at,
        "upi_uri": upi_uri,
    }

    try:
        subscriptions_collection.insert_one(doc)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to persist subscription")

    return {"success": True, "subscription": doc, "deeplinks": deeplinks}


@router.post("/api/subscriptions/{sub_id}/confirm")
def confirm_subscription(sub_id: str, payload: dict):
    """Mark a subscription as paid.

    In a production integration this should be driven by a webhook from a
    payment provider or by server-side verification of the UPI transaction.
    Here we accept a transaction id and mark the record as 'paid'.
    """
    txid = payload.get("transaction_id")
    if not txid:
        raise HTTPException(status_code=400, detail="transaction_id required")

    res = subscriptions_collection.update_one({"id": sub_id}, {"$set": {"status": "paid", "paid_at": datetime.utcnow().isoformat(), "transaction_id": txid}})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="subscription not found")

    return {"success": True, "id": sub_id, "transaction_id": txid}
