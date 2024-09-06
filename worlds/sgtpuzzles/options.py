from Options import Choice, CommonOptions, DefaultOnToggle, ExcludeLocations, ItemLinks, LocalItems, \
    NonLocalItems, OptionGroup, PriorityLocations, StartHints, StartInventory, StartLocationHints, Toggle, Range, \
    OptionDict, StartInventoryPool
from dataclasses import dataclass

from schema import Schema, Optional, And, Or, Any

genres = [
    "blackbox","bridges","cube","dominosa","fifteen","filling","flip","flood","galaxies",
    "guess","inertia","keen","lightup","loopy","magnets","map","mines","mosaic","net",
    "netslide","palisade","pattern","pearl","pegs","range","rect","samegame","signpost",
    "singles","sixteen","slant","solo","tents","towers","tracks","twiddle","undead",
    "unequal","unruly","untangle"
]

genrePresets = {
    "blackbox": ["w8h8m5M5"],
    "dominosa": ["3dt"],
    "loopy": ["7x7","10x10"],
    "net": ["7x7","10x10","7x7w","10x10w"],
    "solo": ["2x3db"],
    "fifteen": ["2x2","3x3","4x4"]
}

class PuzzleCount(Range):
    """
    Number of puzzles to randomly generate.
    """
    range_start = 1
    range_end = 200
    default = 50

class StartingPuzzles(Range):
    """
    Number of puzzles to randomly add to the starting inventory. These will be
    removed from the item pool (along with those in Start Inventory).
    """
    range_start = 0
    range_end = 20
    default = 5

class CompletionPercentage(Range):
    """
    Percent of puzzles which must be completed to finish the world, rounding up.
    """
    display_name = "Target Completion Percentage"
    range_start = 50
    range_end = 100
    default = 90

class GenreWeights(OptionDict):
    """
    Relative chance for each genre to be selected as a random preset.
    """
    schema = Schema({
        Optional(g): Or(float, int) for g in genres
    })
    default = {g: 10 for g in genres}

class PresetOverrides(OptionDict):
    """
    List of presets to use for a given genre. Replaces the default presets for that puzzle if specified.
    """
    default = {}

sgtpuzzles_option_groups = [
    OptionGroup("Game Options", [
        PuzzleCount,
        StartingPuzzles,
        CompletionPercentage,
        GenreWeights,
        PresetOverrides
    ])
]

@dataclass
class SimonTathamPuzzlesOptions(CommonOptions):
    puzzle_count: PuzzleCount
    starting_puzzles: StartingPuzzles
    completion_percentage: CompletionPercentage
    genre_weights: GenreWeights
    preset_overrides: PresetOverrides

    local_items: LocalItems
    non_local_items: NonLocalItems
    start_inventory: StartInventoryPool
    start_hints: StartHints
    start_location_hints: StartLocationHints
    exclude_locations: ExcludeLocations
    priority_locations: PriorityLocations
    item_links: ItemLinks