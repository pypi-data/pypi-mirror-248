from typing import Optional

from pydantic.dataclasses import dataclass
from decimal import Decimal

from capsphere.data.model.data_record import DataRecord


@dataclass
class LedgerEntry(DataRecord):
    user_id: int = 0
    ledgerable_id: int = 0
    ledgerable_type: str = ''
    ref_code: str = ''
    reason: str = ''
    credit: int = 0
    debit: int = 0
    amount: Decimal = Decimal(0.00)
    balance: Decimal = Decimal(0.00)
    id: Optional[int] = None
    loan_payment_id: Optional[int] = None
    due_date: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @staticmethod
    def from_dict(data: dict):
        return LedgerEntry(**data)
