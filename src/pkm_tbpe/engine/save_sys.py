import json
import os

class SaveSys:
    SAVE_DIR = "saves_py"

    @classmethod
    def save_game(cls, user, slot: int):
        if not os.path.exists(cls.SAVE_DIR):
            os.makedirs(cls.SAVE_DIR)

        filepath = os.path.join(cls.SAVE_DIR, f"save{slot}.json")
        data = {
            "username": user.username,
            "pokedollars": user.bag.pokedollars,
            "unlocked_locations": list(user.unlocked_locations)
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Game saved to slot {slot}.")

    @classmethod
    def load_game(cls, user, slot: int) -> bool:
        filepath = os.path.join(cls.SAVE_DIR, f"save{slot}.json")
        if not os.path.exists(filepath):
            return False

        with open(filepath, "r") as f:
            data = json.load(f)
            user.username = data.get("username", "Cyan")
            user.bag.pokedollars = data.get("pokedollars", 500)
            user.unlocked_locations = set(data.get("unlocked_locations", ["Pallet Town"]))

        print(f"Game loaded from slot {slot}.")
        return True
