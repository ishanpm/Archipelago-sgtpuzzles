from math import ceil
from worlds.generic.Rules import set_rule
from BaseClasses import LocationProgressType, MultiWorld
from .Items import max_puzzles
from .options import SimonTathamPuzzlesOptions


# Sets rules on entrances and advancements that are always applied
def set_rules(multiworld: MultiWorld, player: int, options: SimonTathamPuzzlesOptions, puzzles: list[str]):
    for i in range(200):
        if i < len(puzzles):
            set_rule(multiworld.get_location(f"Puzzle {i+1} Reward", player), lambda state, i=i: state.has(f"Puzzle {i+1}", player, 1))
        else:
            multiworld.get_location(f"Puzzle {i+1} Reward", player).progress_type = LocationProgressType.EXCLUDED


# Sets rules on completion condition
def set_completion_rules(multiworld: MultiWorld, player: int, options: SimonTathamPuzzlesOptions, puzzles: list[str]):
    target_puzzles = ceil(len(puzzles) * options.completion_percentage / 100)
    multiworld.completion_condition[player] = lambda state: state.has_from_list_unique(
        [f"Puzzle {i+1}" for i in range(200)], player, target_puzzles)
