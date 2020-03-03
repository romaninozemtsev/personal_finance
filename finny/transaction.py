from enum import Enum
from datetime import datetime


class TxType(Enum):
    DEBIT = 1
    CREDIT = 2

@dataclass
class Transaction:
    tx_type: TxType
    amount: float
    description: str
    tx_date: datetime

