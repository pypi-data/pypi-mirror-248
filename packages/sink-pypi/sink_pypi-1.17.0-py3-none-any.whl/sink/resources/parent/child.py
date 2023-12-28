# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_raw_response_wrapper, async_to_raw_response_wrapper
from ..._base_client import make_request_options
from ...types.parent import ChildInlinedResponseResponse

if TYPE_CHECKING:
    from ..._client import Sink, AsyncSink

__all__ = ["Child", "AsyncChild"]


class Child(SyncAPIResource):
    with_raw_response: ChildWithRawResponse

    def __init__(self, client: Sink) -> None:
        super().__init__(client)
        self.with_raw_response = ChildWithRawResponse(self)

    def inlined_response(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChildInlinedResponseResponse:
        """Method with inlined response model."""
        return self._get(
            "/inlined_response",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChildInlinedResponseResponse,
        )


class AsyncChild(AsyncAPIResource):
    with_raw_response: AsyncChildWithRawResponse

    def __init__(self, client: AsyncSink) -> None:
        super().__init__(client)
        self.with_raw_response = AsyncChildWithRawResponse(self)

    async def inlined_response(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChildInlinedResponseResponse:
        """Method with inlined response model."""
        return await self._get(
            "/inlined_response",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChildInlinedResponseResponse,
        )


class ChildWithRawResponse:
    def __init__(self, child: Child) -> None:
        self.inlined_response = to_raw_response_wrapper(
            child.inlined_response,
        )


class AsyncChildWithRawResponse:
    def __init__(self, child: AsyncChild) -> None:
        self.inlined_response = async_to_raw_response_wrapper(
            child.inlined_response,
        )
