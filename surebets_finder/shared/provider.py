from enum import Enum, unique


@unique
class Provider(Enum):
    EFORTUNA = "efortuna"
    LVBET = "lvbet"
    BETCLICK = "betclick"
