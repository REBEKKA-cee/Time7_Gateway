from enum import Enum


class AuthResult(str, Enum):
    """Unified wrapper for Impinj authentication results."""

    AUTHENTIC = "authentic"        # Genuine
    TAMPERED = "tampered"          # Tampered
    UNKNOWN = "unknown"            # Unknown / Not found
    EXPIRED = "expired"            # Expired
    MISMATCH = "mismatch"          # Data mismatch
    ERROR = "error"                # Call error
