from dataclasses import dataclass
from datetime import datetime

from bson.objectid import ObjectId

from surebets_finder.shared.category import Category
from surebets_finder.shared.provider import Provider


@dataclass
class RawContent:
    id: ObjectId
    content: str
    category: Category
    provider: Provider
    was_processed: bool = False
    created_at: datetime = datetime.utcnow()
