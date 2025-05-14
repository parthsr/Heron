from balance_validator import BalanceValidator
from revenue_validator import RevenueValidator
from risk_validator import RiskValidator
import json
from pathlib import Path

def main():
    # Create output directory
    output_dir = Path('outputs')
    output_dir.mkdir(exist_ok=True)
    
    # Initialize validators
    validators = {
        'balance': BalanceValidator(),
        'revenue': RevenueValidator(),
        'risk': RiskValidator()
    }
    
    # Run all validators
    results = {}
    for name, validator in validators.items():
        print(f"Running {name} validator...")
        results[name] = validator.validate()
    
    # Generate summary
    summary = {
        'total_validators': len(validators),
        'validator_results': {
            name: {
                'metrics_analyzed': len(results[name]['distribution_analysis']),
                'anomalies_found': len(results[name]['anomaly_detection']),
                'companies_with_warnings': len(results[name]['consistency_checks']),
                'total_warnings': sum(len(w) for w in results[name]['consistency_checks'].values())
            }
            for name in validators.keys()
        }
    }
    
    # Save summary
    with open(output_dir / 'validation_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\nValidation complete!")
    print(f"Results saved in {output_dir}")
    print("\nSummary:")
    for name, stats in summary['validator_results'].items():
        print(f"\n{name.upper()} Validator:")
        print(f"  Metrics analyzed: {stats['metrics_analyzed']}")
        print(f"  Anomalies found: {stats['anomalies_found']}")
        print(f"  Companies with warnings: {stats['companies_with_warnings']}")
        print(f"  Total warnings: {stats['total_warnings']}")

if __name__ == "__main__":
    main() 