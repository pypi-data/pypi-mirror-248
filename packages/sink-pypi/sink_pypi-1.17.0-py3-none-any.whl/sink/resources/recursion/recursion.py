# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import TYPE_CHECKING

from ..._resource import SyncAPIResource, AsyncAPIResource
from .shared_responses import (
    SharedResponses,
    AsyncSharedResponses,
    SharedResponsesWithRawResponse,
    AsyncSharedResponsesWithRawResponse,
)

if TYPE_CHECKING:
    from ..._client import Sink, AsyncSink

__all__ = ["Recursion", "AsyncRecursion"]


class Recursion(SyncAPIResource):
    shared_responses: SharedResponses
    with_raw_response: RecursionWithRawResponse

    def __init__(self, client: Sink) -> None:
        super().__init__(client)
        self.shared_responses = SharedResponses(client)
        self.with_raw_response = RecursionWithRawResponse(self)


class AsyncRecursion(AsyncAPIResource):
    shared_responses: AsyncSharedResponses
    with_raw_response: AsyncRecursionWithRawResponse

    def __init__(self, client: AsyncSink) -> None:
        super().__init__(client)
        self.shared_responses = AsyncSharedResponses(client)
        self.with_raw_response = AsyncRecursionWithRawResponse(self)


class RecursionWithRawResponse:
    def __init__(self, recursion: Recursion) -> None:
        self.shared_responses = SharedResponsesWithRawResponse(recursion.shared_responses)


class AsyncRecursionWithRawResponse:
    def __init__(self, recursion: AsyncRecursion) -> None:
        self.shared_responses = AsyncSharedResponsesWithRawResponse(recursion.shared_responses)
