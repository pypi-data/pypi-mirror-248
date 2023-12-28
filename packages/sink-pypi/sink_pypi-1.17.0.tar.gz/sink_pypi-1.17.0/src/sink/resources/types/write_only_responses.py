# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_raw_response_wrapper, async_to_raw_response_wrapper
from ...types.types import WriteOnlyResponseSimpleResponse
from ..._base_client import make_request_options

if TYPE_CHECKING:
    from ..._client import Sink, AsyncSink

__all__ = ["WriteOnlyResponses", "AsyncWriteOnlyResponses"]


class WriteOnlyResponses(SyncAPIResource):
    with_raw_response: WriteOnlyResponsesWithRawResponse

    def __init__(self, client: Sink) -> None:
        super().__init__(client)
        self.with_raw_response = WriteOnlyResponsesWithRawResponse(self)

    def simple(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WriteOnlyResponseSimpleResponse:
        """Endpoint with a response schema object that contains a `writeOnly` property."""
        return self._get(
            "/types/write_only_responses/simple",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WriteOnlyResponseSimpleResponse,
        )


class AsyncWriteOnlyResponses(AsyncAPIResource):
    with_raw_response: AsyncWriteOnlyResponsesWithRawResponse

    def __init__(self, client: AsyncSink) -> None:
        super().__init__(client)
        self.with_raw_response = AsyncWriteOnlyResponsesWithRawResponse(self)

    async def simple(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WriteOnlyResponseSimpleResponse:
        """Endpoint with a response schema object that contains a `writeOnly` property."""
        return await self._get(
            "/types/write_only_responses/simple",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WriteOnlyResponseSimpleResponse,
        )


class WriteOnlyResponsesWithRawResponse:
    def __init__(self, write_only_responses: WriteOnlyResponses) -> None:
        self.simple = to_raw_response_wrapper(
            write_only_responses.simple,
        )


class AsyncWriteOnlyResponsesWithRawResponse:
    def __init__(self, write_only_responses: AsyncWriteOnlyResponses) -> None:
        self.simple = async_to_raw_response_wrapper(
            write_only_responses.simple,
        )
