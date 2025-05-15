from typing import Any, Dict, List, Optional, Union, Callable
from .base_validator import BaseValidator, ValidationResult, ValidationSeverity
from .metric_rules import MetricRules, ValidationType, MetricRule
import logging

logger = logging.getLogger(__name__)

class MetricValidator(BaseValidator):
    def __init__(self):
        super().__init__()
        self.metric_rules = MetricRules()
        
    def get_metric_rules(self, metric_name: str) -> Dict:
        """Get validation rules for a specific metric"""
        rule = self.metric_rules.get_rule_for_metric(metric_name)
        if not rule:
            return {}
        return {
            "validation_type": rule.validation_type.value,
            "min_value": rule.min_value,
            "max_value": rule.max_value,
            "description": rule.description
        }
    
    def get_dynamic_range(self, rule: MetricRule, value: Any) -> tuple:
        """Get dynamic range values from callable functions"""
        min_value = rule.min_value
        max_value = rule.max_value
        
        if callable(min_value):
            min_value, _ = min_value(value)
        if callable(max_value):
            _, max_value = max_value(value)
            
        return min_value, max_value
    
    def validate(self, value: Any, metric_name: str) -> ValidationResult:
        """Validate a single metric value against its rules"""
        # Get rule for this metric
        rule = self.metric_rules.get_rule_for_metric(metric_name)
        
        if not rule:
            logger.warning(f"No validation rule found for metric: {metric_name}")
            return ValidationResult(
                is_valid=True,
                message=f"No validation rule defined for {metric_name}",
                severity=ValidationSeverity.INFO,
                metric_name=metric_name,
                value=value,
                expected_range=None
            )
        
        # Handle None/null values
        if value is None:
            return ValidationResult(
                is_valid=False,
                message=f"Missing value for {metric_name}",
                severity=ValidationSeverity.WARNING,
                metric_name=metric_name,
                value=value,
                expected_range=None
            )
        
        # Get validation range from the rule
        min_value = rule.min_value
        max_value = rule.max_value
        
        # Handle callable range functions
        if callable(min_value):
            min_value, _ = min_value(value)
        if callable(max_value):
            _, max_value = max_value(value)
        
        # Perform validation based on validation type
        is_valid = True
        message = f"Validation passed for {metric_name}"
        
        # Using if/elif instead of match/case for Python 3.9 compatibility
        validation_type = rule.validation_type.value
        if validation_type == "non_negative":
            is_valid = value >= 0
            message = f"{metric_name} should be non-negative" if not is_valid else message
        elif validation_type == "non_zero":
            is_valid = value != 0
            message = f"{metric_name} should be non-zero" if not is_valid else message
        elif validation_type == "ratio":
            is_valid = (min_value is None or value >= min_value) and (max_value is None or value <= max_value)
            message = f"{metric_name} should be between {min_value} and {max_value}" if not is_valid else message
        elif validation_type == "probability":
            is_valid = 0 <= value <= 1
            message = f"{metric_name} should be between 0 and 1" if not is_valid else message
        elif validation_type == "weekday":
            is_valid = 0 <= value <= 6
            message = f"{metric_name} should be between 0 (Monday) and 6 (Sunday)" if not is_valid else message
        elif validation_type == "percentage":
            is_valid = 0 <= value <= 100
            message = f"{metric_name} should be between 0 and 100" if not is_valid else message
        elif validation_type == "cashflow":
            # Cashflow can be any value unless min/max specified
            is_valid = (min_value is None or value >= min_value) and (max_value is None or value <= max_value)
            message = f"{metric_name} should be within range {min_value} to {max_value}" if not is_valid else message
        else:
            # Default range check for other types
            is_valid = (min_value is None or value >= min_value) and (max_value is None or value <= max_value)
            message = f"{metric_name} should be within range {min_value} to {max_value}" if not is_valid else message
        
        # Use custom validation function if provided
        if rule.custom_validation:
            custom_valid, custom_message = rule.custom_validation(value)
            if not custom_valid:
                is_valid = False
                message = custom_message
        
        # Determine severity based on rule
        severity = ValidationSeverity.ERROR if not is_valid else ValidationSeverity.INFO
        if hasattr(rule, 'severity') and rule.severity:
            try:
                severity = ValidationSeverity[rule.severity.upper()]
            except (KeyError, AttributeError):
                severity = ValidationSeverity.ERROR
        
        return ValidationResult(
            is_valid=is_valid,
            message=message,
            severity=severity,
            metric_name=metric_name,
            value=value,
            expected_range=(min_value, max_value)
        )
    
    def validate_metric_group(self, group_name: str, values: Dict[str, Any]) -> Dict[str, ValidationResult]:
        """Validate all metrics for a specific group"""
        results = {}
        
        rules = self.metric_rules.get_rules_for_group(group_name)
        for rule in rules:
            if rule.metric_name in values:
                results[rule.metric_name] = self.validate(values[rule.metric_name], rule.metric_name)
        
        return results
    
    def validate_all_metrics(self, metrics: Dict[str, Any]) -> Dict[str, ValidationResult]:
        """Validate all metrics in the provided dictionary and include validation for missing metrics"""
        results = {}
        
        # Get all metrics that should be validated based on the rules
        all_expected_metrics = set()
        for group_rules in self.metric_rules.rules.values():
            for rule in group_rules:
                all_expected_metrics.add(rule.metric_name)
        
        # Validate provided metrics
        for metric_name, value in metrics.items():
            results[metric_name] = self.validate(value, metric_name)
        
        # Check for missing metrics and generate validation results for them
        missing_metrics = all_expected_metrics - set(metrics.keys())
        for metric_name in missing_metrics:
            rule = self.metric_rules.get_rule_for_metric(metric_name)
            severity = ValidationSeverity.WARNING
            if hasattr(rule, 'severity') and rule.severity:
                try:
                    severity = ValidationSeverity[rule.severity.upper()]
                except (KeyError, AttributeError):
                    severity = ValidationSeverity.WARNING
                    
            results[metric_name] = ValidationResult(
                is_valid=False,
                message=f"Missing metric: {metric_name}",
                severity=severity,
                metric_name=metric_name,
                value=None,
                expected_range=None
            )
        
        return results
    
    def get_missing_metrics(self, metrics: Dict[str, Any]) -> List[str]:
        """Return a list of metrics that are expected but missing from the input"""
        all_expected_metrics = set()
        for group_rules in self.metric_rules.rules.values():
            for rule in group_rules:
                all_expected_metrics.add(rule.metric_name)
        
        return list(all_expected_metrics - set(metrics.keys())) 