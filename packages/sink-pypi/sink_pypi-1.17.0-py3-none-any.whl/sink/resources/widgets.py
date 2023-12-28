# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from typing_extensions import Literal

import httpx

from ..types import Widget
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import to_raw_response_wrapper, async_to_raw_response_wrapper
from .._base_client import make_request_options

if TYPE_CHECKING:
    from .._client import Sink, AsyncSink

__all__ = ["Widgets", "AsyncWidgets"]


class Widgets(SyncAPIResource):
    with_raw_response: WidgetsWithRawResponse

    def __init__(self, client: Sink) -> None:
        super().__init__(client)
        self.with_raw_response = WidgetsWithRawResponse(self)

    def retrieve_with_filter(
        self,
        filter_type: Optional[Literal["available", "archived", "out_of_stock"]],
        *,
        widget_id: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Widget:
        """
        Endpoint that tests using an integer and enum in the pathParams

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            f"/widgets/{widget_id}/filter/{filter_type}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Widget,
        )


class AsyncWidgets(AsyncAPIResource):
    with_raw_response: AsyncWidgetsWithRawResponse

    def __init__(self, client: AsyncSink) -> None:
        super().__init__(client)
        self.with_raw_response = AsyncWidgetsWithRawResponse(self)

    async def retrieve_with_filter(
        self,
        filter_type: Optional[Literal["available", "archived", "out_of_stock"]],
        *,
        widget_id: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Widget:
        """
        Endpoint that tests using an integer and enum in the pathParams

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            f"/widgets/{widget_id}/filter/{filter_type}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Widget,
        )


class WidgetsWithRawResponse:
    def __init__(self, widgets: Widgets) -> None:
        self.retrieve_with_filter = to_raw_response_wrapper(
            widgets.retrieve_with_filter,
        )


class AsyncWidgetsWithRawResponse:
    def __init__(self, widgets: AsyncWidgets) -> None:
        self.retrieve_with_filter = async_to_raw_response_wrapper(
            widgets.retrieve_with_filter,
        )
