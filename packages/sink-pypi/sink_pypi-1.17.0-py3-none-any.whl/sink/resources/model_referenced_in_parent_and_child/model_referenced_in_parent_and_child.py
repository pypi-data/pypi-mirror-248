# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from .child import Child, AsyncChild, ChildWithRawResponse, AsyncChildWithRawResponse
from ...types import ModelReferencedInParentAndChild
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_raw_response_wrapper, async_to_raw_response_wrapper
from ..._base_client import make_request_options

if TYPE_CHECKING:
    from ..._client import Sink, AsyncSink

__all__ = ["ModelReferencedInParentAndChildResource", "AsyncModelReferencedInParentAndChildResource"]


class ModelReferencedInParentAndChildResource(SyncAPIResource):
    child: Child
    with_raw_response: ModelReferencedInParentAndChildResourceWithRawResponse

    def __init__(self, client: Sink) -> None:
        super().__init__(client)
        self.child = Child(client)
        self.with_raw_response = ModelReferencedInParentAndChildResourceWithRawResponse(self)

    def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ModelReferencedInParentAndChild:
        return self._get(
            "/model_referenced_in_parent_and_child",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelReferencedInParentAndChild,
        )


class AsyncModelReferencedInParentAndChildResource(AsyncAPIResource):
    child: AsyncChild
    with_raw_response: AsyncModelReferencedInParentAndChildResourceWithRawResponse

    def __init__(self, client: AsyncSink) -> None:
        super().__init__(client)
        self.child = AsyncChild(client)
        self.with_raw_response = AsyncModelReferencedInParentAndChildResourceWithRawResponse(self)

    async def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ModelReferencedInParentAndChild:
        return await self._get(
            "/model_referenced_in_parent_and_child",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelReferencedInParentAndChild,
        )


class ModelReferencedInParentAndChildResourceWithRawResponse:
    def __init__(self, model_referenced_in_parent_and_child: ModelReferencedInParentAndChildResource) -> None:
        self.child = ChildWithRawResponse(model_referenced_in_parent_and_child.child)

        self.retrieve = to_raw_response_wrapper(
            model_referenced_in_parent_and_child.retrieve,
        )


class AsyncModelReferencedInParentAndChildResourceWithRawResponse:
    def __init__(self, model_referenced_in_parent_and_child: AsyncModelReferencedInParentAndChildResource) -> None:
        self.child = AsyncChildWithRawResponse(model_referenced_in_parent_and_child.child)

        self.retrieve = async_to_raw_response_wrapper(
            model_referenced_in_parent_and_child.retrieve,
        )
