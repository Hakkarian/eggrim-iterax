ICON_LETTERS = {"K": "0", "R": "8", "Y": "a", "B": "c", ".": "e"}
ICON_COLKEY = 14

ICON_ROWS = (
    "................................",
    ".......KKK............KK........",
    "......KKKKK....BB....KKKK.......",
    ".......KKKKK..BBB...KKKKK.......",
    "........KKKKK..BB..KKKKK........",
    ".........KKKKK...KKKKKK.........",
    "..........KKKKK.KKKKKK..........",
    "...........KKKKKKKKKK...........",
    "........RRR.KKKKKKKK.YYY........",
    "........RRR..KKKKKK..YYY........",
    "............KKKKKKKK..Y.........",
    "...........KKKKKKKKKK...........",
    ".........KKKKKKKKKKKKK..........",
    "........KKKKKKKKKKKKKKK.........",
    ".......KKKKKK.KKKK.KKKKK........",
    ".......KKKKK..KKKK..KKKKK.......",
    ".......KKKK...KKKK...KKKK.......",
    "........K....KKKKK....KK........",
    "..........KKKKKKKKKK............",
    ".........KKKKKKKKKKKKK..........",
    "........KKKKKKKKKKKKKKK.........",
    ".......KKKK...KKKK..KKKK........",
    "......KKKK....KKKK...KKK........",
    "......KKK.....KKKK...KKKK.......",
    "......KKK.....KKKK...KKKK.......",
    "......KKK.....KKKK....KKK.......",
    "......KKK.....KKKK...KKKK.......",
    "......KKKK....KKK....KKK........",
    ".......KKK.....KK...KKKK........",
    ".......KKKK........KKKK.........",
    "........KKK.........KKK.........",
    ".........K...........K..........",
)

ICON_CHARS = tuple("".join(ICON_LETTERS[ch] for ch in row) for row in ICON_ROWS)