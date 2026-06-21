from typing import List, Optional
from .pokemon import Pokemon

class Party:
    def __init__(self):
        self.pokemon: List[Optional[Pokemon]] = [None] * 6

    def add(self, pkm: Pokemon) -> bool:
        pkm.is_foe = False
        for i in range(len(self.pokemon)):
            if self.pokemon[i] is None:
                self.pokemon[i] = pkm
                return True
        return False

    def remove(self, index: int) -> Optional[Pokemon]:
        if 0 <= index < len(self.pokemon):
            pkm = self.pokemon[index]
            self.pokemon[index] = None
            return pkm
        return None

    def swap(self, i: int, j: int):
        if 0 <= i < 6 and 0 <= j < 6:
            self.pokemon[i], self.pokemon[j] = self.pokemon[j], self.pokemon[i]

    def smush(self):
        """Move all pokemon to the front of the list."""
        new_party = [p for p in self.pokemon if p is not None]
        while len(new_party) < 6:
            new_party.append(None)
        self.pokemon = new_party

    def get_alive_count(self) -> int:
        return sum(1 for p in self.pokemon if p is not None and p.hp > 0)

    def is_all_fainted(self) -> bool:
        return self.get_alive_count() == 0

    def first_alive_index(self) -> int:
        for i, p in enumerate(self.pokemon):
            if p is not None and p.hp > 0:
                return i
        return -1

    def __iter__(self):
        return iter(self.pokemon)

    def __len__(self):
        return sum(1 for p in self.pokemon if p is not None)
