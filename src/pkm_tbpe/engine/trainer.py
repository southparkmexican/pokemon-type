from enum import Enum
from typing import List, Optional
from .pokemon import Pokemon

class TrainerTitle(Enum):
    PEWTER_GYM_LEADER = ("Pewter City Gym Leader", "Brock", 2000, True)
    CERULEAN_GYM_LEADER = ("Cerulean City Gym Leader", "Misty", 2000, True)

    def __init__(self, title_str, name, prize, is_major):
        self.title_str = title_str
        self.trainer_name = name
        self.prize = prize
        self.is_major = is_major

class Trainer:
    def __init__(self, title: TrainerTitle):
        self.title = title
        self.name = title.trainer_name
        self.party: List[Optional[Pokemon]] = [None] * 6

    def add_pokemon(self, pkm: Pokemon):
        for i in range(6):
            if self.party[i] is None:
                self.party[i] = pkm
                return
