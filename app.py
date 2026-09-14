from pathlib import Path
from uuid import uuid4
import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from packages.schemas.intent import ZorielIntent
from services.ai.intent import parse_intent
from services.search.catalog import CatalogSearch
from services.commerce.service import CommerceService

load_dotenv()
BASE = Path(__file__).parent
catalog = CatalogSearch(BASE / "data" / "real_catalog.json")
commerce = CommerceService(catalog)

app = FastAPI(title="Zoriel Commerce Engine", version="0.3.0")

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    context: dict = Field(default_factory=dict)

class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    budget: int | None = None
    location: str = "Bhubaneswar"

class OrderRequest(BaseModel):
    item_id: str
    permission: bool = False

@app.get("/api/health")
def health():
    return {"ok": True, "service": "zoriel-commerce", "version": "0.3.0", "mode": os.getenv("ZORIEL_MODE", "live-discovery-pilot"), "city": catalog.city}

@app.get("/api/meta")
def meta():
    return {"city": catalog.city, "last_checked": catalog.last_checked, "notice": catalog.data["notice"], "mode": os.getenv("ZORIEL_MODE", "live-discovery-pilot")}

@app.post("/api/intent", response_model=ZorielIntent)
def intent(req: ChatRequest):
    return parse_intent(req.message, default_city=catalog.city)

@app.post("/api/chat")
def chat(req: ChatRequest):
    parsed = parse_intent(req.message, default_city=catalog.city)
    if parsed.needs_clarification:
        return {
            "intent": parsed.intent,
            "needs_clarification": True,
            "reply": "Tell me what you need. You can speak naturally — for example, ‘5 jana ke liye ₹1000 ke andar biryani, 7 baje ke aas-paas.’",
            "structured_intent": parsed.model_dump(),
            "results": [],
        }
    results = commerce.discover(parsed.budget.max_amount, parsed.quantity)
    return {
        "intent": parsed.intent,
        "budget": parsed.budget.max_amount,
        "people": parsed.quantity,
        "location": parsed.location.city,
        "timing": parsed.requested_time or "Flexible",
        "confidence": parsed.confidence,
        "needs_clarification": False,
        "reply": f"I found {len(results)} relevant options around {catalog.city}. I ranked them for your request; live price and availability are re-checked at the seller before purchase.",
        "structured_intent": parsed.model_dump(),
        "results": results,
        "source": "current-discovery-pilot",
        "last_checked": catalog.last_checked,
    }

@app.post("/api/search")
def search(req: SearchRequest):
    return {"results": commerce.discover(req.budget), "source": "current-discovery-pilot", "last_checked": catalog.last_checked}

@app.post("/api/orders")
def order(req: OrderRequest):
    prepared = commerce.prepare_purchase(req.item_id)
    if prepared is None:
        raise HTTPException(404, "Item not found")
    if not req.permission:
        return {"status": "permission_required", "message": "Zoriel will never place a purchase without your explicit approval."}
    return {
        "status": "handoff",
        "order_id": "ZR-" + uuid4().hex[:8].upper(),
        "item": prepared["item"],
        "message": "v0.3 opens the verified seller surface. Direct ONDC checkout/payment begins after Buyer NP onboarding and certification.",
    }

app.mount("/", StaticFiles(directory=BASE / "static", html=True), name="static")
