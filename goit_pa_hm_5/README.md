# Homework 5: Sample Size Calculation for Binomial Metric

## Assignment Overview

**Course:** Product Analytics  
**Student:** Fefelov  
**Date:** October 31, 2025

## Task Description

Calculate sample size for an A/B test for MelodyFlow music streaming app. The test evaluates a new "Smart Playlist Recommendations" feature that uses AI to create personalized playlists based on user listening history.

**Primary Metric:** 7-day retention rate

## Files in This Directory

1. **Fefelov_PA_assignment_5.md** - Complete homework document with:
   - Problem context and hypothesis
   - Detailed calculations with explanations
   - MDE, significance level, and power justification
   - Test type selection rationale
   - Multiple scenarios comparison
   - Practical recommendations
   - Mathematical appendix

2. **sample_size_calculator.py** - Python script for verification:
   - Calculates sample size for binomial metrics
   - Multiple scenarios (different MDE, power levels)
   - Test duration estimation
   - Feasibility analysis
   - Results visualization

## Quick Summary

### Recommended Test Design

- **Sample size per group:** 9,097 users (~9,100 rounded)
- **Total sample size:** 18,194 users (~18,200 rounded)
- **MDE:** 5% relative improvement (41% → 43.05%)
- **Significance level (α):** 0.05
- **Statistical power:** 80%
- **Test type:** Two-sided
- **Duration:** 14-21 days (recommended)

## Key Results

| Scenario | MDE | Power | n per group | Total | Duration |
|----------|-----|-------|-------------|-------|----------|
| **Main (Recommended)** | 5% | 80% | 9,097 | 18,194 | 8-14 days |
| Higher Power | 5% | 90% | 12,179 | 24,357 | 8-14 days |
| Larger Effect | 10% | 80% | 2,286 | 4,572 | 8-14 days |
| One-sided | 5% | 80% | 7,166 | 14,332 | 8-14 days |

## Running the Python Script

```powershell
# Navigate to homework directory
cd goit_pa_hm_5

# Run the calculator
python sample_size_calculator.py
```

The script will output:
- Detailed calculations for all scenarios
- Test duration estimates
- Feasibility analysis
- Summary comparison table
- Final recommendations

## Key Formulas Used

### Sample Size for Two Proportions

```
n = (Z_{α/2} + Z_β)² × [p₁(1-p₁) + p₂(1-p₂)] / (p₂ - p₁)²
```

Where:
- **n** = sample size per group
- **Z_{α/2}** = 1.96 (for α = 0.05, two-sided)
- **Z_β** = 0.84 (for 80% power)
- **p₁** = 0.41 (baseline retention)
- **p₂** = 0.4305 (expected retention)

## Deliverables Checklist

- [x] Document with MDE definition and justification
- [x] Significance level (α) selection and rationale
- [x] Statistical power selection and rationale
- [x] Test type selection (one-sided vs two-sided)
- [x] Sample size calculation with detailed steps
- [x] Multiple scenarios comparison
- [x] Practical feasibility analysis
- [x] Python verification script
- [x] Clear explanations and conclusions
- [x] Ready for Google Drive upload

