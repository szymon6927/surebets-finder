from typing import Protocol


class IWebClient(Protocol):
    def get_raw_data(self) -> str:
        ...
