# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from ...types import DecoratorTestKeepMeResponse
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .languages import (
    Languages,
    AsyncLanguages,
    LanguagesWithRawResponse,
    AsyncLanguagesWithRawResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_raw_response_wrapper, async_to_raw_response_wrapper
from ..._base_client import make_request_options
from .keep_this_resource import (
    KeepThisResource,
    AsyncKeepThisResource,
    KeepThisResourceWithRawResponse,
    AsyncKeepThisResourceWithRawResponse,
)

if TYPE_CHECKING:
    from ..._client import Sink, AsyncSink

__all__ = ["DecoratorTests", "AsyncDecoratorTests"]


class DecoratorTests(SyncAPIResource):
    languages: Languages
    keep_this_resource: KeepThisResource
    with_raw_response: DecoratorTestsWithRawResponse

    def __init__(self, client: Sink) -> None:
        super().__init__(client)
        self.languages = Languages(client)
        self.keep_this_resource = KeepThisResource(client)
        self.with_raw_response = DecoratorTestsWithRawResponse(self)

    def keep_me(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DecoratorTestKeepMeResponse:
        """Top-level method that should not be skipped."""
        return self._get(
            "/decorator_tests/keep/me",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DecoratorTestKeepMeResponse,
        )


class AsyncDecoratorTests(AsyncAPIResource):
    languages: AsyncLanguages
    keep_this_resource: AsyncKeepThisResource
    with_raw_response: AsyncDecoratorTestsWithRawResponse

    def __init__(self, client: AsyncSink) -> None:
        super().__init__(client)
        self.languages = AsyncLanguages(client)
        self.keep_this_resource = AsyncKeepThisResource(client)
        self.with_raw_response = AsyncDecoratorTestsWithRawResponse(self)

    async def keep_me(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DecoratorTestKeepMeResponse:
        """Top-level method that should not be skipped."""
        return await self._get(
            "/decorator_tests/keep/me",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DecoratorTestKeepMeResponse,
        )


class DecoratorTestsWithRawResponse:
    def __init__(self, decorator_tests: DecoratorTests) -> None:
        self.languages = LanguagesWithRawResponse(decorator_tests.languages)
        self.keep_this_resource = KeepThisResourceWithRawResponse(decorator_tests.keep_this_resource)

        self.keep_me = to_raw_response_wrapper(
            decorator_tests.keep_me,
        )


class AsyncDecoratorTestsWithRawResponse:
    def __init__(self, decorator_tests: AsyncDecoratorTests) -> None:
        self.languages = AsyncLanguagesWithRawResponse(decorator_tests.languages)
        self.keep_this_resource = AsyncKeepThisResourceWithRawResponse(decorator_tests.keep_this_resource)

        self.keep_me = async_to_raw_response_wrapper(
            decorator_tests.keep_me,
        )
