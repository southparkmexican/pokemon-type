from enum import Enum, auto
from typing import Set, List
from .party import Party
from .bag import Bag

class Gender(Enum):
    BOY = "boy"
    GIRL = "girl"

class Difficulty(Enum):
    EASY = "EASY"
    NORMAL = "NORMAL"
    CHALLENGE = "CHALLENGE"
    PROFESSIONAL = "PROFESSIONAL"

class User:
    def __init__(self):
        self.username: str = "Cyan"
        self.gender: Gender = Gender.BOY
        self.text_speed: int = 2000
        self.difficulty: Difficulty = Difficulty.CHALLENGE

        self.party: Party = Party()
        self.bag: Bag = Bag()

        self.pokedex_registered: Set[str] = set()
        self.badges: List[str] = []

        self.reputation: int = 0
        self.record_colosseum_trainers_beaten: int = 0

        # Progression flags
        self.unlocked_locations: Set[str] = {"Pallet Town"}

    def register_pokemon(self, pkm_name: str):
        self.pokedex_registered.add(pkm_name)
