from bson.objectid import ObjectId

from surebets_finder.raw_content.domain.entities import RawContent
from surebets_finder.shared.category import Category
from surebets_finder.shared.provider import Provider


def test_can_instantiate() -> None:
    # given
    raw_content = RawContent(
        id=ObjectId(), content="some content", category=Category.ESPORT, provider=Provider.EFORTUNA, was_processed=False
    )

    # then
    assert isinstance(raw_content, RawContent)
