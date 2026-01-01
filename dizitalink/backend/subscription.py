from fastapi import APIRouter, HTTPException
from datetime import datetime

router = APIRouter()


@router.get("/api/subscriptions")
def list_subscriptions():
    """Return a simple placeholder list of subscriptions."""
    return {"subscriptions": [], "generated_at": datetime.utcnow().isoformat()}


@router.post("/api/subscriptions")
def create_subscription(item: dict):
    # placeholder implementation
    if not item:
        raise HTTPException(status_code=400, detail="Invalid payload")
    item["id"] = "sub_placeholder"
    item["created_at"] = datetime.utcnow().isoformat()
    return {"success": True, "subscription": item}
