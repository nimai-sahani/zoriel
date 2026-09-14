from services.ai.intent import parse_intent

def test_hinglish_food_request():
    intent = parse_intent("5 jana ke liye ₹1000 ke andar biryani 7 baje ke aas paas")
    assert intent.intent == "food_order"
    assert intent.item == "biryani"
    assert intent.quantity == 5
    assert intent.budget.max_amount == 1000
    assert intent.requested_time == "19:00"
    assert intent.location.city == "Bhubaneswar"

def test_budget_without_time():
    intent = parse_intent("good dinner under 500")
    assert intent.budget.max_amount == 500
    assert intent.requested_time is None

def test_ambiguous_request_clarifies():
    intent = parse_intent("woh wali achhi si cheez chahiye jo kal li thi")
    assert intent.needs_clarification is True
