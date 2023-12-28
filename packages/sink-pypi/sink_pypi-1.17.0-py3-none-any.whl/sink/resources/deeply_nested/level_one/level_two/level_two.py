# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from .....types import Card
from ....._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .level_three import (
    LevelThree,
    AsyncLevelThree,
    LevelThreeWithRawResponse,
    AsyncLevelThreeWithRawResponse,
)
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import to_raw_response_wrapper, async_to_raw_response_wrapper
from ....._base_client import make_request_options

if TYPE_CHECKING:
    from ....._client import Sink, AsyncSink

__all__ = ["LevelTwo", "AsyncLevelTwo"]


class LevelTwo(SyncAPIResource):
    level_three: LevelThree
    with_raw_response: LevelTwoWithRawResponse

    def __init__(self, client: Sink) -> None:
        super().__init__(client)
        self.level_three = LevelThree(client)
        self.with_raw_response = LevelTwoWithRawResponse(self)

    def method_level_2(
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


class AsyncLevelTwo(AsyncAPIResource):
    level_three: AsyncLevelThree
    with_raw_response: AsyncLevelTwoWithRawResponse

    def __init__(self, client: AsyncSink) -> None:
        super().__init__(client)
        self.level_three = AsyncLevelThree(client)
        self.with_raw_response = AsyncLevelTwoWithRawResponse(self)

    async def method_level_2(
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


class LevelTwoWithRawResponse:
    def __init__(self, level_two: LevelTwo) -> None:
        self.level_three = LevelThreeWithRawResponse(level_two.level_three)

        self.method_level_2 = to_raw_response_wrapper(
            level_two.method_level_2,
        )


class AsyncLevelTwoWithRawResponse:
    def __init__(self, level_two: AsyncLevelTwo) -> None:
        self.level_three = AsyncLevelThreeWithRawResponse(level_two.level_three)

        self.method_level_2 = async_to_raw_response_wrapper(
            level_two.method_level_2,
        )
