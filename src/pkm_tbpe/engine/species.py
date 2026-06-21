from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Species:
    name: str
    type1: str
    type2: str
    evolution_level: int
    base_stats: Dict[str, int]
    moves: List[str]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data["name"],
            type1=data["type1"],
            type2=data["type2"],
            evolution_level=data["evolution_level"],
            base_stats=data["base_stats"],
            moves=data["moves"]
        )
