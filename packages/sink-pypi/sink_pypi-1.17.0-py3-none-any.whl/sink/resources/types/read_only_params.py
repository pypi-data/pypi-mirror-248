# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import maybe_transform
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_raw_response_wrapper, async_to_raw_response_wrapper
from ...types.types import ReadOnlyParamSimpleResponse, read_only_param_simple_params
from ..._base_client import make_request_options

if TYPE_CHECKING:
    from ..._client import Sink, AsyncSink

__all__ = ["ReadOnlyParams", "AsyncReadOnlyParams"]


class ReadOnlyParams(SyncAPIResource):
    with_raw_response: ReadOnlyParamsWithRawResponse

    def __init__(self, client: Sink) -> None:
        super().__init__(client)
        self.with_raw_response = ReadOnlyParamsWithRawResponse(self)

    def simple(
        self,
        *,
        should_show_up: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> ReadOnlyParamSimpleResponse:
        """
        Endpoint with a request params schema object that contains a `readOnly`
        property.

        Args:
          should_show_up: This should be generated in the request params type.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/types/read_only_params/simple",
            body=maybe_transform(
                {"should_show_up": should_show_up}, read_only_param_simple_params.ReadOnlyParamSimpleParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ReadOnlyParamSimpleResponse,
        )


class AsyncReadOnlyParams(AsyncAPIResource):
    with_raw_response: AsyncReadOnlyParamsWithRawResponse

    def __init__(self, client: AsyncSink) -> None:
        super().__init__(client)
        self.with_raw_response = AsyncReadOnlyParamsWithRawResponse(self)

    async def simple(
        self,
        *,
        should_show_up: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> ReadOnlyParamSimpleResponse:
        """
        Endpoint with a request params schema object that contains a `readOnly`
        property.

        Args:
          should_show_up: This should be generated in the request params type.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/types/read_only_params/simple",
            body=maybe_transform(
                {"should_show_up": should_show_up}, read_only_param_simple_params.ReadOnlyParamSimpleParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ReadOnlyParamSimpleResponse,
        )


class ReadOnlyParamsWithRawResponse:
    def __init__(self, read_only_params: ReadOnlyParams) -> None:
        self.simple = to_raw_response_wrapper(
            read_only_params.simple,
        )


class AsyncReadOnlyParamsWithRawResponse:
    def __init__(self, read_only_params: AsyncReadOnlyParams) -> None:
        self.simple = async_to_raw_response_wrapper(
            read_only_params.simple,
        )
