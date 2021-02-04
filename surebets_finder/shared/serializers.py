from decimal import ROUND_HALF_UP, Decimal
from enum import Enum
from typing import Any, Dict

from bson import Decimal128


def dataclass_serializer(data: Any) -> Dict[Any, Any]:
    serialized = dict()

    for field, value in data:
        if isinstance(value, Enum):
            serialized[field] = value.value
        elif isinstance(value, Decimal):
            quantize_value = Decimal(value.quantize(Decimal(".01"), rounding=ROUND_HALF_UP))
            serialized[field] = Decimal128(str(quantize_value))
        else:
            serialized[field] = value

    return serialized
