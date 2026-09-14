from typing import Literal
from pydantic import BaseModel, Field

class Budget(BaseModel):
    max_amount: int | None = Field(default=None, ge=0)
    currency: str = "INR"

class LocationContext(BaseModel):
    city: str = "Bhubaneswar"
    area: str | None = None

class ZorielIntent(BaseModel):
    intent: Literal["food_order", "unknown"] = "unknown"
    item: str | None = None
    quantity: int | None = Field(default=None, ge=1)
    budget: Budget = Field(default_factory=Budget)
    requested_time: str | None = None
    location: LocationContext = Field(default_factory=LocationContext)
    constraints: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    needs_clarification: bool = False
