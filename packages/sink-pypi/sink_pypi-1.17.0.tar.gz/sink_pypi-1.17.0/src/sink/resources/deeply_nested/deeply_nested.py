# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import TYPE_CHECKING

from .level_one import (
    LevelOne,
    AsyncLevelOne,
    LevelOneWithRawResponse,
    AsyncLevelOneWithRawResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource

if TYPE_CHECKING:
    from ..._client import Sink, AsyncSink

__all__ = ["DeeplyNested", "AsyncDeeplyNested"]


class DeeplyNested(SyncAPIResource):
    level_one: LevelOne
    with_raw_response: DeeplyNestedWithRawResponse

    def __init__(self, client: Sink) -> None:
        super().__init__(client)
        self.level_one = LevelOne(client)
        self.with_raw_response = DeeplyNestedWithRawResponse(self)


class AsyncDeeplyNested(AsyncAPIResource):
    level_one: AsyncLevelOne
    with_raw_response: AsyncDeeplyNestedWithRawResponse

    def __init__(self, client: AsyncSink) -> None:
        super().__init__(client)
        self.level_one = AsyncLevelOne(client)
        self.with_raw_response = AsyncDeeplyNestedWithRawResponse(self)


class DeeplyNestedWithRawResponse:
    def __init__(self, deeply_nested: DeeplyNested) -> None:
        self.level_one = LevelOneWithRawResponse(deeply_nested.level_one)


class AsyncDeeplyNestedWithRawResponse:
    def __init__(self, deeply_nested: AsyncDeeplyNested) -> None:
        self.level_one = AsyncLevelOneWithRawResponse(deeply_nested.level_one)
