import re
from packages.schemas.intent import ZorielIntent, Budget, LocationContext

FOOD_TERMS = ["biryani", "biriyani", "food", "meal", "dinner", "lunch", "khana", "khaana", "ଭାତ", "ବିରିୟାନି"]

def extract_budget(text: str) -> int | None:
    patterns = [
        r"(?:₹|rs\.?|inr)\s*([0-9][0-9,]*)",
        r"(?:under|below|within|upto|up to|less than)\s*(?:₹|rs\.?|inr)?\s*([0-9][0-9,]*)",
        r"([0-9][0-9,]*)\s*(?:rupees|rs)\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return int(match.group(1).replace(",", ""))
    return None

def extract_quantity(text: str) -> int | None:
    patterns = [
        r"(?:for|of|serves?)\s*(\d+)\s*(?:people|person|pax|log|jana|persons)?\b",
        r"(\d+)\s*(?:people|person|pax|log|jana)\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return int(match.group(1))
    return None

def extract_time(text: str) -> str | None:
    # Only interpret a number as time when it is adjacent to am/pm or a time phrase.
    patterns = [
        r"\b(\d{1,2})(?::(\d{2}))?\s*(am|pm)\b",
        r"\b(?:at|around|by|near)\s+(\d{1,2})(?::(\d{2}))?\b",
        r"\b(\d{1,2})(?::(\d{2}))?\s*(?:baje|bajey)\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if not match:
            continue
        hour = int(match.group(1))
        minute = int(match.group(2) or 0)
        meridiem = match.group(3) if len(match.groups()) >= 3 else None
        is_baje = "baje" in match.group(0) or "bajey" in match.group(0)
        if is_baje and hour < 12:
            hour += 12
        if meridiem == "pm" and hour < 12:
            hour += 12
        if meridiem == "am" and hour == 12:
            hour = 0
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            return f"{hour:02d}:{minute:02d}"
    return None

def parse_intent(text: str, default_city: str = "Bhubaneswar") -> ZorielIntent:
    normalized = text.strip().lower()
    matched_food = next((term for term in FOOD_TERMS if term in normalized), None)
    if not matched_food:
        return ZorielIntent(needs_clarification=True)

    quantity = extract_quantity(normalized)
    budget = extract_budget(normalized)
    requested_time = extract_time(normalized)
    confidence = 0.92
    if quantity is None:
        confidence -= 0.04
    if budget is None:
        confidence -= 0.02

    return ZorielIntent(
        intent="food_order",
        item="biryani" if "biry" in normalized or "ବିରିୟାନି" in normalized else matched_food,
        quantity=quantity,
        budget=Budget(max_amount=budget),
        requested_time=requested_time,
        location=LocationContext(city=default_city),
        confidence=max(confidence, 0.0),
        needs_clarification=False,
    )
