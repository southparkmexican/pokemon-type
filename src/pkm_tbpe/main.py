import sys
import random
import time
from .engine.data_manager import DataManager
from .engine.user import User
from .engine.pokemon import Pokemon
from .engine.encounter import Encounter
from .engine.graphics import Graphics
from .engine.save_sys import SaveSys
from .engine.sound import Sound
from .engine.location import Location
from .engine.casino import Casino

def main():
    Sound.init()
    Sound.play_music("titleMusic.mp3")

    Graphics.console.print("[bold green]Initializing Data...[/]")
    DataManager.load_data()

    user = User()
    # Try to load default save if exists
    SaveSys.load_game(user, 0)

    print(Graphics.get_image("printSmallTitleImage"))
    print("\nWelcome to POKEMON TEXT-BASED PYTHON EDITION!")

    if not user.party.pokemon[0]:
        starter = Pokemon("bulbasaur", 5)
        user.party.add(starter)
        user.register_pokemon(starter.species_name)

    while True:
        Sound.play_music("titleMusic.mp3")
        print("\n--- MAIN MENU ---")
        print("[M] Open Map")
        print("[B] Check Bag")
        print("[P] Party")
        print("[W] Wild Battle (Test)")
        print("[C] Casino (Blackjack)")
        print("[S] Save Game")
        print("[E] Exit")

        choice = input("> ").upper()

        if choice == 'M':
            Location.open_map(user)
        elif choice == 'B':
            print(f"\n--- BAG ---")
            print(f"Pokedollars: ${user.bag.pokedollars}")
            print(f"Items: {user.bag.battle_items}")
        elif choice == 'P':
            print(f"\n--- YOUR PARTY ---")
            for i, p in enumerate(user.party.pokemon):
                if p:
                    print(f"[{i+1}] {p}")
                else:
                    print(f"[{i+1}] Empty")
        elif choice == 'W':
            Sound.play_music("wildBattleTheme.mp3")
            wild_name = DataManager.get_random_species_name()
            wild_pkm = Pokemon(wild_name, random.randint(3, 10))
            Encounter.wild_battle(user, wild_pkm)
            Sound.play_music("titleMusic.mp3")
        elif choice == 'C':
            Casino.start_blackjack(user)
        elif choice == 'S':
            SaveSys.save_game(user, 0)
        elif choice == 'E':
            print("Goodbye!")
            sys.exit()

if __name__ == "__main__":
    main()
