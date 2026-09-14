import json, math
from pathlib import Path

class CatalogSearch:
    def __init__(self, data_path: Path):
        self.data = json.loads(data_path.read_text(encoding="utf-8"))

    @property
    def city(self):
        return self.data["city"]

    @property
    def last_checked(self):
        return self.data["last_checked"]

    def rank(self, budget=None, quantity=None, limit=8):
        return sorted(self.data["items"], key=lambda item: self._score(item, budget, quantity), reverse=True)[:limit]

    @staticmethod
    def _score(item, budget=None, quantity=None):
        rating = item.get("rating") or 4.0
        reviews = item.get("reviews") or 0
        price = item.get("price")
        score = rating * 20 + min(math.log10(reviews + 1) * 8, 32)
        if budget is not None:
            if price is not None:
                score += 22 if price <= budget else -35
                if price <= budget:
                    score += max(0, 10 - (budget - price) / max(budget, 1) * 10)
            else:
                score += 2
        if quantity and price and "serves" in item.get("name", "").lower():
            score += 3
        return score
