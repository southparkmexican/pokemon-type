from typing import Dict, List

class Bag:
    def __init__(self):
        self.pokedollars: int = 500
        self.bp: int = 0
        self.debt: int = 0
        self.gold_bars: int = 0
        self.stock_portfolio: Dict[str, int] = {}

        self.battle_items: Dict[str, int] = {
            "Pokeball": 5,
            "Potion": 5,
            "Super Potion": 1,
            "Hyper Potion": 1,
            "Revive": 1,
            "Full Heal": 1
        }
        self.special_items: Dict[str, int] = {
            "Rare Candy": 1
        }
        self.notes: Dict[str, List[str]] = {}

    def add_item(self, item_name: str, count: int = 1):
        if item_name in self.battle_items:
            self.battle_items[item_name] += count
        else:
            self.battle_items[item_name] = count

    def remove_item(self, item_name: str, count: int = 1) -> bool:
        if item_name in self.battle_items and self.battle_items[item_name] >= count:
            self.battle_items[item_name] -= count
            return True
        return False

    def add_pokedollars(self, amount: int):
        self.pokedollars += amount

    def remove_pokedollars(self, amount: int) -> bool:
        if self.pokedollars >= amount:
            self.pokedollars -= amount
            return True
        return False
