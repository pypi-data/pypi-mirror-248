# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from .child import Child, AsyncChild, ChildWithRawResponse, AsyncChildWithRawResponse
from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import to_raw_response_wrapper, async_to_raw_response_wrapper
from ...._base_client import make_request_options
from ....types.resource_refs import ParentModelWithChildRef

if TYPE_CHECKING:
    from ...._client import Sink, AsyncSink

__all__ = ["Parent", "AsyncParent"]


class Parent(SyncAPIResource):
    child: Child
    with_raw_response: ParentWithRawResponse

    def __init__(self, client: Sink) -> None:
        super().__init__(client)
        self.child = Child(client)
        self.with_raw_response = ParentWithRawResponse(self)

    def returns_parent_model_with_child_ref(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ParentModelWithChildRef:
        """endpoint that returns a model that has a nested reference to a child model"""
        return self._get(
            "/resource_refs/parent_with_child_ref",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ParentModelWithChildRef,
        )


class AsyncParent(AsyncAPIResource):
    child: AsyncChild
    with_raw_response: AsyncParentWithRawResponse

    def __init__(self, client: AsyncSink) -> None:
        super().__init__(client)
        self.child = AsyncChild(client)
        self.with_raw_response = AsyncParentWithRawResponse(self)

    async def returns_parent_model_with_child_ref(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ParentModelWithChildRef:
        """endpoint that returns a model that has a nested reference to a child model"""
        return await self._get(
            "/resource_refs/parent_with_child_ref",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ParentModelWithChildRef,
        )


class ParentWithRawResponse:
    def __init__(self, parent: Parent) -> None:
        self.child = ChildWithRawResponse(parent.child)

        self.returns_parent_model_with_child_ref = to_raw_response_wrapper(
            parent.returns_parent_model_with_child_ref,
        )


class AsyncParentWithRawResponse:
    def __init__(self, parent: AsyncParent) -> None:
        self.child = AsyncChildWithRawResponse(parent.child)

        self.returns_parent_model_with_child_ref = async_to_raw_response_wrapper(
            parent.returns_parent_model_with_child_ref,
        )
