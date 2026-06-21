from dataclasses import dataclass
from typing import Optional

@dataclass
class Move:
    name: str
    type: str
    damage: int
    accuracy: int
    effect: str
    effect_accuracy: int
    use_special: bool
    priority: int
    total_pp: int
    current_pp: int

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data["name"],
            type=data["type"],
            damage=data["damage"],
            accuracy=data["accuracy"],
            effect=data["effect"],
            effect_accuracy=data["effect_accuracy"],
            use_special=data["use_special"],
            priority=data["priority"],
            total_pp=data["total_pp"],
            current_pp=data["total_pp"]
        )

    def lower_pp(self):
        if self.current_pp > 0:
            self.current_pp -= 1

    def restore_pp(self, amount: int):
        self.current_pp = min(self.current_pp + amount, self.total_pp)

    def can_use(self) -> bool:
        return self.current_pp > 0

    def __str__(self):
        return f"{self.name} ({self.type} Type, Damage: {self.damage}, Effect: {self.effect}, PP: {self.current_pp}/{self.total_pp})"
