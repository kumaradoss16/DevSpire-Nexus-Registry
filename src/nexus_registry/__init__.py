"""
DevSpire Nexus Registry Python SDK & Validator.
Official client and validation library for DevSpire Nexus Registry.
"""

__version__ = "1.0.0"

from .validator import RegistryValidator, ValidationReport, ValidationIssue, Severity
from .client import RegistryClient

__all__ = [
    "RegistryValidator",
    "ValidationReport",
    "ValidationIssue",
    "Severity",
    "RegistryClient",
    "__version__",
]
