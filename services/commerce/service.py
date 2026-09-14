class CommerceService:
    """Provider-agnostic commerce boundary. Real adapters will plug in here."""
    def __init__(self, catalog):
        self.catalog = catalog

    def discover(self, budget=None, quantity=None):
        return self.catalog.rank(budget=budget, quantity=quantity)

    def prepare_purchase(self, item_id: str):
        item = next((x for x in self.catalog.data["items"] if x["id"] == item_id), None)
        if item is None:
            return None
        return {"status": "handoff_required", "item": item}
