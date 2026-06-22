from typing import List, Optional
from .pokemon import Pokemon

class Arena:
    def __init__(self, player_party: List[Optional[Pokemon]], foe_party: List[Optional[Pokemon]], trainer=None):
        self.turn_num = 1
        self.weather = "None"
        self.turn_weather_ends = 0
        self.trick_room_is_up = False
        self.turn_trick_room_ends = 0
        self.is_caught = False
        self.is_simulation = False

        self.player_party = player_party
        self.foe_party = foe_party
        self.trainer = trainer

    @property
    def p0(self) -> Pokemon:
        return self.player_party[0]

    @property
    def fp0(self) -> Pokemon:
        return self.foe_party[0]

    def increment_turns(self):
        self.turn_num += 1

    def set_up_weather(self, weather: str):
        self.weather = weather
        self.turn_weather_ends = self.turn_num + 4

    def set_up_trick_room(self):
        self.trick_room_is_up = True
        self.turn_trick_room_ends = self.turn_num + 4
