# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_raw_response_wrapper, async_to_raw_response_wrapper
from ...types.names import documents
from ..._base_client import make_request_options

if TYPE_CHECKING:
    from ..._client import Sink, AsyncSink

__all__ = ["Documents", "AsyncDocuments"]


class Documents(SyncAPIResource):
    with_raw_response: DocumentsWithRawResponse

    def __init__(self, client: Sink) -> None:
        super().__init__(client)
        self.with_raw_response = DocumentsWithRawResponse(self)

    def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> documents.Documents:
        """
        Endpoint with a response model that can clash with the resource class in Python.
        """
        return self._post(
            "/names/model_import_clash_with_resource",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=documents.Documents,
        )


class AsyncDocuments(AsyncAPIResource):
    with_raw_response: AsyncDocumentsWithRawResponse

    def __init__(self, client: AsyncSink) -> None:
        super().__init__(client)
        self.with_raw_response = AsyncDocumentsWithRawResponse(self)

    async def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> documents.Documents:
        """
        Endpoint with a response model that can clash with the resource class in Python.
        """
        return await self._post(
            "/names/model_import_clash_with_resource",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=documents.Documents,
        )


class DocumentsWithRawResponse:
    def __init__(self, documents: Documents) -> None:
        self.retrieve = to_raw_response_wrapper(
            documents.retrieve,
        )


class AsyncDocumentsWithRawResponse:
    def __init__(self, documents: AsyncDocuments) -> None:
        self.retrieve = async_to_raw_response_wrapper(
            documents.retrieve,
        )
