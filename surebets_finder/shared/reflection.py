from typing import Any, Callable, Dict, List, Type, TypeVar, cast

T = TypeVar("T", bound=Callable[..., Any])


def raises(*allowed_exceptions: Type[Exception]) -> Callable[[T], T]:
    """
    Use this decorator to document exceptions types that might be raised by given method/function.
    """

    def decorator(obj: T) -> T:
        def _callable(*args: List[Any], **kwargs: Dict[str, Any]) -> Any:
            try:
                return obj(*args, **kwargs)
            except Exception as error:
                if not isinstance(error, allowed_exceptions):
                    raise AssertionError(
                        f"{obj} raised {error.__class__} exception which is not within allowed list {allowed_exceptions}"
                    )

                raise error

        return cast(T, _callable)

    return cast(Callable[[T], T], decorator)
