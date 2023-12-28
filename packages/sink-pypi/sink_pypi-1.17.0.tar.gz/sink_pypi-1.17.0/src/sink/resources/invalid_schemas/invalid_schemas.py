# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import TYPE_CHECKING

from .arrays import (
    Arrays,
    AsyncArrays,
    ArraysWithRawResponse,
    AsyncArraysWithRawResponse,
)
from .objects import (
    Objects,
    AsyncObjects,
    ObjectsWithRawResponse,
    AsyncObjectsWithRawResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource

if TYPE_CHECKING:
    from ..._client import Sink, AsyncSink

__all__ = ["InvalidSchemas", "AsyncInvalidSchemas"]


class InvalidSchemas(SyncAPIResource):
    arrays: Arrays
    objects: Objects
    with_raw_response: InvalidSchemasWithRawResponse

    def __init__(self, client: Sink) -> None:
        super().__init__(client)
        self.arrays = Arrays(client)
        self.objects = Objects(client)
        self.with_raw_response = InvalidSchemasWithRawResponse(self)


class AsyncInvalidSchemas(AsyncAPIResource):
    arrays: AsyncArrays
    objects: AsyncObjects
    with_raw_response: AsyncInvalidSchemasWithRawResponse

    def __init__(self, client: AsyncSink) -> None:
        super().__init__(client)
        self.arrays = AsyncArrays(client)
        self.objects = AsyncObjects(client)
        self.with_raw_response = AsyncInvalidSchemasWithRawResponse(self)


class InvalidSchemasWithRawResponse:
    def __init__(self, invalid_schemas: InvalidSchemas) -> None:
        self.arrays = ArraysWithRawResponse(invalid_schemas.arrays)
        self.objects = ObjectsWithRawResponse(invalid_schemas.objects)


class AsyncInvalidSchemasWithRawResponse:
    def __init__(self, invalid_schemas: AsyncInvalidSchemas) -> None:
        self.arrays = AsyncArraysWithRawResponse(invalid_schemas.arrays)
        self.objects = AsyncObjectsWithRawResponse(invalid_schemas.objects)
