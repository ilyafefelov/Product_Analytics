# -*- coding: utf-8 -*-
"""
Final Project: A/B Test Analysis for Online Advertising Campaign
GoIT Product Analytics Course

Author: Fefelov
Date: November 6, 2025

This script performs comprehensive A/B test analysis comparing Control and Test campaigns:
1. Data loading and preprocessing
2. Statistical significance testing (t-tests)
3. Conversion rate calculations
4. Confidence interval computations
5. Funnel analysis
6. Summary statistics generation
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Tuple, Dict
import warnings
warnings.filterwarnings('ignore')


class ABTestAnalyzer:
    """A/B Test Analysis for advertising campaign comparison."""
    
    def __init__(self, control_path: str, test_path: str):
        """Initialize analyzer with data paths."""
        self.control_path = Path(control_path)
        self.test_path = Path(test_path)
        self.control_df = None
        self.test_df = None
        self.combined_df = None
        
    def load_data(self) -> None:
        """Load and preprocess both datasets."""
        print("Loading data...")
        
        # Load CSV files (semicolon-separated)
        self.control_df = pd.read_csv(self.control_path, sep=';', encoding='utf-8')
        self.test_df = pd.read_csv(self.test_path, sep=';', encoding='utf-8')
        
        # Convert date columns
        self.control_df['Date'] = pd.to_datetime(self.control_df['Date'], format='%d.%m.%Y')
        self.test_df['Date'] = pd.to_datetime(self.test_df['Date'], format='%d.%m.%Y')
        
        # Add group identifier
        self.control_df['Group'] = 'Control'
        self.test_df['Group'] = 'Test'
        
        # Handle missing values (Aug 5 in control has missing data)
        print("\nChecking for missing values...")
        print(f"Control missing: {self.control_df.isnull().sum().sum()}")
        print(f"Test missing: {self.test_df.isnull().sum().sum()}")
        
        # Drop rows with all funnel metrics missing (Aug 5 control)
        funnel_cols = ['# of Impressions', 'Reach', '# of Website Clicks', 
                       '# of Searches', '# of View Content', '# of Add to Cart', '# of Purchase']
        
        control_complete = self.control_df.dropna(subset=funnel_cols, how='all')
        print(f"\nRemoved {len(self.control_df) - len(control_complete)} incomplete rows from control")
        self.control_df = control_complete
        
        # Combine for some analyses
        self.combined_df = pd.concat([self.control_df, self.test_df], ignore_index=True)
        
        print(f"\nData loaded successfully:")
        print(f"  Control: {len(self.control_df)} days")
        print(f"  Test: {len(self.test_df)} days")
        
    def calculate_aggregate_metrics(self) -> Dict:
        """Calculate aggregated metrics for both groups."""
        print("\n" + "="*70)
        print("CALCULATING AGGREGATE METRICS")
        print("="*70)
        
        results = {}
        
        for group_name, df in [('Control', self.control_df), ('Test', self.test_df)]:
            metrics = {
                'total_spend': df['Spend [USD]'].sum(),
                'total_impressions': df['# of Impressions'].sum(),
                'total_reach': df['Reach'].sum(),
                'total_clicks': df['# of Website Clicks'].sum(),
                'total_searches': df['# of Searches'].sum(),
                'total_view_content': df['# of View Content'].sum(),
                'total_add_to_cart': df['# of Add to Cart'].sum(),
                'total_purchases': df['# of Purchase'].sum(),
                'days': len(df)
            }
            
            # Calculate rates
            metrics['ctr'] = metrics['total_clicks'] / metrics['total_impressions'] if metrics['total_impressions'] > 0 else 0
            metrics['click_to_search'] = metrics['total_searches'] / metrics['total_clicks'] if metrics['total_clicks'] > 0 else 0
            metrics['search_to_view'] = metrics['total_view_content'] / metrics['total_searches'] if metrics['total_searches'] > 0 else 0
            metrics['view_to_cart'] = metrics['total_add_to_cart'] / metrics['total_view_content'] if metrics['total_view_content'] > 0 else 0
            metrics['cart_to_purchase'] = metrics['total_purchases'] / metrics['total_add_to_cart'] if metrics['total_add_to_cart'] > 0 else 0
            metrics['overall_conversion'] = metrics['total_purchases'] / metrics['total_clicks'] if metrics['total_clicks'] > 0 else 0
            
            # Cost metrics
            metrics['cost_per_click'] = metrics['total_spend'] / metrics['total_clicks'] if metrics['total_clicks'] > 0 else 0
            metrics['cost_per_purchase'] = metrics['total_spend'] / metrics['total_purchases'] if metrics['total_purchases'] > 0 else 0
            metrics['roas_proxy'] = metrics['total_purchases'] / metrics['total_spend'] if metrics['total_spend'] > 0 else 0
            
            # Daily averages
            metrics['avg_daily_spend'] = metrics['total_spend'] / metrics['days']
            metrics['avg_daily_purchases'] = metrics['total_purchases'] / metrics['days']
            
            results[group_name] = metrics
        
        self.aggregate_metrics = results
        return results
    
    def print_aggregate_summary(self) -> None:
        """Print formatted summary of aggregate metrics."""
        print("\n" + "="*70)
        print("AGGREGATE METRICS SUMMARY")
        print("="*70)
        
        ctrl = self.aggregate_metrics['Control']
        test = self.aggregate_metrics['Test']
        
        print(f"\n{'Metric':<30} {'Control':<20} {'Test':<20} {'Difference':<15}")
        print("-" * 85)
        
        # Volume metrics
        print(f"{'Total Spend ($)':<30} {ctrl['total_spend']:>20,.2f} {test['total_spend']:>20,.2f} {test['total_spend']-ctrl['total_spend']:>15,.2f}")
        print(f"{'Total Impressions':<30} {ctrl['total_impressions']:>20,} {test['total_impressions']:>20,} {test['total_impressions']-ctrl['total_impressions']:>15,}")
        print(f"{'Total Clicks':<30} {ctrl['total_clicks']:>20,} {test['total_clicks']:>20,} {test['total_clicks']-ctrl['total_clicks']:>15,}")
        print(f"{'Total Purchases':<30} {ctrl['total_purchases']:>20,} {test['total_purchases']:>20,} {test['total_purchases']-ctrl['total_purchases']:>15,}")
        
        print("\n" + "-" * 85)
        
        # Rate metrics (percentages)
        print(f"{'CTR (%)':<30} {ctrl['ctr']*100:>20.3f} {test['ctr']*100:>20.3f} {(test['ctr']-ctrl['ctr'])*100:>15.3f}")
        print(f"{'Cart→Purchase (%)':<30} {ctrl['cart_to_purchase']*100:>20.3f} {test['cart_to_purchase']*100:>20.3f} {(test['cart_to_purchase']-ctrl['cart_to_purchase'])*100:>15.3f}")
        print(f"{'Overall Conversion (%)':<30} {ctrl['overall_conversion']*100:>20.3f} {test['overall_conversion']*100:>20.3f} {(test['overall_conversion']-ctrl['overall_conversion'])*100:>15.3f}")
        
        print("\n" + "-" * 85)
        
        # Cost metrics
        print(f"{'Cost per Click ($)':<30} {ctrl['cost_per_click']:>20.2f} {test['cost_per_click']:>20.2f} {test['cost_per_click']-ctrl['cost_per_click']:>15.2f}")
        print(f"{'Cost per Purchase ($)':<30} {ctrl['cost_per_purchase']:>20.2f} {test['cost_per_purchase']:>20.2f} {test['cost_per_purchase']-ctrl['cost_per_purchase']:>15.2f}")
        
        # Relative improvements
        print("\n" + "="*70)
        print("RELATIVE IMPROVEMENTS (Test vs Control)")
        print("="*70)
        
        improvements = {
            'CTR': (test['ctr'] / ctrl['ctr'] - 1) * 100,
            'Cart→Purchase': (test['cart_to_purchase'] / ctrl['cart_to_purchase'] - 1) * 100,
            'Overall Conversion': (test['overall_conversion'] / ctrl['overall_conversion'] - 1) * 100,
            'Cost per Purchase': (test['cost_per_purchase'] / ctrl['cost_per_purchase'] - 1) * 100,
        }
        
        for metric, pct in improvements.items():
            direction = "↑" if pct > 0 else "↓"
            print(f"{metric:<30} {direction} {abs(pct):>6.2f}%")
    
    def perform_t_tests(self) -> Dict:
        """Perform independent t-tests on daily metrics."""
        print("\n" + "="*70)
        print("STATISTICAL SIGNIFICANCE TESTING (Independent T-Tests)")
        print("="*70)
        
        # Daily metrics to test
        metrics_to_test = [
            ('Spend [USD]', 'Daily Spend'),
            ('# of Impressions', 'Daily Impressions'),
            ('# of Website Clicks', 'Daily Clicks'),
            ('# of Searches', 'Daily Searches'),
            ('# of View Content', 'Daily View Content'),
            ('# of Add to Cart', 'Daily Add to Cart'),
            ('# of Purchase', 'Daily Purchases'),
        ]
        
        # Calculate daily conversion rates
        self.control_df['CTR'] = self.control_df['# of Website Clicks'] / self.control_df['# of Impressions']
        self.test_df['CTR'] = self.test_df['# of Website Clicks'] / self.test_df['# of Impressions']
        
        self.control_df['Cart_to_Purchase'] = self.control_df['# of Purchase'] / self.control_df['# of Add to Cart']
        self.test_df['Cart_to_Purchase'] = self.test_df['# of Purchase'] / self.test_df['# of Add to Cart']
        
        self.control_df['Overall_Conversion'] = self.control_df['# of Purchase'] / self.control_df['# of Website Clicks']
        self.test_df['Overall_Conversion'] = self.test_df['# of Purchase'] / self.test_df['# of Website Clicks']
        
        metrics_to_test.extend([
            ('CTR', 'Click-Through Rate'),
            ('Cart_to_Purchase', 'Cart to Purchase Rate'),
            ('Overall_Conversion', 'Overall Conversion Rate'),
        ])
        
        results = {}
        
        print(f"\n{'Metric':<35} {'t-statistic':<15} {'p-value':<15} {'Significant?':<15}")
        print("-" * 80)
        
        for col, name in metrics_to_test:
            control_data = self.control_df[col].dropna()
            test_data = self.test_df[col].dropna()
            
            # Two-sided independent t-test
            t_stat, p_value = stats.ttest_ind(control_data, test_data, equal_var=False)
            
            is_significant = p_value < 0.05
            sig_marker = "✓ YES" if is_significant else "✗ NO"
            
            results[name] = {
                't_statistic': t_stat,
                'p_value': p_value,
                'significant': is_significant,
                'control_mean': control_data.mean(),
                'test_mean': test_data.mean(),
                'control_std': control_data.std(),
                'test_std': test_data.std(),
            }
            
            print(f"{name:<35} {t_stat:>15.4f} {p_value:>15.6f} {sig_marker:<15}")
        
        self.t_test_results = results
        return results
    
    def calculate_confidence_interval_cart_to_purchase(self, confidence: float = 0.95) -> Dict:
        """
        Calculate confidence interval for the difference in Cart→Purchase conversion rates.
        
        This is the key metric for Task 5.
        """
        print("\n" + "="*70)
        print("CONFIDENCE INTERVAL: Cart→Purchase Conversion Rate Difference")
        print("="*70)
        
        # Aggregate totals
        ctrl_purchases = self.control_df['# of Purchase'].sum()
        ctrl_carts = self.control_df['# of Add to Cart'].sum()
        test_purchases = self.test_df['# of Purchase'].sum()
        test_carts = self.test_df['# of Add to Cart'].sum()
        
        # Conversion rates
        p_ctrl = ctrl_purchases / ctrl_carts
        p_test = test_purchases / test_carts
        
        # Standard errors
        se_ctrl = np.sqrt(p_ctrl * (1 - p_ctrl) / ctrl_carts)
        se_test = np.sqrt(p_test * (1 - p_test) / test_carts)
        
        # Difference and its SE
        diff = p_test - p_ctrl
        se_diff = np.sqrt(se_ctrl**2 + se_test**2)
        
        # Z-score for confidence level
        alpha = 1 - confidence
        z = stats.norm.ppf(1 - alpha/2)
        
        # Confidence interval
        ci_lower = diff - z * se_diff
        ci_upper = diff + z * se_diff
        
        result = {
            'control_rate': p_ctrl,
            'test_rate': p_test,
            'difference': diff,
            'se_difference': se_diff,
            'confidence_level': confidence,
            'z_score': z,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'contains_zero': ci_lower <= 0 <= ci_upper,
            'ctrl_purchases': ctrl_purchases,
            'ctrl_carts': ctrl_carts,
            'test_purchases': test_purchases,
            'test_carts': test_carts,
        }
        
        print(f"\nControl Group:")
        print(f"  Add to Cart: {ctrl_carts:,}")
        print(f"  Purchases: {ctrl_purchases:,}")
        print(f"  Conversion Rate: {p_ctrl*100:.2f}%")
        
        print(f"\nTest Group:")
        print(f"  Add to Cart: {test_carts:,}")
        print(f"  Purchases: {test_purchases:,}")
        print(f"  Conversion Rate: {p_test*100:.2f}%")
        
        print(f"\nDifference (Test - Control):")
        print(f"  Point Estimate: {diff*100:.2f} percentage points")
        print(f"  Standard Error: {se_diff*100:.2f} pp")
        
        print(f"\n{confidence*100:.0f}% Confidence Interval:")
        print(f"  Lower Bound: {ci_lower*100:.2f} pp")
        print(f"  Upper Bound: {ci_upper*100:.2f} pp")
        print(f"  Interval: [{ci_lower*100:.2f}%, {ci_upper*100:.2f}%]")
        
        if result['contains_zero']:
            print(f"\n⚠️  CI contains zero → NO statistically significant difference")
        else:
            print(f"\n✓ CI does NOT contain zero → statistically significant difference")
            if diff > 0:
                print(f"  Test campaign has BETTER conversion rate")
            else:
                print(f"  Control campaign has BETTER conversion rate")
        
        self.ci_result = result
        return result
    
    def generate_funnel_data(self) -> pd.DataFrame:
        """Generate funnel stage data for visualization."""
        print("\n" + "="*70)
        print("FUNNEL ANALYSIS")
        print("="*70)
        
        stages = [
            'Impressions',
            'Clicks',
            'Searches',
            'View Content',
            'Add to Cart',
            'Purchase'
        ]
        
        control_values = [
            self.aggregate_metrics['Control']['total_impressions'],
            self.aggregate_metrics['Control']['total_clicks'],
            self.aggregate_metrics['Control']['total_searches'],
            self.aggregate_metrics['Control']['total_view_content'],
            self.aggregate_metrics['Control']['total_add_to_cart'],
            self.aggregate_metrics['Control']['total_purchases'],
        ]
        
        test_values = [
            self.aggregate_metrics['Test']['total_impressions'],
            self.aggregate_metrics['Test']['total_clicks'],
            self.aggregate_metrics['Test']['total_searches'],
            self.aggregate_metrics['Test']['total_view_content'],
            self.aggregate_metrics['Test']['total_add_to_cart'],
            self.aggregate_metrics['Test']['total_purchases'],
        ]
        
        funnel_df = pd.DataFrame({
            'Stage': stages,
            'Control': control_values,
            'Test': test_values,
        })
        
        # Calculate conversion rates from previous stage
        funnel_df['Control_Rate'] = funnel_df['Control'] / funnel_df['Control'].shift(1) * 100
        funnel_df['Test_Rate'] = funnel_df['Test'] / funnel_df['Test'].shift(1) * 100
        
        # Drop rate (inverse of conversion)
        funnel_df['Control_Drop'] = 100 - funnel_df['Control_Rate']
        funnel_df['Test_Drop'] = 100 - funnel_df['Test_Rate']
        
        print("\nFunnel Stage Counts:")
        print(funnel_df[['Stage', 'Control', 'Test']].to_string(index=False))
        
        print("\nStage-to-Stage Conversion Rates (%):")
        print(funnel_df[['Stage', 'Control_Rate', 'Test_Rate']].to_string(index=False))
        
        self.funnel_data = funnel_df
        return funnel_df
    
    def export_results_summary(self, output_path: str) -> None:
        """Export comprehensive results summary to text file."""
        print(f"\n" + "="*70)
        print("EXPORTING RESULTS SUMMARY")
        print("="*70)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("A/B TEST ANALYSIS RESULTS SUMMARY\n")
            f.write("Final Project - Product Analytics\n")
            f.write("Author: Fefelov\n")
            f.write("Date: November 6, 2025\n")
            f.write("="*70 + "\n\n")
            
            # Aggregate metrics
            f.write("AGGREGATE METRICS\n")
            f.write("-"*70 + "\n")
            ctrl = self.aggregate_metrics['Control']
            test = self.aggregate_metrics['Test']
            
            f.write(f"Control Group ({ctrl['days']} days):\n")
            f.write(f"  Total Spend: ${ctrl['total_spend']:,.2f}\n")
            f.write(f"  Total Clicks: {ctrl['total_clicks']:,}\n")
            f.write(f"  Total Purchases: {ctrl['total_purchases']:,}\n")
            f.write(f"  CTR: {ctrl['ctr']*100:.3f}%\n")
            f.write(f"  Cart→Purchase: {ctrl['cart_to_purchase']*100:.2f}%\n")
            f.write(f"  Cost per Purchase: ${ctrl['cost_per_purchase']:.2f}\n\n")
            
            f.write(f"Test Group ({test['days']} days):\n")
            f.write(f"  Total Spend: ${test['total_spend']:,.2f}\n")
            f.write(f"  Total Clicks: {test['total_clicks']:,}\n")
            f.write(f"  Total Purchases: {test['total_purchases']:,}\n")
            f.write(f"  CTR: {test['ctr']*100:.3f}%\n")
            f.write(f"  Cart→Purchase: {test['cart_to_purchase']*100:.2f}%\n")
            f.write(f"  Cost per Purchase: ${test['cost_per_purchase']:.2f}\n\n")
            
            # T-test results
            f.write("\n" + "="*70 + "\n")
            f.write("STATISTICAL SIGNIFICANCE (T-Tests)\n")
            f.write("-"*70 + "\n")
            
            for metric, result in self.t_test_results.items():
                f.write(f"\n{metric}:\n")
                f.write(f"  Control Mean: {result['control_mean']:.4f}\n")
                f.write(f"  Test Mean: {result['test_mean']:.4f}\n")
                f.write(f"  t-statistic: {result['t_statistic']:.4f}\n")
                f.write(f"  p-value: {result['p_value']:.6f}\n")
                f.write(f"  Significant (α=0.05): {'YES' if result['significant'] else 'NO'}\n")
            
            # CI for cart to purchase
            f.write("\n" + "="*70 + "\n")
            f.write("CONFIDENCE INTERVAL: Cart→Purchase Conversion\n")
            f.write("-"*70 + "\n")
            ci = self.ci_result
            f.write(f"Control Rate: {ci['control_rate']*100:.2f}%\n")
            f.write(f"Test Rate: {ci['test_rate']*100:.2f}%\n")
            f.write(f"Difference: {ci['difference']*100:.2f} pp\n")
            f.write(f"95% CI: [{ci['ci_lower']*100:.2f}%, {ci['ci_upper']*100:.2f}%]\n")
            f.write(f"Contains Zero: {'Yes (not significant)' if ci['contains_zero'] else 'No (significant)'}\n")
            
            f.write("\n" + "="*70 + "\n")
            f.write("END OF SUMMARY\n")
            f.write("="*70 + "\n")
        
        print(f"Results summary exported to: {output_path}")
    
    def run_full_analysis(self) -> None:
        """Execute complete analysis pipeline."""
        print("\n" + "="*70)
        print("STARTING FULL A/B TEST ANALYSIS")
        print("="*70)
        
        self.load_data()
        self.calculate_aggregate_metrics()
        self.print_aggregate_summary()
        self.perform_t_tests()
        self.calculate_confidence_interval_cart_to_purchase()
        self.generate_funnel_data()
        
        # Export summary
        output_path = self.control_path.parent / 'analysis_results_summary.txt'
        self.export_results_summary(output_path)
        
        print("\n" + "="*70)
        print("ANALYSIS COMPLETE!")
        print("="*70)
        print("\nNext steps:")
        print("  1. Review analysis_results_summary.txt")
        print("  2. Use results to populate deliverable documents")
        print("  3. Run funnel visualization notebook")
        print("="*70)


def main():
    """Main execution function."""
    # Paths relative to script location
    script_dir = Path(__file__).parent
    control_path = script_dir / 'control_group.csv'
    test_path = script_dir / 'test_group.csv'
    
    # Create analyzer instance
    analyzer = ABTestAnalyzer(
        control_path=str(control_path),
        test_path=str(test_path)
    )
    
    # Run full analysis
    analyzer.run_full_analysis()
    
    return analyzer


if __name__ == "__main__":
    analyzer = main()
