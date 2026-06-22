import json
import random
from typing import Dict, List
from .species import Species
from .move import Move

class DataManager:
    _species: Dict[str, Species] = {}
    _moves: Dict[str, dict] = {}

    @classmethod
    def load_data(cls):
        with open('data/species.json', 'r') as f:
            species_data = json.load(f)
            for key, data in species_data.items():
                cls._species[key.lower()] = Species.from_dict(data)

        with open('data/moves.json', 'r') as f:
            cls._moves = json.load(f)

    @classmethod
    def get_species(cls, name: str) -> Species:
        return cls._species.get(name.lower(), cls._species["default"])

    @classmethod
    def get_move(cls, name: str) -> Move:
        data = cls._moves.get(name, cls._moves.get("Move Not Found"))
        if not data:
            return Move(name="Unknown", type="Normal", damage=0, accuracy=0, effect="None", effect_accuracy=0, use_special=False, priority=0, total_pp=10, current_pp=10)
        return Move.from_dict(data)

    @classmethod
    def get_all_species_names(cls):
        return [n for n in cls._species.keys() if n != 'default']

    @classmethod
    def get_random_species_name(cls) -> str:
        names = cls.get_all_species_names()
        return random.choice(names)
