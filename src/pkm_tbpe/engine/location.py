from enum import Enum
from typing import List, Dict, Optional
from .user import User
from .graphics import Graphics
from .sound import Sound
from .encounter import Encounter
from .pokemon import Pokemon
import random
from rich.panel import Panel

class Area(Enum):
    PALLET_TOWN = "Pallet Town"
    VIRIDIAN_CITY = "Viridian City"
    PEWTER_CITY = "Pewter City"
    CERULEAN_CITY = "Cerulean City"
    ROUTE_1 = "Route 1"
    ROUTE_2 = "Route 2"

class Location:
    @classmethod
    def open_map(cls, user: User):
        while True:
            Graphics.console.print("\n[bold blue]--- WORLD MAP ---[/]")
            Graphics.console.print("P: Pallet Town")
            if Area.VIRIDIAN_CITY.value in user.unlocked_locations:
                Graphics.console.print("V: Viridian City")
            if Area.ROUTE_1.value in user.unlocked_locations:
                Graphics.console.print("1: Route 1")
            Graphics.console.print("B: Back")

            choice = input("> ").upper()
            if choice == 'P':
                cls.go_to_pallet_town(user)
            elif choice == 'V' and Area.VIRIDIAN_CITY.value in user.unlocked_locations:
                cls.go_to_viridian_city(user)
            elif choice == '1' and Area.ROUTE_1.value in user.unlocked_locations:
                cls.go_on_route(user, 1)
            elif choice == 'B':
                break

    @classmethod
    def go_to_pallet_town(cls, user: User):
        Sound.play_music("palletTownTheme.mp3")
        while True:
            Graphics.console.print(Panel(Graphics.get_image("printHome"), title="Pallet Town"))
            print("\n1: Visit Mom (Heal)")
            print("2: Visit Prof. Oak's Lab")
            print("3: Go to Route 1")
            print("B: Back to Map")

            choice = input("> ").upper()
            if choice == '1':
                print("Mom: Welcome home! Your Pokemon look tired. Let me heal them.")
                for p in user.party.pokemon:
                    if p: p.hp = p.max_hp
                print("Your party has been healed!")
            elif choice == '2':
                print("Prof. Oak: Keep working on that Pokedex!")
            elif choice == '3':
                user.unlocked_locations.add(Area.ROUTE_1.value)
                cls.go_on_route(user, 1)
            elif choice == 'B':
                break

    @classmethod
    def go_on_route(cls, user: User, route_num: int):
        Sound.play_music("earlyRouteTheme.mp3")
        print(f"\nYou are on Route {route_num}.")

        while True:
            print("\n1: Look for wild Pokemon")
            print("2: Move forward")
            print("B: Back")

            choice = input("> ").upper()
            if choice == '1':
                from .data_manager import DataManager
                wild_pkm = Pokemon(DataManager.get_random_species_name(), random.randint(2, 6))
                Encounter.wild_battle(user, wild_pkm)
                Sound.play_music("earlyRouteTheme.mp3")
            elif choice == '2':
                if route_num == 1:
                    print("You arrived at Viridian City!")
                    user.unlocked_locations.add(Area.VIRIDIAN_CITY.value)
                    cls.go_to_viridian_city(user)
                    break
            elif choice == 'B':
                break

    @classmethod
    def go_to_viridian_city(cls, user: User):
        Sound.play_music("viridianTheme.mp3")
        while True:
            print("\n--- Viridian City ---")
            print("1: Pokemon Center")
            print("2: Mart")
            print("3: Gym (Locked)")
            print("B: Back to Map")

            choice = input("> ").upper()
            if choice == '1':
                print("Healing Pokemon...")
                for p in user.party.pokemon:
                    if p: p.hp = p.max_hp
            elif choice == 'B':
                break
