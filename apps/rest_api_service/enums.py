""" Enums for the REST API service. """

from enum import Enum

class StatusPayment(Enum):
    """Enum for payment status."""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class OperationType(Enum):
    """Enum for wallet operation types."""
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"

class WalletType(Enum):
    """Enum for wallet types."""
    ETH= "eth"

class OrderStatus(Enum):
    """Enum for order status."""
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"