# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import TYPE_CHECKING

from .refs import Refs, AsyncRefs, RefsWithRawResponse, AsyncRefsWithRawResponse
from .cursor import (
    Cursor,
    AsyncCursor,
    CursorWithRawResponse,
    AsyncCursorWithRawResponse,
)
from .offset import (
    Offset,
    AsyncOffset,
    OffsetWithRawResponse,
    AsyncOffsetWithRawResponse,
)
from .cursor_id import (
    CursorID,
    AsyncCursorID,
    CursorIDWithRawResponse,
    AsyncCursorIDWithRawResponse,
)
from .fake_pages import (
    FakePages,
    AsyncFakePages,
    FakePagesWithRawResponse,
    AsyncFakePagesWithRawResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from .page_number import (
    PageNumber,
    AsyncPageNumber,
    PageNumberWithRawResponse,
    AsyncPageNumberWithRawResponse,
)
from .response_headers import (
    ResponseHeaders,
    AsyncResponseHeaders,
    ResponseHeadersWithRawResponse,
    AsyncResponseHeadersWithRawResponse,
)
from .top_level_arrays import (
    TopLevelArrays,
    AsyncTopLevelArrays,
    TopLevelArraysWithRawResponse,
    AsyncTopLevelArraysWithRawResponse,
)

if TYPE_CHECKING:
    from ..._client import Sink, AsyncSink

__all__ = ["PaginationTests", "AsyncPaginationTests"]


class PaginationTests(SyncAPIResource):
    page_number: PageNumber
    refs: Refs
    response_headers: ResponseHeaders
    top_level_arrays: TopLevelArrays
    cursor: Cursor
    cursor_id: CursorID
    offset: Offset
    fake_pages: FakePages
    with_raw_response: PaginationTestsWithRawResponse

    def __init__(self, client: Sink) -> None:
        super().__init__(client)
        self.page_number = PageNumber(client)
        self.refs = Refs(client)
        self.response_headers = ResponseHeaders(client)
        self.top_level_arrays = TopLevelArrays(client)
        self.cursor = Cursor(client)
        self.cursor_id = CursorID(client)
        self.offset = Offset(client)
        self.fake_pages = FakePages(client)
        self.with_raw_response = PaginationTestsWithRawResponse(self)


class AsyncPaginationTests(AsyncAPIResource):
    page_number: AsyncPageNumber
    refs: AsyncRefs
    response_headers: AsyncResponseHeaders
    top_level_arrays: AsyncTopLevelArrays
    cursor: AsyncCursor
    cursor_id: AsyncCursorID
    offset: AsyncOffset
    fake_pages: AsyncFakePages
    with_raw_response: AsyncPaginationTestsWithRawResponse

    def __init__(self, client: AsyncSink) -> None:
        super().__init__(client)
        self.page_number = AsyncPageNumber(client)
        self.refs = AsyncRefs(client)
        self.response_headers = AsyncResponseHeaders(client)
        self.top_level_arrays = AsyncTopLevelArrays(client)
        self.cursor = AsyncCursor(client)
        self.cursor_id = AsyncCursorID(client)
        self.offset = AsyncOffset(client)
        self.fake_pages = AsyncFakePages(client)
        self.with_raw_response = AsyncPaginationTestsWithRawResponse(self)


class PaginationTestsWithRawResponse:
    def __init__(self, pagination_tests: PaginationTests) -> None:
        self.page_number = PageNumberWithRawResponse(pagination_tests.page_number)
        self.refs = RefsWithRawResponse(pagination_tests.refs)
        self.response_headers = ResponseHeadersWithRawResponse(pagination_tests.response_headers)
        self.top_level_arrays = TopLevelArraysWithRawResponse(pagination_tests.top_level_arrays)
        self.cursor = CursorWithRawResponse(pagination_tests.cursor)
        self.cursor_id = CursorIDWithRawResponse(pagination_tests.cursor_id)
        self.offset = OffsetWithRawResponse(pagination_tests.offset)
        self.fake_pages = FakePagesWithRawResponse(pagination_tests.fake_pages)


class AsyncPaginationTestsWithRawResponse:
    def __init__(self, pagination_tests: AsyncPaginationTests) -> None:
        self.page_number = AsyncPageNumberWithRawResponse(pagination_tests.page_number)
        self.refs = AsyncRefsWithRawResponse(pagination_tests.refs)
        self.response_headers = AsyncResponseHeadersWithRawResponse(pagination_tests.response_headers)
        self.top_level_arrays = AsyncTopLevelArraysWithRawResponse(pagination_tests.top_level_arrays)
        self.cursor = AsyncCursorWithRawResponse(pagination_tests.cursor)
        self.cursor_id = AsyncCursorIDWithRawResponse(pagination_tests.cursor_id)
        self.offset = AsyncOffsetWithRawResponse(pagination_tests.offset)
        self.fake_pages = AsyncFakePagesWithRawResponse(pagination_tests.fake_pages)
