import os
import pygame

class Sound:
    _initialized = False
    _current_music = None

    @classmethod
    def init(cls):
        if not cls._initialized:
            try:
                pygame.mixer.init()
                cls._initialized = True
            except Exception:
                pass

    @classmethod
    def play_music(cls, filename: str, loop: bool = True):
        if not cls._initialized:
            return

        filepath = os.path.join("assets", filename)
        if not os.path.exists(filepath):
            if not filename.startswith("music/"):
                filepath = os.path.join("assets/music", filename)

        if not os.path.exists(filepath):
            return

        try:
            if cls._current_music == filepath:
                return

            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play(-1 if loop else 0)
            cls._current_music = filepath
        except Exception:
            pass

    @classmethod
    def stop_music(cls):
        if cls._initialized:
            pygame.mixer.music.stop()
            cls._current_music = None

    @classmethod
    def play_sound(cls, filename: str):
        if not cls._initialized:
            return

        filepath = os.path.join("assets", filename)
        if not os.path.exists(filepath):
            if not filename.startswith("music/"):
                filepath = os.path.join("assets/music", filename)

        if not os.path.exists(filepath):
            return

        try:
            sound = pygame.mixer.Sound(filepath)
            sound.play()
        except Exception:
            pass
