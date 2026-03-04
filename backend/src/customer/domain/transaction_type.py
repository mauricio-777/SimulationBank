from enum import Enum

# parte-Mauricio
class TransactionType(str, Enum):
    """
    Enum: tipo de transacción bancaria
    DEPOSIT | WITHDRAWAL | PAYMENT | INQUIRY
    """
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    PAYMENT = "PAYMENT"
    INQUIRY = "INQUIRY"
