# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import TYPE_CHECKING

from .eeoc import (
    EEOCResource,
    AsyncEEOCResource,
    EEOCResourceWithRawResponse,
    AsyncEEOCResourceWithRawResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource

if TYPE_CHECKING:
    from ..._client import Sink, AsyncSink

__all__ = ["Casing", "AsyncCasing"]


class Casing(SyncAPIResource):
    eeoc: EEOCResource
    with_raw_response: CasingWithRawResponse

    def __init__(self, client: Sink) -> None:
        super().__init__(client)
        self.eeoc = EEOCResource(client)
        self.with_raw_response = CasingWithRawResponse(self)


class AsyncCasing(AsyncAPIResource):
    eeoc: AsyncEEOCResource
    with_raw_response: AsyncCasingWithRawResponse

    def __init__(self, client: AsyncSink) -> None:
        super().__init__(client)
        self.eeoc = AsyncEEOCResource(client)
        self.with_raw_response = AsyncCasingWithRawResponse(self)


class CasingWithRawResponse:
    def __init__(self, casing: Casing) -> None:
        self.eeoc = EEOCResourceWithRawResponse(casing.eeoc)


class AsyncCasingWithRawResponse:
    def __init__(self, casing: AsyncCasing) -> None:
        self.eeoc = AsyncEEOCResourceWithRawResponse(casing.eeoc)
