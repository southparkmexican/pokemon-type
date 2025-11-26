# Pokemon Text Based Java Edition (pokemon-tbje)
![title_img.png](resources/title_img.png)

**A terminal-based Pokémon battle game, written in Java, complete with 241 species, faithful game mechanics, adjustable difficulty, dynamic AI, procedurally generated opponents, random wild encounters, competitive battles, and custom graphics. Built from scratch over 2 months.**

## Features
- 241 Pokémon with stats, types, evolutions, moves, and sprites
- Real battle mechanics: type matchups, stat changes, status effects, weather
- Smart AI trained via custom in-engine ML multi-threaded simulation
- Dynamic difficulty scaling, procedurally generated trainers/opponents
- Full single-player campaign: gym leaders, wild encounters, Team Rocket, Colosseum, and Elite Four
- Improved money system: Proper bank, loans, stocks, gold assets, and a casino with playable mini-games!
- Terminal UI using Unicode + ANSI escape strings
- Catching system, items, switching, trick room, and more
- Save file system to track all progress

## Build and Run
Open a terminal (anything should work but recommendations: Mac - iTerm2 | Linux - Kitty/Konsole | Windows - MSYS2)
```
cd <where/you/keep/java/projects>
git clone https://github.com/zachMahan64/pokemon-tbje.git
# make sure you have the latest versions of Java and Maven before proceeding:
java --version # should say >= Java 24
mvn --version  # ^ same
cd pokemon-tbje
mvn clean package
java -jar target/pokemon_tbje-1.0.jar

# add this alias (POSIX only) for ease, if you want (& edit the path):
echo 'alias pkm="cd ~/<path/to>/pokemon-tbje/ && java -jar target/pokemon_tbje-1.0.jar"' >> ~/.bashrc # or ~/.zshrc, etc.
source ~/.bashrc # or ~/.zshrc, etc. 
# now you can do this to play anytime:
pkm
```
Note: saves are always loaded in `saves/` *parallel* to the directory you start up pkm-tbje! The alias provided above handles this consistently for you.
Tips:
- Make sure:
  - your terminal is at least ~ 70 x 120 characters (adjust to your own liking, though) 
  - your terminal font is size is < 14.0 (not too important as long as you have at least ~70 rows) and line spacing is set to 1.0 (crucial for visual proportions)!
  - you're using a mono-spaced font for proper graphics proportions

## AI Engine
- Analyzes matchups in real-time based on game state and 30+ engine parameters
- Trained with smart parameter tweaking algorithm which uses 1-prop z-tests to check for statistical significance on improvements from parameter tweaks
- Scores moves and switches with a point total system
- Provides live move/switch recommendations & shows match-up & move ratings
- Allows player to run battle simulations mid-game to estimate win probabilities
- Opposing trainers never blunder on `PROFESSIONAL` difficulty (except for an intentional .1% of the time). Trainers in `CHALLENGE` are similarly smart most of the time but choose 2nd and 3rd best moves more often. In `NORMAL`, they choose less optimal moves more often, and, in `EASY`, they choose nearly random moves.
- This was probably the hardest part of the entire game to program (besides, well, writing the entire battle logic for Pokémon from scratch)
- **See screenshot section for the game analysis interface**

## Visuals & Audio
- Uses Unicode braille characters as pixel-art dot matrices. Also uses ANSI escape strings for color.
- All coloring was done by hand (painfully).
- Dot-converted Pokémon, trainer, and location images. Used: https://emojicombos.com/dot-art-generator (amazing website, btw).
- Background music & sound effects via JavaFX (YouTube-sourced MP3s and waveforms, I do not own the rights)
- Over 50 soundtracks and sound effects are in the game!
- Disclaimer: All assets used for educational purposes.
- **See screenshot section to view visuals for yourself**

## Platform Support
- Works best on **Mac/Linux** terminals.
- Windows' terminal may clobber the visuals a bit due to character spacing issues. Try using MSYS2 on Windows!
- Potential build issues: the build will fail if Java or Maven are not pointing to open-jdk-24. Ensure Java 24 is installed on your computer.

## Notes
- This was my first large coding project. The codebase isn't great (in quite a few places). A lot of it has been painstakingly refactored, though.
- Project on hold for now, but might revisit in the future!
## Screenshots
![battle_sim_demo.png](resources/battle_sim_demo.png)
^ see the match-up analysis interface (and our shiny charizard)
![map.png](resources/map.png)
^ map coloring isn't completely finished (manually inserting ansi escape strings is quite tedious)
![move_ratings_demo.png](resources/move_ratings_demo.png)
^ see move rating interface
![rocketopolis.png](resources/rocketopolis.png)
^ see the largest among the game's cities; there are a lot of activities to do
![south_kanto_sea.png](resources/south_kanto_sea.png)
^ route 19 (a water route along the sea)
![squirtle_vs_celebi.ong.png](resources/squirtle_vs_celebi.ong.png)
^ lvl 5 squirtle vs lvl 40 celebi; match-up doesn't look great for us
![the_colosseum_outside.png](resources/the_colosseum_outside.png)
^ the outside of the battle colosseum, fun
![the_colosseum_demo.png](resources/the_colosseum_demo.png)
^ the inside of the colosseum, this is a long battle rush where opponents' parties scale to your party's size, level, and stats. you get progressively more BP (battle points) as your win streak increases and you can steal one of your opponent's pokemon in each battle after reaching 25 record wins in a row. this is a quick way to get many rare pokemon.
![play_menu.png](resources/play_menu.png)
^ play menu -> open map to go to locations, etc. see badges, level cap, reputation, etc are tracked. the date is based on the in-game storyline. the difficulty is shown ('PROFESSIONAL' is the hardest with the smartest opponents). 
![tyranitar_vs_venusaur.png](resources/tyranitar_vs_venusaur.png)
^ tyranitar vs venusaur; doesn't look good for us, we should switch to mewtwo!
![vaughan_distric_gyn.png](resources/vaughan_distric_gyn.png)
^ exterior of a gym
![viridian_city_gym.png](resources/viridian_city_gym.png)
^ another gym exterior
![blastoise_vs_dragonite.png](resources/blastoise_vs_dragonite.png)
^ blastoise vs dragonite
![giovanni.png](resources/giovanni.png)
^ Giovanni, one of the hardest gym leaders you face
![party_selection_screen.png](resources/party_selection_screen.png)
^ what you see when you have to switch in a battle. here, the engine is saying to switch to mewtwo!
![pikachu_last_hope.png](resources/pikachu_last_hope.png)
^ pikachu, save us! see how he's our last pokemon left (as indicated by `oxxxxx`). `o` is our alive pikachu and each `x` is a fainted party member!
![pokedex.png](resources/pokedex.png)
^ the pokedex menu!
![pokedex_list.png](resources/pokedex_list.png)
^ list of all pokemon in the pokedex; red is uncaught and green are caught pokemon.
![mew_pkdx.png](resources/mew_pkdx.png)
^ searching up mew in pokedex! look at all that sweet data
![secret_shop.png](resources/secret_shop.png)
^ an unassuming hot dog stand that doubles as a way to purchase pokemon (totally not a black market)
