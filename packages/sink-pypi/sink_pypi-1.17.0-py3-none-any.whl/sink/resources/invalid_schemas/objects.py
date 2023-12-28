# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_raw_response_wrapper, async_to_raw_response_wrapper
from ..._base_client import make_request_options
from ...types.invalid_schemas import ObjectMissingItemsResponse

if TYPE_CHECKING:
    from ..._client import Sink, AsyncSink

__all__ = ["Objects", "AsyncObjects"]


class Objects(SyncAPIResource):
    with_raw_response: ObjectsWithRawResponse

    def __init__(self, client: Sink) -> None:
        super().__init__(client)
        self.with_raw_response = ObjectsWithRawResponse(self)

    def missing_items(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectMissingItemsResponse:
        return self._get(
            "/invalid_schemas/objects/property_missing_def",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectMissingItemsResponse,
        )


class AsyncObjects(AsyncAPIResource):
    with_raw_response: AsyncObjectsWithRawResponse

    def __init__(self, client: AsyncSink) -> None:
        super().__init__(client)
        self.with_raw_response = AsyncObjectsWithRawResponse(self)

    async def missing_items(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectMissingItemsResponse:
        return await self._get(
            "/invalid_schemas/objects/property_missing_def",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectMissingItemsResponse,
        )


class ObjectsWithRawResponse:
    def __init__(self, objects: Objects) -> None:
        self.missing_items = to_raw_response_wrapper(
            objects.missing_items,
        )


class AsyncObjectsWithRawResponse:
    def __init__(self, objects: AsyncObjects) -> None:
        self.missing_items = async_to_raw_response_wrapper(
            objects.missing_items,
        )
