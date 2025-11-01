"""
Sample Size Calculator for Binomial Metric (7-day Retention)
Homework 5: MelodyFlow A/B Test - Smart Playlist Recommendations

Author: Fefelov
Date: October 31, 2025
"""

import numpy as np
from scipy import stats
import math


def calculate_sample_size_binomial(
    p1: float,
    p2: float,
    alpha: float = 0.05,
    power: float = 0.80,
    two_sided: bool = True
) -> dict:
    """
    Calculate sample size for comparing two proportions (binomial metric).
    
    Parameters:
    -----------
    p1 : float
        Baseline proportion (control group)
    p2 : float
        Expected proportion (test group)
    alpha : float
        Significance level (default: 0.05)
    power : float
        Statistical power (default: 0.80)
    two_sided : bool
        Whether to use two-sided test (default: True)
    
    Returns:
    --------
    dict : Dictionary with calculation results
    """
    
    # Z-values
    if two_sided:
        z_alpha = stats.norm.ppf(1 - alpha/2)
    else:
        z_alpha = stats.norm.ppf(1 - alpha)
    
    z_beta = stats.norm.ppf(power)
    
    # Calculate sample size
    numerator = (z_alpha + z_beta) ** 2
    variance_sum = p1 * (1 - p1) + p2 * (1 - p2)
    diff_squared = (p2 - p1) ** 2
    
    n_per_group = numerator * variance_sum / diff_squared
    
    # Calculate effect size (Cohen's h)
    effect_size = 2 * (math.asin(math.sqrt(p2)) - math.asin(math.sqrt(p1)))
    
    # Relative improvement
    relative_improvement = (p2 - p1) / p1
    
    return {
        'n_per_group': math.ceil(n_per_group),
        'total_sample': math.ceil(n_per_group * 2),
        'p1': p1,
        'p2': p2,
        'absolute_difference': p2 - p1,
        'relative_improvement': relative_improvement,
        'effect_size': effect_size,
        'z_alpha': z_alpha,
        'z_beta': z_beta,
        'alpha': alpha,
        'power': power,
        'test_type': 'two-sided' if two_sided else 'one-sided'
    }


def print_results(results: dict, scenario_name: str = ""):
    """Print formatted results."""
    if scenario_name:
        print(f"\n{'='*70}")
        print(f"Scenario: {scenario_name}")
        print(f"{'='*70}")
    
    print(f"\nInput Parameters:")
    print(f"  Baseline proportion (p1):     {results['p1']:.4f} ({results['p1']*100:.2f}%)")
    print(f"  Expected proportion (p2):     {results['p2']:.4f} ({results['p2']*100:.2f}%)")
    print(f"  Absolute difference:          {results['absolute_difference']:.4f} ({results['absolute_difference']*100:.2f} pp)")
    print(f"  Relative improvement:         {results['relative_improvement']*100:.2f}%")
    print(f"  Significance level (α):       {results['alpha']:.4f}")
    print(f"  Statistical power (1-β):      {results['power']:.4f}")
    print(f"  Test type:                    {results['test_type']}")
    
    print(f"\nCalculated Values:")
    print(f"  Z(α/2):                       {results['z_alpha']:.4f}")
    print(f"  Z(β):                         {results['z_beta']:.4f}")
    print(f"  Effect size (Cohen's h):      {results['effect_size']:.4f}")
    
    print(f"\n{'*'*70}")
    print(f"RESULTS:")
    print(f"  Sample size per group:        {results['n_per_group']:,} users")
    print(f"  Total sample size:            {results['total_sample']:,} users")
    print(f"{'*'*70}")


def estimate_test_duration(n_total: int, dau: int, traffic_split: float = 0.5):
    """
    Estimate test duration based on available traffic.
    
    Parameters:
    -----------
    n_total : int
        Total required sample size
    dau : int
        Daily Active Users
    traffic_split : float
        Proportion of traffic allocated to experiment (default: 0.5 for 50/50 split)
    """
    users_per_day = dau * traffic_split
    days_to_collect = math.ceil(n_total / users_per_day)
    observation_period = 7  # For 7-day retention
    
    total_days = days_to_collect + observation_period
    
    print(f"\nTest Duration Estimate:")
    print(f"  DAU:                          {dau:,} users")
    print(f"  Traffic allocation:           {traffic_split*100:.0f}%")
    print(f"  Users per day in experiment:  {int(users_per_day):,} users")
    print(f"  Days to collect sample:       {days_to_collect} days")
    print(f"  Observation period (7-day):   {observation_period} days")
    print(f"  Minimum total duration:       {total_days} days")
    print(f"  Recommended duration:         14-21 days (for stability)")


def main():
    """Main execution function."""
    
    print("="*70)
    print("SAMPLE SIZE CALCULATOR FOR MELODYFLOW A/B TEST")
    print("Feature: Smart Playlist Recommendations")
    print("Metric: 7-day Retention Rate")
    print("="*70)
    
    # Given data
    total_users = 1_000_000
    dau = 200_000  # 20% of total users
    baseline_retention = 0.41
    
    print(f"\nCurrent Product Metrics:")
    print(f"  Total users:                  {total_users:,}")
    print(f"  DAU (20%):                    {dau:,}")
    print(f"  Baseline 7-day retention:     {baseline_retention*100:.1f}%")
    
    # Scenario 1: Main scenario (5% relative improvement, 80% power)
    print("\n" + "="*70)
    print("SCENARIO 1: RECOMMENDED (Main)")
    print("="*70)
    
    results_main = calculate_sample_size_binomial(
        p1=0.41,
        p2=0.41 * 1.05,  # 5% relative improvement
        alpha=0.05,
        power=0.80,
        two_sided=True
    )
    print_results(results_main)
    estimate_test_duration(results_main['total_sample'], dau, traffic_split=0.5)
    
    # Scenario 2: Higher power (90%)
    print("\n" + "="*70)
    print("SCENARIO 2: HIGHER POWER")
    print("="*70)
    
    results_high_power = calculate_sample_size_binomial(
        p1=0.41,
        p2=0.41 * 1.05,
        alpha=0.05,
        power=0.90,
        two_sided=True
    )
    print_results(results_high_power, "5% improvement with 90% power")
    estimate_test_duration(results_high_power['total_sample'], dau, traffic_split=0.5)
    
    # Scenario 3: Larger effect (10% relative improvement)
    print("\n" + "="*70)
    print("SCENARIO 3: LARGER EFFECT")
    print("="*70)
    
    results_large_effect = calculate_sample_size_binomial(
        p1=0.41,
        p2=0.41 * 1.10,  # 10% relative improvement
        alpha=0.05,
        power=0.80,
        two_sided=True
    )
    print_results(results_large_effect, "10% improvement with 80% power")
    estimate_test_duration(results_large_effect['total_sample'], dau, traffic_split=0.5)
    
    # Scenario 4: One-sided test (for comparison)
    print("\n" + "="*70)
    print("SCENARIO 4: ONE-SIDED TEST (For Comparison)")
    print("="*70)
    
    results_one_sided = calculate_sample_size_binomial(
        p1=0.41,
        p2=0.41 * 1.05,
        alpha=0.05,
        power=0.80,
        two_sided=False
    )
    print_results(results_one_sided, "5% improvement with one-sided test")
    estimate_test_duration(results_one_sided['total_sample'], dau, traffic_split=0.5)
    
    # Summary comparison
    print("\n" + "="*70)
    print("SUMMARY COMPARISON TABLE")
    print("="*70)
    
    print(f"\n{'Scenario':<30} {'MDE':<8} {'Power':<8} {'Test Type':<12} {'n/group':<10} {'Total':<10} {'Duration*'}")
    print("-" * 100)
    print(f"{'Main (Recommended)':<30} {'5%':<8} {'80%':<8} {'Two-sided':<12} {results_main['n_per_group']:<10,} {results_main['total_sample']:<10,} {'8-14 days'}")
    print(f"{'Higher Power':<30} {'5%':<8} {'90%':<8} {'Two-sided':<12} {results_high_power['n_per_group']:<10,} {results_high_power['total_sample']:<10,} {'8-14 days'}")
    print(f"{'Larger Effect':<30} {'10%':<8} {'80%':<8} {'Two-sided':<12} {results_large_effect['n_per_group']:<10,} {results_large_effect['total_sample']:<10,} {'8-14 days'}")
    print(f"{'One-sided':<30} {'5%':<8} {'80%':<8} {'One-sided':<12} {results_one_sided['n_per_group']:<10,} {results_one_sided['total_sample']:<10,} {'8-14 days'}")
    
    print("\n* Duration includes collection period + 7-day observation + buffer for stability")
    
    # Feasibility check
    print("\n" + "="*70)
    print("FEASIBILITY ANALYSIS")
    print("="*70)
    
    required_percentage = (results_main['total_sample'] / dau) * 100
    
    print(f"\nRequired sample:              {results_main['total_sample']:,} users")
    print(f"Available DAU:                {dau:,} users")
    print(f"Required % of DAU:            {required_percentage:.1f}%")
    print(f"\n✅ FEASIBILITY: The test is HIGHLY FEASIBLE with current user base.")
    print(f"   We only need {required_percentage:.1f}% of daily active users.")
    print(f"   With 50/50 traffic split, we can collect the sample in 1-2 days.")
    
    # Recommendations
    print("\n" + "="*70)
    print("FINAL RECOMMENDATIONS")
    print("="*70)
    
    print(f"""
1. Recommended Design:
   - Sample size per group: {results_main['n_per_group']:,} users
   - Total sample size: {results_main['total_sample']:,} users
   - Traffic split: 50% control / 50% test
   - Test duration: 14-21 days (recommended for stability)
   - Metric: 7-day retention rate

2. Key Parameters:
   - MDE: 5% relative improvement (41% → 43.05%)
   - Significance level: α = 0.05
   - Statistical power: 80%
   - Test type: Two-sided

3. Success Criteria:
   - 7-day retention increases from 41% to at least 43.05%
   - p-value < 0.05
   - No negative impact on guardrail metrics

4. Monitoring:
   - Daily monitoring of key metrics
   - Guardrail metrics: ARPPU, revenue, technical stability
   - Engagement metrics: session duration, tracks played
    """)
    
    print("="*70)
    print("Calculation completed successfully!")
    print("="*70)


if __name__ == "__main__":
    main()
