import logging
from math import ceil
from BaseClasses import Item, Region, Entrance, Tutorial, ItemClassification
from .items import SimonTathamPuzzlesItem, item_table, max_puzzles
from .locations import SimonTathamPuzzlesLocation, advancement_table
from .options import SimonTathamPuzzlesOptions, genrePresets, sgtpuzzles_option_groups
from .rules import set_rules, set_completion_rules
from worlds.AutoWorld import World, WebWorld

client_version = 1


class SimonTathamPuzzlesWeb(WebWorld):
    option_groups = sgtpuzzles_option_groups


class SimonTathamPuzzlesWorld(World):
    """
    Simon Tatham's Portable Puzzle Collection features implementations of
    various classic puzzle games. Solve a randomly generated collection of
    puzzles to unlock the boss puzzles and win.
    """
    game = "Simon Tatham's Portable Puzzle Collection"
    options: SimonTathamPuzzlesOptions
    options_dataclass = SimonTathamPuzzlesOptions
    web = SimonTathamPuzzlesWeb()
    puzzles: list[str]
    solve_target: int
    world_seed: int

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.id for name, data in advancement_table.items()}

    def generate_early(self):
        self.world_seed = self.multiworld.random.getrandbits(32)

        # Generate list of puzzles
        puzzle_count = self.options.puzzle_count.value
        self.puzzles = []
        genre_weights = self.options.genre_weights

        genres = self.multiworld.random.choices(list(genre_weights.keys()), (genre_weights.values()), k=puzzle_count)

        for i in range(puzzle_count):
            if genres[i] in self.options.preset_overrides:
                presets = self.options.preset_overrides[genres[i]]
            else:
                presets = genrePresets[genres[i]]

            preset = self.multiworld.random.choice(presets)

            new_puzzle = f"{genres[i]}:{preset}"
            self.puzzles.append(new_puzzle)

        self.solve_target = ceil(puzzle_count * (self.options.completion_percentage / 100))

    def create_regions(self):
        menu = Region("Menu", self.player, self.multiworld)
        region = Region("Puzzles", self.player, self.multiworld)

        for i in range(len(self.puzzles)):
            loc_name = f"Puzzle {i+1} Reward"
            loc_data = advancement_table[loc_name]
            new_location = SimonTathamPuzzlesLocation(self.player, loc_name, loc_data.id, region)
            region.locations.append(new_location)

        connection = Entrance(self.player, "Get Puzzles", menu)
        menu.exits.append(connection)
        connection.connect(region)
        self.multiworld.regions += [menu, region]

    def create_filler(self) -> Item:
        return self.create_item("Filler")

    def create_items(self):
        # Generate list of items
        itempool: list[str] = [f"Puzzle {i+1}" for i in range(len(self.puzzles))]

        # Remove existing starting items
        starting_items = self.multiworld.precollected_items[self.player]

        for item in starting_items:
            if item.name in itempool:
                itempool.remove(item.name)
            else:
                logging.warning(f"Couldn't remove {item.name} from puzzle itempool. It's probably useless.")

        # Choose more starting items and remove them
        starting_item_count = min(self.options.starting_puzzles.value, len(itempool))

        extra_starting_items = self.multiworld.random.sample(itempool, starting_item_count)

        for item in extra_starting_items:
            itempool.remove(item)
            self.multiworld.push_precollected(self.create_item(item))

        # Add remaining items and filler
        self.multiworld.itempool += [self.create_item(itemname) for itemname in itempool]

        filler_items = len(self.puzzles) - len(itempool)
        self.multiworld.itempool += [self.create_filler() for _ in range(filler_items)]

        print(itempool)
        print(self.multiworld.precollected_items[self.player])

    def set_rules(self):
        set_rules(self.multiworld, self.player, self.puzzles)
        set_completion_rules(self.multiworld, self.player, self.solve_target)

    def fill_slot_data(self):
        return {
            "world_seed": self.world_seed,
            "seed_name": self.multiworld.seed_name,
            "player_name": self.player_name,
            "player_id": self.player,
            "client_version": client_version,
            "race": self.multiworld.is_race,
            "puzzles": self.puzzles,
            "solve_target": self.solve_target
        }

    def create_item(self, name: str) -> SimonTathamPuzzlesItem:
        item_data = item_table[name]
        classification = ItemClassification.progression if item_data.progression else ItemClassification.filler
        return SimonTathamPuzzlesItem(name, classification, item_data.code, self.player)
