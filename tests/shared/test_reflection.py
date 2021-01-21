import pytest

from surebets_finder.shared.reflection import raises


def test_raises_decorator_with_valid_exception() -> None:
    @raises(ValueError)
    def raise_an_exception() -> None:
        raise ValueError()

    with pytest.raises(ValueError):
        raise_an_exception()


def test_raises_decorator_with_invalid_exception() -> None:
    @raises(ValueError)
    def raise_an_exception() -> None:
        raise RuntimeError()

    with pytest.raises(AssertionError):
        raise_an_exception()
