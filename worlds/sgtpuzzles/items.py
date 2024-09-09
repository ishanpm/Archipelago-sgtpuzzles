from BaseClasses import Item
import typing

base_id = 925000
max_puzzles = 200

class ItemData(typing.NamedTuple):
    code: int
    progression: bool = True


class SimonTathamPuzzlesItem(Item):
    game: str = "SimonTathamPuzzles"


# item_table = {
#     "Loopy": ItemData(base_id + 0),
#     "Net": ItemData(base_id + 1),
#     "Fifteen": ItemData(base_id + 2),
#     "Boss Key": ItemData(base_id + 3)
# }

item_table = {f"Puzzle {i+1}": ItemData(base_id+i) for i in range(max_puzzles)}
item_table["Filler"] = ItemData(max_puzzles, False)

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items()}
