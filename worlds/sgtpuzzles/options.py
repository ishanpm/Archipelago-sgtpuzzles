from Options import Choice, CommonOptions, DefaultOnToggle, ExcludeLocations, ItemLinks, LocalItems, \
    NonLocalItems, OptionGroup, PriorityLocations, StartHints, StartInventory, StartLocationHints, Toggle, Range, \
    OptionDict, StartInventoryPool
from dataclasses import dataclass

from schema import Schema, Optional, And, Or, Any

genres = [
    "blackbox","bridges","cube","dominosa","fifteen","filling","flip","flood","galaxies",
    "group","guess","inertia","keen","lightup","loopy","magnets","map","mines","mosaic","net",
    "netslide","palisade","pattern","pearl","pegs","range","rect","samegame","signpost",
    "singles","sixteen","slant","solo","tents","towers","tracks","twiddle","undead",
    "unequal","unruly","untangle"
]

genrePresets = {
    "blackbox": ["w8h8m5M5"],
    "bridges": ["7x7i30e10m2d0"],
    "cube": ["c4x4"],
    "dominosa": ["3dt"],
    "fifteen": ["2x2","3x3","4x4"],
    "filling": ["9x7","13x9"],
    "flip": ["3x3c","4x4c","5x5c","3x3r"],
    "flood": ["12x12c6m5"],
    "galaxies": ["7x7dn"],
    "group": ["6dn","6dni"],
    "guess": ["c6p4g10Bm"],
    "inertia": ["10x8"],
    "keen": ["4de"],
    "lightup": ["7x7b20s4d0"],
    "loopy": ["7x7t0de","10x10t0de"],
    "magnets": ["6x5de","6x5dt","6x5dtS"],
    "map": ["20x15n30dn"],
    "mines": ["9x9n10","9x9n35"],
    "mosaic": ["3x3","5x5"],
    "net": ["5x5","7x7","9x9","5x5w","7x7w","9x9w"],
    "netslide": ["3x3b1","3x3","3x3wb1","3x3w"],
    "palisade": ["5x5n5","8x6n6"],
    "pattern": ["10x10","15x15"],
    "pearl": ["6x6de","6x6dt","8x8de","8x8dt"],
    "pegs": ["5x5random"],
    "range": ["9x6"],
    "rect": ["7x7","9x9"],
    "samegame": ["5x5c3s2","10x5c3s2"],
    "signpost": ["4x4c","4x4"],
    "singles": ["5x5de"],
    "sixteen": ["2x2","3x3","4x3","4x4"],
    "slant": ["5x5de","5x5dh","8x8de"],
    "solo": ["2x3db"],
    "tents": ["8x8de"],
    "towers": ["4de","5de"],
    "tracks": ["8x8de","8x8dt"],
    "twiddle": ["3x3n2r","3x3n2","3x3n2o"],
    "undead": ["4x4de","4x4dn"],
    "unequal": ["4de","5ade"],
    "unruly": ["8x8dt"],
    "untangle": ["6","10"]
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
    removed from the item pool.
    """
    range_start = 0
    range_end = 20
    default = 5

class CompletionPercentage(Range):
    """
    Percent of puzzles which must be completed to finish the world, rounding up.
    """
    display_name = "Target Completion Percentage"
    range_start = 20
    range_end = 100
    default = 90

class GenreWeights(OptionDict):
    """
    Relative chance for each genre to be selected as a random preset. Remove a
    genre from this list to disable it.
    """
    schema = Schema({
        Optional(g): Or(float, int) for g in genres
    })
    default = {g: 10 for g in genres if g != "group"} # it's a secret :P

class PresetOverrides(OptionDict):
    """
    List of presets to use for a given genre. Replaces the default presets for
    that puzzle if specified.

    For example, to make Net puzzles always use wrapping grids, add:
    net: [5x5w, 7x7w, 9x9w, 11x11w]
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