# congress_api/exceptions.py
from typing import Optional, Any


class CongressAPIError(Exception):
    """Base exception for Congress API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Any] = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class ValidationError(CongressAPIError):
    """Raised when input parameters fail validation."""
    pass


class AmendmentError(CongressAPIError):
    """Base class for amendment-related errors."""
    pass


class AmendmentTypeError(AmendmentError):
    """Raised when an invalid amendment type is provided."""
    def __init__(self, amendment_type: str, valid_types: set):
        message = (
            f"Invalid amendment type: {amendment_type}. "
            f"Must be one of: {', '.join(sorted(valid_types))}"
        )
        super().__init__(message)


class AmendmentTextError(AmendmentError):
    """Raised when trying to access text for unsupported congress/amendment type."""
    def __init__(self, congress: int, amendment_type: Optional[str] = None):
        if amendment_type:
            message = f"Amendment type '{amendment_type}' does not support text access"
        else:
            message = f"Text endpoint is only available for congress >= 117 (got {congress})"
        super().__init__(message)


class BillError(CongressAPIError):
    """Base class for bill-related errors."""
    pass


class BillTypeError(BillError):
    """Raised when an invalid bill type is provided."""
    def __init__(self, bill_type: str, valid_types: set):
        message = (
            f"Invalid bill type: {bill_type}. "
            f"Must be one of: {', '.join(sorted(valid_types))}"
        )
        super().__init__(message)


class BillNumberError(BillError):
    """Raised when an invalid bill number is provided."""
    def __init__(self, bill_number: Any):
        message = f"Invalid bill number: {bill_number}. Must be a positive integer."
        super().__init__(message)


class CongressNumberError(BillError):
    """Raised when an invalid congress number is provided."""
    def __init__(self, congress: Any):
        message = f"Invalid congress number: {congress}. Must be a positive integer."
        super().__init__(message)