import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from .pokemon import Pokemon

class Graphics:
    console = Console()

    COLOR_MAP = {
        "\u001B[31m": "red",
        "\u001B[32m": "green",
        "\u001B[33m": "yellow",
        "\u001B[34m": "blue",
        "\u001B[35m": "magenta",
        "\u001B[36m": "cyan",
        "\u001B[37m": "white",
        "\u001B[92m": "bright_green",
        "\u001B[94m": "bright_blue",
        "\u001B[93m": "bright_yellow",
        "\u001B[96m": "bright_cyan",
        "\u001B[95m": "bright_magenta",
        "\u001B[0m": "reset",
    }

    @classmethod
    def get_image(cls, name: str) -> str:
        filepath = f"assets/graphics/{name}.txt"
        if not os.path.exists(filepath):
            return f"[Missing Image: {name}]"

        with open(filepath, "r") as f:
            content = f.read()

        rich_content = content
        for ansi, rich_tag in cls.COLOR_MAP.items():
            if rich_tag == "reset":
                rich_content = rich_content.replace(ansi, "[/]")
            else:
                rich_content = rich_content.replace(ansi, f"[{rich_tag}]")

        return rich_content

    @classmethod
    def print_pokemon(cls, pokemon: Pokemon, is_foe: bool = False):
        img_name = pokemon.species_name.lower()
        image_text = cls.get_image(img_name)

        title = f"{pokemon.name} (Lv. {pokemon.level})"
        if pokemon.shiny:
            title += " [yellow]★[/]"

        panel = Panel(Text.from_markup(image_text), title=title, expand=False)
        cls.console.print(panel)

    @classmethod
    def print_battle_status(cls, player_pkm: Pokemon, foe_pkm: Pokemon, turn: int, weather: str):
        player_info = f"[bold]{player_pkm.name}[/]\nHP: {player_pkm.hp}/{player_pkm.max_hp}"
        foe_info = f"[bold]{foe_pkm.name}[/]\nHP: {foe_pkm.hp}/{foe_pkm.max_hp}"

        cls.console.print(Columns([
            Panel(player_info, title="Your Pokemon", border_style="green"),
            Panel(f"Turn: {turn}\nWeather: {weather}", padding=(1, 2)),
            Panel(foe_info, title="Foe Pokemon", border_style="red")
        ]))
