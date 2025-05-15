from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum
import logging

class ValidationSeverity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

@dataclass
class ValidationResult:
    is_valid: bool
    message: str
    severity: ValidationSeverity
    metric_name: str
    value: Any
    expected_range: Optional[tuple] = None
    details: Optional[Dict] = None

class BaseValidator(ABC):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        
    @abstractmethod
    def validate(self, value: Any, metric_name: str) -> ValidationResult:
        """Validate a single value for a metric"""
        pass
    
    @abstractmethod
    def get_metric_rules(self, metric_name: str) -> Dict:
        """Get validation rules for a specific metric"""
        pass
    
    def validate_batch(self, values: List[Any], metric_name: str) -> List[ValidationResult]:
        """Validate a batch of values for a metric"""
        return [self.validate(value, metric_name) for value in values]
    
    def format_validation_result(self, 
                               is_valid: bool, 
                               message: str, 
                               severity: ValidationSeverity,
                               metric_name: str,
                               value: Any,
                               expected_range: Optional[tuple] = None,
                               details: Optional[Dict] = None) -> ValidationResult:
        """Format a validation result with consistent structure"""
        return ValidationResult(
            is_valid=is_valid,
            message=message,
            severity=severity,
            metric_name=metric_name,
            value=value,
            expected_range=expected_range,
            details=details
        ) 