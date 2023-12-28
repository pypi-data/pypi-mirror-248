# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import TYPE_CHECKING

from .child import Child, AsyncChild, ChildWithRawResponse, AsyncChildWithRawResponse
from ..._resource import SyncAPIResource, AsyncAPIResource

if TYPE_CHECKING:
    from ..._client import Sink, AsyncSink

__all__ = ["Parent", "AsyncParent"]


class Parent(SyncAPIResource):
    child: Child
    with_raw_response: ParentWithRawResponse

    def __init__(self, client: Sink) -> None:
        super().__init__(client)
        self.child = Child(client)
        self.with_raw_response = ParentWithRawResponse(self)


class AsyncParent(AsyncAPIResource):
    child: AsyncChild
    with_raw_response: AsyncParentWithRawResponse

    def __init__(self, client: AsyncSink) -> None:
        super().__init__(client)
        self.child = AsyncChild(client)
        self.with_raw_response = AsyncParentWithRawResponse(self)


class ParentWithRawResponse:
    def __init__(self, parent: Parent) -> None:
        self.child = ChildWithRawResponse(parent.child)


class AsyncParentWithRawResponse:
    def __init__(self, parent: AsyncParent) -> None:
        self.child = AsyncChildWithRawResponse(parent.child)
