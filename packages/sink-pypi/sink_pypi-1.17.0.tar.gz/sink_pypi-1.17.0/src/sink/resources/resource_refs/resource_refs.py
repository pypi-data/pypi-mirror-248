# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import TYPE_CHECKING

from .parent import (
    Parent,
    AsyncParent,
    ParentWithRawResponse,
    AsyncParentWithRawResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource

if TYPE_CHECKING:
    from ..._client import Sink, AsyncSink

__all__ = ["ResourceRefs", "AsyncResourceRefs"]


class ResourceRefs(SyncAPIResource):
    parent: Parent
    with_raw_response: ResourceRefsWithRawResponse

    def __init__(self, client: Sink) -> None:
        super().__init__(client)
        self.parent = Parent(client)
        self.with_raw_response = ResourceRefsWithRawResponse(self)


class AsyncResourceRefs(AsyncAPIResource):
    parent: AsyncParent
    with_raw_response: AsyncResourceRefsWithRawResponse

    def __init__(self, client: AsyncSink) -> None:
        super().__init__(client)
        self.parent = AsyncParent(client)
        self.with_raw_response = AsyncResourceRefsWithRawResponse(self)


class ResourceRefsWithRawResponse:
    def __init__(self, resource_refs: ResourceRefs) -> None:
        self.parent = ParentWithRawResponse(resource_refs.parent)


class AsyncResourceRefsWithRawResponse:
    def __init__(self, resource_refs: AsyncResourceRefs) -> None:
        self.parent = AsyncParentWithRawResponse(resource_refs.parent)
