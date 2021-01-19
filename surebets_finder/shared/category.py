from enum import Enum, unique
from typing import List


@unique
class Category(Enum):
    ESPORT = "esport"

    @staticmethod
    def values() -> List[str]:
        return [e.value for e in Category]
