import random
from typing import Optional
from .arena import Arena
from .pokemon import Pokemon
from .move import Move

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
    def calc_damage(cls, arena: Arena, move: Move, dealer: Pokemon, recipient: Pokemon, apply_variation: bool = True) -> int:
        if move.damage == 0:
            return 0

        lvl_mult = (2.0 * dealer.level / 5.0) + 2.0

        # Effective Attack and Defense
        burn_mult = 0.5 if dealer.status_condition == "Burn" and not move.use_special else 1.0

        # Simulating getStatMultiplier from Java - basic implementation
        def get_multiplier(stage):
            if stage >= 0: return (2 + stage) / 2
            return 2 / (2 - stage)

        if move.use_special:
            atk = dealer.sp_atk * get_multiplier(dealer.sp_atk_stage)
            dfn = recipient.sp_def * get_multiplier(recipient.sp_def_stage)
        else:
            atk = dealer.attack * get_multiplier(dealer.attack_stage) * burn_mult
            dfn = recipient.defense * get_multiplier(recipient.defense_stage)

        effectiveness = cls.get_type_effectiveness(move.type, recipient.type1) * \
                        cls.get_type_effectiveness(move.type, recipient.type2)

        stab = cls.get_stab(move, dealer)
        weather = cls.get_weather_multiplier(arena, move)

        eruption_mult = 1.0
        if move.name in ["Water Spout", "Eruption"]:
            eruption_mult = dealer.hp / dealer.max_hp

        damage = (((lvl_mult * move.damage * (atk / dfn)) / 50.0) + 2.0) * stab * effectiveness * weather * eruption_mult

        if apply_variation:
            variation = random.uniform(0.85, 1.0)
            damage *= variation
        else:
            damage *= 0.925 # Java's default dmgRoll for calcDamageWithoutVariation

        return int(damage)
