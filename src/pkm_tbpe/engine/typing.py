import time
import random
from typing import Tuple

class TypingGame:
    SENTENCES = [
        "The quick brown fox jumps over the lazy dog.",
        "A wizard's job is to vex chumps quickly in fog.",
        "Sphinx of black quartz, judge my vow.",
        "Pack my box with five dozen liquor jugs.",
        "How vexingly quick daft zebras jump!",
        "The five boxing wizards jump quickly.",
        "Jaded zombies acted quaintly but kept driving their oxen forward.",
        "Six big devils from Japan quickly forgot how to Waltz."
    ]

    WORDS = [
        "pokemon", "battle", "attack", "defense", "speed", "accuracy", "trainer",
        "champion", "evolution", "legendary", "victory", "defeat", "strength",
        "power", "element", "spirit", "journey", "adventure", "friendship"
    ]

    @classmethod
    def get_task(cls, power: int) -> str:
        if power == 0:
            return random.choice(cls.WORDS).lower()
        elif power < 50:
            return random.choice(cls.WORDS)
        elif power < 90:
            word1 = random.choice(cls.WORDS)
            word2 = random.choice(cls.WORDS)
            return f"{word1} {word2}"
        else:
            return random.choice(cls.SENTENCES)

    @classmethod
    def run_task(cls, target_text: str) -> Tuple[float, float]:
        print("\n--- TYPING TASK ---")
        print(f"Type this: {target_text}")
        print("Ready...")
        time.sleep(1)
        print("GO!")

        start_time = time.time()
        typed_text = input("> ")
        end_time = time.time()

        time_taken = end_time - start_time

        matches = 0
        min_len = min(len(target_text), len(typed_text))
        for i in range(min_len):
            if target_text[i] == typed_text[i]:
                matches += 1

        accuracy = matches / max(len(target_text), 1)

        if len(typed_text) > len(target_text):
            accuracy -= (len(typed_text) - len(target_text)) / len(target_text)
            accuracy = max(0.0, accuracy)

        return accuracy, time_taken
