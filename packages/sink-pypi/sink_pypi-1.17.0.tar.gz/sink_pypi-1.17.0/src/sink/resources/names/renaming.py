# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_raw_response_wrapper, async_to_raw_response_wrapper
from ...types.names import RenamingExplicitResponsePropertyResponse
from ..._base_client import make_request_options

if TYPE_CHECKING:
    from ..._client import Sink, AsyncSink

__all__ = ["Renaming", "AsyncRenaming"]


class Renaming(SyncAPIResource):
    with_raw_response: RenamingWithRawResponse

    def __init__(self, client: Sink) -> None:
        super().__init__(client)
        self.with_raw_response = RenamingWithRawResponse(self)

    def explicit_response_property(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> RenamingExplicitResponsePropertyResponse:
        """Endpoint with a renamed response property in each language."""
        return self._get(
            "/names/renaming/explicit_response_property",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RenamingExplicitResponsePropertyResponse,
        )


class AsyncRenaming(AsyncAPIResource):
    with_raw_response: AsyncRenamingWithRawResponse

    def __init__(self, client: AsyncSink) -> None:
        super().__init__(client)
        self.with_raw_response = AsyncRenamingWithRawResponse(self)

    async def explicit_response_property(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> RenamingExplicitResponsePropertyResponse:
        """Endpoint with a renamed response property in each language."""
        return await self._get(
            "/names/renaming/explicit_response_property",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RenamingExplicitResponsePropertyResponse,
        )


class RenamingWithRawResponse:
    def __init__(self, renaming: Renaming) -> None:
        self.explicit_response_property = to_raw_response_wrapper(
            renaming.explicit_response_property,
        )


class AsyncRenamingWithRawResponse:
    def __init__(self, renaming: AsyncRenaming) -> None:
        self.explicit_response_property = async_to_raw_response_wrapper(
            renaming.explicit_response_property,
        )
