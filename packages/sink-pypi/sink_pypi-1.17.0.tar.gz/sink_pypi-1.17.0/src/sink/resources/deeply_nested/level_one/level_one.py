# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from ....types import Card
from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .level_two import (
    LevelTwo,
    AsyncLevelTwo,
    LevelTwoWithRawResponse,
    AsyncLevelTwoWithRawResponse,
)
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import to_raw_response_wrapper, async_to_raw_response_wrapper
from ...._base_client import make_request_options

if TYPE_CHECKING:
    from ...._client import Sink, AsyncSink

__all__ = ["LevelOne", "AsyncLevelOne"]


class LevelOne(SyncAPIResource):
    level_two: LevelTwo
    with_raw_response: LevelOneWithRawResponse

    def __init__(self, client: Sink) -> None:
        super().__init__(client)
        self.level_two = LevelTwo(client)
        self.with_raw_response = LevelOneWithRawResponse(self)

    def method_level_1(
        self,
        card_token: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Card:
        """
        Get card configuration such as spend limit and state.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            f"/cards/{card_token}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Card,
        )


class AsyncLevelOne(AsyncAPIResource):
    level_two: AsyncLevelTwo
    with_raw_response: AsyncLevelOneWithRawResponse

    def __init__(self, client: AsyncSink) -> None:
        super().__init__(client)
        self.level_two = AsyncLevelTwo(client)
        self.with_raw_response = AsyncLevelOneWithRawResponse(self)

    async def method_level_1(
        self,
        card_token: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Card:
        """
        Get card configuration such as spend limit and state.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            f"/cards/{card_token}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Card,
        )


class LevelOneWithRawResponse:
    def __init__(self, level_one: LevelOne) -> None:
        self.level_two = LevelTwoWithRawResponse(level_one.level_two)

        self.method_level_1 = to_raw_response_wrapper(
            level_one.method_level_1,
        )


class AsyncLevelOneWithRawResponse:
    def __init__(self, level_one: AsyncLevelOne) -> None:
        self.level_two = AsyncLevelTwoWithRawResponse(level_one.level_two)

        self.method_level_1 = async_to_raw_response_wrapper(
            level_one.method_level_1,
        )
