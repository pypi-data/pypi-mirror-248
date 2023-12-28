# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import TYPE_CHECKING

from .payments import (
    Payments,
    AsyncPayments,
    PaymentsWithRawResponse,
    AsyncPaymentsWithRawResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource

if TYPE_CHECKING:
    from ..._client import Sink, AsyncSink

__all__ = ["CompanyResource", "AsyncCompanyResource"]


class CompanyResource(SyncAPIResource):
    payments: Payments
    with_raw_response: CompanyResourceWithRawResponse

    def __init__(self, client: Sink) -> None:
        super().__init__(client)
        self.payments = Payments(client)
        self.with_raw_response = CompanyResourceWithRawResponse(self)


class AsyncCompanyResource(AsyncAPIResource):
    payments: AsyncPayments
    with_raw_response: AsyncCompanyResourceWithRawResponse

    def __init__(self, client: AsyncSink) -> None:
        super().__init__(client)
        self.payments = AsyncPayments(client)
        self.with_raw_response = AsyncCompanyResourceWithRawResponse(self)


class CompanyResourceWithRawResponse:
    def __init__(self, company: CompanyResource) -> None:
        self.payments = PaymentsWithRawResponse(company.payments)


class AsyncCompanyResourceWithRawResponse:
    def __init__(self, company: AsyncCompanyResource) -> None:
        self.payments = AsyncPaymentsWithRawResponse(company.payments)
