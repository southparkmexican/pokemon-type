import random
from typing import Optional, List, Tuple
from .arena import Arena
from .pokemon import Pokemon
from .move import Move
from .typing import TypingGame

class Fight:
    TYPE_CHART = {
        "Normal": {"Rock": 0.5, "Ghost": 0.0, "Steel": 0.5},
        "Fire": {"Fire": 0.5, "Water": 0.5, "Grass": 2.0, "Ice": 2.0, "Bug": 2.0, "Rock": 0.5, "Dragon": 0.5, "Steel": 2.0},
        "Water": {"Fire": 2.0, "Water": 0.5, "Grass": 0.5, "Ground": 2.0, "Rock": 2.0, "Dragon": 0.5},
        "Electric": {"Water": 2.0, "Electric": 0.5, "Grass": 0.5, "Ground": 0.0, "Flying": 2.0, "Dragon": 0.5},
        "Grass": {"Fire": 0.5, "Water": 2.0, "Grass": 0.5, "Poison": 0.5, "Ground": 2.0, "Flying": 0.5, "Bug": 0.5, "Rock": 2.0, "Dragon": 0.5, "Steel": 0.5},
        "Ice": {"Fire": 0.5, "Water": 0.5, "Grass": 2.0, "Ice": 0.5, "Ground": 2.0, "Flying": 2.0, "Dragon": 2.0, "Steel": 0.5},
        "Fighting": {"Normal": 2.0, "Ice": 2.0, "Poison": 0.5, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Rock": 2.0, "Ghost": 0.0, "Dark": 2.0, "Steel": 2.0, "Fairy": 0.5},
        "Poison": {"Grass": 2.0, "Poison": 0.5, "Ground": 0.5, "Rock": 0.5, "Ghost": 0.5, "Steel": 0.0, "Fairy": 2.0},
        "Ground": {"Fire": 2.0, "Electric": 2.0, "Grass": 0.5, "Poison": 2.0, "Flying": 0.0, "Bug": 0.5, "Rock": 2.0, "Steel": 2.0},
        "Flying": {"Electric": 0.5, "Grass": 2.0, "Fighting": 2.0, "Bug": 2.0, "Rock": 0.5, "Steel": 0.5},
        "Psychic": {"Fighting": 2.0, "Poison": 2.0, "Psychic": 0.5, "Dark": 0.0, "Steel": 0.5},
        "Bug": {"Fire": 0.5, "Grass": 2.0, "Fighting": 0.5, "Poison": 0.5, "Flying": 0.5, "Psychic": 2.0, "Ghost": 0.5, "Dark": 2.0, "Steel": 0.5, "Fairy": 0.5},
        "Rock": {"Fire": 2.0, "Ice": 2.0, "Fighting": 0.5, "Ground": 0.5, "Flying": 2.0, "Bug": 2.0, "Steel": 0.5},
        "Ghost": {"Normal": 0.0, "Psychic": 2.0, "Ghost": 2.0, "Dark": 0.5},
        "Dragon": {"Dragon": 2.0, "Steel": 0.5, "Fairy": 0.0},
        "Dark": {"Fighting": 0.5, "Psychic": 2.0, "Ghost": 2.0, "Dark": 0.5, "Fairy": 0.5},
        "Steel": {"Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Ice": 2.0, "Rock": 2.0, "Steel": 0.5, "Fairy": 2.0},
        "Fairy": {"Fire": 0.5, "Fighting": 2.0, "Poison": 0.5, "Dragon": 2.0, "Dark": 2.0, "Steel": 0.5},
        "None": {}
    }

    @classmethod
    def get_type_effectiveness(cls, attack_type: str, target_type: str) -> float:
        if target_type == "None":
            return 1.0
        return cls.TYPE_CHART.get(attack_type, {}).get(target_type, 1.0)

    @classmethod
    def get_stab(cls, move: Move, pokemon: Pokemon) -> float:
        if move.type == pokemon.type1 or move.type == pokemon.type2:
            return 1.5
        return 1.0

    @classmethod
    def get_weather_multiplier(cls, arena: Arena, move: Move) -> float:
        if arena.weather == "Rainy":
            if move.type == "Water": return 1.5
            if move.type == "Fire": return 0.5
        if arena.weather == "Sunny":
            if move.type == "Fire": return 1.5
            if move.type == "Water": return 0.5
        return 1.0

    @classmethod
    def get_multiplier(cls, stage: int) -> float:
        if stage >= 0: return (2 + stage) / 2
        return 2 / (2 - abs(stage))

    @classmethod
    def calc_damage(cls, arena: Arena, move: Move, dealer: Pokemon, recipient: Pokemon, typing_accuracy: float = 1.0, apply_variation: bool = True) -> int:
        if move.damage == 0:
            return 0

        lvl_mult = (2.0 * dealer.level / 5.0) + 2.0

        burn_mult = 0.5 if dealer.status_condition == "Burn" and not move.use_special else 1.0

        if move.use_special:
            atk = dealer.sp_atk * cls.get_multiplier(dealer.sp_atk_stage)
            dfn = recipient.sp_def * cls.get_multiplier(recipient.sp_def_stage)
        else:
            atk = dealer.attack * cls.get_multiplier(dealer.attack_stage) * burn_mult
            dfn = recipient.defense * cls.get_multiplier(recipient.defense_stage)

        effectiveness = cls.get_type_effectiveness(move.type, recipient.type1) * \
                        cls.get_type_effectiveness(move.type, recipient.type2)

        stab = cls.get_stab(move, dealer)
        weather = cls.get_weather_multiplier(arena, move)

        eruption_mult = 1.0
        if move.name in ["Water Spout", "Eruption"]:
            eruption_mult = dealer.hp / max(dealer.max_hp, 1)

        damage = (((lvl_mult * move.damage * (atk / max(dfn, 1))) / 50.0) + 2.0) * stab * effectiveness * weather * eruption_mult * typing_accuracy

        if apply_variation:
            variation = random.uniform(0.85, 1.0)
            damage *= variation
        else:
            damage *= 0.925

        return int(damage)

    @classmethod
    def use_move(cls, arena: Arena, move: Move, dealer: Pokemon, recipient: Pokemon, typing_results: Optional[Tuple[float, float]] = None):
        if dealer.hp <= 0 or recipient.hp <= 0:
            return

        accuracy, time_taken = typing_results if typing_results else (1.0, 0.0)

        print(f"\n{dealer.name} used {move.name}!")

        hit_threshold = random.randint(1, 100)
        if hit_threshold > move.accuracy * accuracy:
            print(f"But it missed!")
            return

        damage = cls.calc_damage(arena, move, dealer, recipient, accuracy)
        recipient.hp = max(0, recipient.hp - damage)

        if damage > 0:
            print(f"It did {damage} damage!")
            effectiveness = cls.get_type_effectiveness(move.type, recipient.type1) * \
                            cls.get_type_effectiveness(move.type, recipient.type2)
            if effectiveness > 1.0:
                print("It's super effective!")
            elif effectiveness < 1.0 and effectiveness > 0:
                print("It's not very effective...")
            elif effectiveness == 0:
                print(f"It doesn't affect {recipient.name}...")

        if move.effect != "None" and random.randint(1, 100) <= move.effect_accuracy:
            cls.apply_effect(arena, move.effect, dealer, recipient)

    @classmethod
    def apply_effect(cls, arena: Arena, effect: str, dealer: Pokemon, recipient: Pokemon):
        if effect == "Opponent Attack -1":
            recipient.attack_stage = max(-6, recipient.attack_stage - 1)
            print(f"{recipient.name}'s Attack fell!")
        elif effect == "Opponent Defense -1":
            recipient.defense_stage = max(-6, recipient.defense_stage - 1)
            print(f"{recipient.name}'s Defense fell!")
        elif effect == "Own Attack +1":
            dealer.attack_stage = min(6, dealer.attack_stage + 1)
            print(f"{dealer.name}'s Attack rose!")
