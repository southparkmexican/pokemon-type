import time
import random
from typing import List, Optional, Tuple
from .arena import Arena
from .pokemon import Pokemon
from .fight import Fight
from .graphics import Graphics
from .typing import TypingGame

class Encounter:
    @classmethod
    def wild_battle(cls, user, wild_pokemon: Pokemon):
        arena = Arena(user.party.pokemon, [wild_pokemon])
        print(f"A wild {wild_pokemon.name} appeared!")

        while not arena.is_caught and arena.p0.hp > 0 and arena.fp0.hp > 0:
            Graphics.print_battle_status(arena.p0, arena.fp0, arena.turn_num, arena.weather)

            choice = input("\n[F]ight [B]ag [S]witch [R]un: ").upper()

            if choice == 'F':
                for i, move in enumerate(arena.p0.moves):
                    print(f"[{i+1}] {move.name} ({move.type})")

                try:
                    move_idx = int(input("Choose a move: ")) - 1
                    player_move = arena.p0.moves[move_idx]
                except (ValueError, IndexError):
                    print("Invalid move selection.")
                    continue

                task = TypingGame.get_task(player_move.damage)
                typing_results = TypingGame.run_task(task)

                foe_move = cls.choose_foe_move(arena, arena.fp0, arena.p0)
                cls.resolve_turn(arena, player_move, foe_move, typing_results)

            elif choice == 'R':
                print("You ran away!")
                break

            arena.increment_turns()

        if arena.p0.hp <= 0:
            print(f"Your {arena.p0.name} fainted! You blacked out.")
        elif arena.fp0.hp <= 0:
            print(f"The wild {arena.fp0.name} fainted! You won!")

    @classmethod
    def choose_foe_move(cls, arena: Arena, foe: Pokemon, player: Pokemon):
        best_move = None
        max_dmg = -1
        for move in foe.moves:
            dmg = Fight.calc_damage(arena, move, foe, player, apply_variation=False)
            if dmg > max_dmg:
                max_dmg = dmg
                best_move = move
        return best_move

    @classmethod
    def resolve_turn(cls, arena: Arena, player_move, foe_move, typing_results):
        accuracy, time_taken = typing_results

        player_speed = arena.p0.speed * Fight.get_multiplier(arena.p0.speed_stage)
        task_len = len(player_move.name)
        typing_speed = task_len / max(time_taken, 0.1)
        if typing_speed > 5:
            player_speed *= 1.5

        foe_speed = arena.fp0.speed * Fight.get_multiplier(arena.fp0.speed_stage)

        if player_move.priority > foe_move.priority:
            Fight.use_move(arena, player_move, arena.p0, arena.fp0, typing_results)
            Fight.use_move(arena, foe_move, arena.fp0, arena.p0)
        elif foe_move.priority > player_move.priority:
            Fight.use_move(arena, foe_move, arena.fp0, arena.p0)
            Fight.use_move(arena, player_move, arena.p0, arena.fp0, typing_results)
        elif player_speed >= foe_speed:
            Fight.use_move(arena, player_move, arena.p0, arena.fp0, typing_results)
            Fight.use_move(arena, foe_move, arena.fp0, arena.p0)
        else:
            Fight.use_move(arena, foe_move, arena.fp0, arena.p0)
            Fight.use_move(arena, player_move, arena.p0, arena.fp0, typing_results)
