from typing import Dict, List, Optional, Union, Callable
from dataclasses import dataclass
from enum import Enum

class ValidationType(Enum):
    NON_NEGATIVE = "non_negative"
    NON_ZERO = "non_zero"
    RANGE = "range"
    RATIO = "ratio"
    COUNT = "count"
    AMOUNT = "amount"
    DAYS = "days"
    PROBABILITY = "probability"
    WEEKDAY = "weekday"
    PERCENTAGE = "percentage"
    ARRAY = "array"
    CASHFLOW = "cashflow"

@dataclass
class MetricRule:
    metric_name: str
    validation_type: ValidationType
    min_value: Optional[Union[float, Callable]] = None
    max_value: Optional[Union[float, Callable]] = None
    description: str = ""
    severity: str = "error"
    dependencies: List[str] = None
    custom_validation: Optional[Callable] = None

class MetricRules:
    def __init__(self):
        # Define dynamic range functions
        def get_growth_rate_range(value: float) -> tuple:
            """Growth rate can be negative but not less than -100%"""
            return (-1, None)
        
        def get_ratio_range(value: float) -> tuple:
            """Ratios should be between 0 and 1"""
            return (0, 1)
        
        def get_probability_range(value: float) -> tuple:
            """Probabilities should be between 0 and 1"""
            return (0, 1)
        
        def get_weekday_range(value: float) -> tuple:
            """Weekdays should be between 0 (Monday) and 6 (Sunday)"""
            return (0, 6)
        
        def get_percentage_range(value: float) -> tuple:
            """Percentages should be between 0 and 100"""
            return (0, 100)
        
        def get_cashflow_range(value: float) -> tuple:
            """Cashflow can be any value"""
            return (None, None)
        
        def get_negative_range(value: float) -> tuple:
            """Value should be negative (less than or equal to 0)"""
            return (None, 0)

        self.rules: Dict[str, List[MetricRule]] = {
            "balance": [
                MetricRule("inflow_growth_rate", ValidationType.RATIO, get_growth_rate_range,
                          None, "Growth rate should be >= -1 (can be negative but not less than -100%)"),
                MetricRule("inflow_daily_average", ValidationType.NON_NEGATIVE, 0, None,
                          "Daily average inflow should be non-negative"),
                MetricRule("outflow_daily_average", ValidationType.CASHFLOW, get_negative_range,
                          None, "Daily average outflow should be negative (less than or equal to 0)"),
                MetricRule("latest_balance", ValidationType.AMOUNT, None, None,
                          "Latest balance can be positive or negative"),
                MetricRule("balance_minimum", ValidationType.AMOUNT, None, None,
                          "Minimum balance can be positive or negative"),
                MetricRule("balance_average", ValidationType.AMOUNT, None, None,
                          "Average balance can be positive or negative"),
                MetricRule("change_in_balance", ValidationType.CASHFLOW, get_cashflow_range,
                          None, "Change in balance can be positive or negative"),
                MetricRule("weekday_balance_average", ValidationType.AMOUNT, None, None,
                          "Weekday average balance can be positive or negative"),
                MetricRule("weekday_with_highest_avg", ValidationType.WEEKDAY, get_weekday_range,
                          None, "Weekday should be between 0 (Monday) and 6 (Sunday)"),
                MetricRule("weekday_with_lowest_avg", ValidationType.WEEKDAY, get_weekday_range,
                          None, "Weekday should be between 0 (Monday) and 6 (Sunday)")
            ],
            "data_quality": [
                MetricRule("data_volume", ValidationType.NON_ZERO, 1, None,
                          "Should have at least one transaction"),
                MetricRule("date_range", ValidationType.NON_NEGATIVE, 0, None,
                          "Date range should be non-negative"),
                MetricRule("data_freshness", ValidationType.NON_NEGATIVE, 0, None,
                          "Days since last transaction should be non-negative"),
                MetricRule("has_balance_ratio", ValidationType.RATIO, get_ratio_range,
                          None, "Ratio should be between 0 and 1"),
                MetricRule("data_coverage", ValidationType.RATIO, get_ratio_range,
                          None, "Coverage ratio should be between 0 and 1"),
                MetricRule("accounts", ValidationType.NON_ZERO, 1, None,
                          "Should have at least one account"),
                MetricRule("potentially_duplicated_account_pairs", ValidationType.NON_NEGATIVE, 0, None,
                          "Count of duplicate pairs should be non-negative"),
                MetricRule("inflows", ValidationType.NON_NEGATIVE, 0, None,
                          "Count of inflows should be non-negative"),
                MetricRule("outflows", ValidationType.NON_NEGATIVE, 0, None,
                          "Count of outflows should be non-negative"),
                MetricRule("inflow_amount", ValidationType.NON_NEGATIVE, 0, None,
                          "Total inflow amount should be non-negative"),
                MetricRule("confidence", ValidationType.RATIO, get_ratio_range,
                          None, "Confidence score should be between 0 and 1"),
                MetricRule("revenue_anomalies", ValidationType.NON_NEGATIVE, 0, None,
                          "Count of anomalies should be non-negative")
            ],
            "debt": [
                MetricRule("last_debt_investment", ValidationType.NON_NEGATIVE, 0, None,
                          "Last debt investment amount should be non-negative"),
                MetricRule("last_debt_investment_days", ValidationType.NON_NEGATIVE, 0, None,
                          "Days since last investment should be non-negative"),
                MetricRule("debt_repayment_daily_average", ValidationType.NON_NEGATIVE, 0, None,
                          "Average daily debt repayment should be non-negative"),
                MetricRule("debt_investment", ValidationType.NON_NEGATIVE, 0, None,
                          "Total debt investment should be non-negative"),
                MetricRule("debt_investors", ValidationType.NON_NEGATIVE, 0, None,
                          "Count of debt investors should be non-negative"),
                MetricRule("debt_investment_count", ValidationType.NON_NEGATIVE, 0, None,
                          "Count of debt investments should be non-negative"),
                MetricRule("debt_repayment", ValidationType.NON_NEGATIVE, 0, None,
                          "Total debt repayment should be non-negative"),
                MetricRule("debt_service_coverage_ratio", ValidationType.CASHFLOW, None, None,
                          "Debt service coverage ratio can be positive or negative")
            ],
            "heron": [
                MetricRule("merchant_heron_ids", ValidationType.NON_NEGATIVE, 0, None,
                          "Merchant Heron ID should be a non-negative number"),
                MetricRule("predicted_nsf_fees", ValidationType.PROBABILITY, get_probability_range,
                          None, "Probability should be between 0 and 1"),
                MetricRule("predicted_balance_daily_average", ValidationType.AMOUNT, None, None,
                          "Predicted balance can be positive or negative"),
                MetricRule("heron_score", ValidationType.NON_NEGATIVE, 0, None,
                          "Heron score should be non-negative"),
                MetricRule("distinct_mcas_from_outflows", ValidationType.NON_NEGATIVE, 0, None,
                          "Count of distinct MCAs should be non-negative"),
                MetricRule("distinct_mcas_from_inflows", ValidationType.NON_NEGATIVE, 0, None,
                          "Count of distinct MCAs should be non-negative")
            ],
            "processing_quality": [
                MetricRule("category_coverage", ValidationType.RATIO, get_ratio_range,
                          None, "Category coverage ratio should be between 0 and 1"),
                MetricRule("merchant_coverage", ValidationType.RATIO, get_ratio_range,
                          None, "Merchant coverage ratio should be between 0 and 1"),
                MetricRule("unconnected_account_ratio", ValidationType.RATIO, 0, None,
                          "Unconnected account ratio should be non-negative")
            ],
            "profit_and_loss": [
                MetricRule("revenue_daily_average", ValidationType.NON_NEGATIVE, 0, None,
                          "Average daily revenue should be non-negative"),
                MetricRule("cogs_daily_average", ValidationType.NON_NEGATIVE, 0, None,
                          "Average daily COGS should be non-negative"),
                MetricRule("opex_daily_average", ValidationType.NON_NEGATIVE, 0, None,
                          "Average daily operational expenses should be non-negative"),
                MetricRule("revenue_sources", ValidationType.NON_NEGATIVE, 0, None,
                          "Count of revenue sources should be non-negative"),
                MetricRule("revenue", ValidationType.NON_NEGATIVE, 0, None,
                          "Total revenue should be non-negative"),
                MetricRule("annualized_revenue", ValidationType.NON_NEGATIVE, 0, None,
                          "Annualized revenue should be non-negative"),
                MetricRule("cogs", ValidationType.NON_NEGATIVE, 0, None,
                          "Total COGS should be non-negative"),
                MetricRule("average_credit_card_spend", ValidationType.NON_NEGATIVE, 0, None,
                          "Average credit card spend should be non-negative"),
                MetricRule("opex", ValidationType.NON_NEGATIVE, 0, None,
                          "Total operational expenses should be non-negative"),
                MetricRule("revenue_growth_rate", ValidationType.RATIO, get_growth_rate_range,
                          None, "Revenue growth rate should be >= -1 (can be negative but not less than -100%)"),
                MetricRule("revenue_profit_and_loss", ValidationType.NON_NEGATIVE, 0, None,
                          "Total revenue from P&L view should be non-negative"),
                MetricRule("annualized_revenue_profit_and_loss", ValidationType.NON_NEGATIVE, 0, None,
                          "Annualized revenue from P&L view should be non-negative"),
                MetricRule("cogs_profit_and_loss", ValidationType.NON_NEGATIVE, 0, None,
                          "Total COGS from P&L view should be non-negative"),
                MetricRule("opex_profit_and_loss", ValidationType.NON_NEGATIVE, 0, None,
                          "Total Opex from P&L view should be non-negative"),
                MetricRule("revenue_monthly_average", ValidationType.NON_NEGATIVE, 0, None,
                          "Average monthly revenue should be non-negative"),
                MetricRule("gross_operating_cashflow", ValidationType.CASHFLOW, get_cashflow_range,
                          None, "Gross operating cashflow can be positive or negative"),
                MetricRule("net_operating_cashflow", ValidationType.CASHFLOW, get_cashflow_range,
                          None, "Net operating cashflow can be positive or negative"),
                MetricRule("gross_operating_cashflow_profit_and_loss", ValidationType.CASHFLOW, get_cashflow_range,
                          None, "Gross operating cashflow from P&L view can be positive or negative"),
                MetricRule("net_operating_cashflow_profit_and_loss", ValidationType.CASHFLOW, get_cashflow_range,
                          None, "Net operating cashflow from P&L view can be positive or negative"),
                MetricRule("gross_operating_cashflow_daily_average", ValidationType.CASHFLOW, get_cashflow_range,
                          None, "Average daily gross operating cashflow can be positive or negative"),
                MetricRule("net_operating_cashflow_daily_average", ValidationType.CASHFLOW, get_cashflow_range,
                          None, "Average daily net operating cashflow can be positive or negative")
            ],
            "risk_flag": [
                MetricRule("deposit_days", ValidationType.NON_NEGATIVE, 0, None,
                          "Count of deposit days should be non-negative"),
                MetricRule("nsf_fees", ValidationType.NON_NEGATIVE, 0, None,
                          "Count of NSF fees should be non-negative"),
                MetricRule("nsf_days", ValidationType.NON_NEGATIVE, 0, None,
                          "Count of NSF days should be non-negative"),
                MetricRule("debt_collection", ValidationType.NON_NEGATIVE, 0, None,
                          "Total debt collection amount should be non-negative"),
                MetricRule("atm_withdrawals", ValidationType.NON_NEGATIVE, 0, None,
                          "Total ATM withdrawal amount should be non-negative"),
                MetricRule("tax_payments", ValidationType.NON_NEGATIVE, 0, None,
                          "Count of tax payments should be non-negative"),
                MetricRule("tax_payment_amount", ValidationType.NON_NEGATIVE, 0, None,
                          "Total tax payment amount should be non-negative"),
                MetricRule("negative_balance_days", ValidationType.NON_NEGATIVE, 0, None,
                          "Count of negative balance days should be non-negative"),
                MetricRule("negative_balance_days_by_account", ValidationType.NON_NEGATIVE, 0, None,
                          "Count of negative balance days by account should be non-negative")
            ]
        }

    def get_rule_for_metric(self, metric_name: str) -> Optional[MetricRule]:
        """Get validation rule for a specific metric"""
        for group_rules in self.rules.values():
            for rule in group_rules:
                if rule.metric_name == metric_name:
                    return rule
        return None

    def get_rules_for_group(self, group_name: str) -> List[MetricRule]:
        """Get all validation rules for a specific metric group"""
        return self.rules.get(group_name, [])

    def add_rule(self, group_name: str, rule: MetricRule) -> None:
        """Add a new validation rule"""
        if group_name not in self.rules:
            self.rules[group_name] = []
        self.rules[group_name].append(rule)

    def update_rule(self, metric_name: str, updated_rule: MetricRule) -> bool:
        """Update an existing validation rule"""
        for group_name, rules in self.rules.items():
            for i, rule in enumerate(rules):
                if rule.metric_name == metric_name:
                    self.rules[group_name][i] = updated_rule
                    return True
        return False

    def remove_rule(self, metric_name: str) -> bool:
        """Remove a validation rule"""
        for group_name, rules in self.rules.items():
            for i, rule in enumerate(rules):
                if rule.metric_name == metric_name:
                    del self.rules[group_name][i]
                    return True
        return False 