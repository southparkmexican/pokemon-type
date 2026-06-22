import random
from dataclasses import dataclass, field
from typing import List, Optional
from .species import Species
from .move import Move
from .data_manager import DataManager

@dataclass
class Pokemon:
    species_name: str
    level: int
    shiny: bool = False
    name: str = ""
    type1: str = ""
    type2: str = ""

    # Base stats
    base_hp: int = 0
    base_attack: int = 0
    base_defense: int = 0
    base_sp_atk: int = 0
    base_sp_def: int = 0
    base_speed: int = 0

    # Current stats (calculated from level)
    max_hp: int = 0
    hp: int = 0
    attack: int = 0
    defense: int = 0
    sp_atk: int = 0
    sp_def: int = 0
    speed: int = 0

    # Moves
    moves: List[Move] = field(default_factory=list)

    # Battle state
    status_condition: str = "None"
    is_foe: bool = True
    turn_sent_out: int = 0
    wake_up_turn: int = 0

    # Stat stages
    attack_stage: int = 0
    defense_stage: int = 0
    sp_atk_stage: int = 0
    sp_def_stage: int = 0
    speed_stage: int = 0
    accuracy_stage: int = 0
    evasion_stage: int = 0

    def __post_init__(self):
        species = DataManager.get_species(self.species_name)
        if not self.name:
            self.name = species.name
        self.type1 = species.type1
        self.type2 = species.type2

        self.base_hp = species.base_stats["hp"]
        self.base_attack = species.base_stats["attack"]
        self.base_defense = species.base_stats["defense"]
        self.base_sp_atk = species.base_stats["sp_atk"]
        self.base_sp_def = species.base_stats["sp_def"]
        self.base_speed = species.base_stats["speed"]

        self.calculate_stats()
        self.hp = self.max_hp

        for move_name in species.moves:
            self.moves.append(DataManager.get_move(move_name))

    def calculate_stats(self):
        self.max_hp = int(10 + self.base_hp * (self.level / 50.0))
        self.attack = int(5 + self.base_attack * (self.level / 50.0))
        self.defense = int(5 + self.base_defense * (self.level / 50.0))
        self.sp_atk = int(5 + self.base_sp_atk * (self.level / 50.0))
        self.sp_def = int(5 + self.base_sp_def * (self.level / 50.0))
        self.speed = int(5 + self.base_speed * (self.level / 50.0))

    def reset_stages(self):
        self.attack_stage = 0
        self.defense_stage = 0
        self.sp_atk_stage = 0
        self.sp_def_stage = 0
        self.speed_stage = 0
        self.accuracy_stage = 0
        self.evasion_stage = 0

    @staticmethod
    def get_shiny_odds() -> bool:
        return random.randint(1, 4096) == 1

    def __str__(self):
        shiny_str = " (Shiny)" if self.shiny else ""
        return f"Lvl {self.level} {self.name}{shiny_str} - HP: {self.hp}/{self.max_hp}"
