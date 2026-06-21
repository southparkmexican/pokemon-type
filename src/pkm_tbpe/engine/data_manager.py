import json
from typing import Dict
from .species import Species
from .move import Move

class DataManager:
    _species: Dict[str, Species] = {}
    _moves: Dict[str, Move] = {}

    @classmethod
    def load_data(cls):
        with open('data/species.json', 'r') as f:
            species_data = json.load(f)
            for key, data in species_data.items():
                cls._species[key.lower()] = Species.from_dict(data)

        with open('data/moves.json', 'r') as f:
            moves_data = json.load(f)
            for key, data in moves_data.items():
                cls._moves[key] = data # Keep as dict to instantiate fresh Moves

    @classmethod
    def get_species(cls, name: str) -> Species:
        return cls._species.get(name.lower(), cls._species["default"])

    @classmethod
    def get_move(cls, name: str) -> Move:
        data = cls._moves.get(name, cls._moves["Move Not Found"])
        return Move.from_dict(data)

    @classmethod
    def get_all_species_names(cls):
        return list(cls._species.keys())
