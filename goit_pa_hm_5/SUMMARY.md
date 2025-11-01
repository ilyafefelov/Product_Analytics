# Sample Size Calculation - Quick Reference

## MelodyFlow A/B Test: Smart Playlist Recommendations

---

## 📊 Main Results

### Primary Recommendation

```
╔═══════════════════════════════════════════════════════════╗
║         RECOMMENDED SAMPLE SIZE CALCULATION               ║
╠═══════════════════════════════════════════════════════════╣
║  Sample size per group:    9,097 users (~9,100)          ║
║  Total sample size:        18,194 users (~18,200)        ║
║                                                            ║
║  Test duration:            14-21 days                     ║
║  % of DAU needed:          9.1%                           ║
║  Feasibility:              ✅ HIGHLY FEASIBLE             ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 🎯 Test Parameters

| Parameter | Value | Justification |
|-----------|-------|---------------|
| **Baseline (p₁)** | 41.0% | Current 7-day retention |
| **Expected (p₂)** | 43.05% | Target retention |
| **MDE** | 2.05 pp (5% relative) | Balance between impact & practicality |
| **Significance (α)** | 0.05 | Industry standard, 95% confidence |
| **Power (1-β)** | 0.80 | Industry minimum, 80% chance to detect |
| **Test Type** | Two-sided | Conservative, checks both directions |

---

## 📐 Calculation Formula

```
n = (Z_{α/2} + Z_β)² × [p₁(1-p₁) + p₂(1-p₂)]
    ─────────────────────────────────────────
                  (p₂ - p₁)²

Where:
  Z_{α/2} = 1.96  (for α = 0.05, two-sided)
  Z_β     = 0.84  (for 80% power)
  p₁      = 0.41  (baseline)
  p₂      = 0.4305 (expected)
```

### Step-by-step:

1. **(Z_{α/2} + Z_β)² = (1.96 + 0.84)² = 7.84**
2. **p₁(1-p₁) = 0.41 × 0.59 = 0.2419**
3. **p₂(1-p₂) = 0.4305 × 0.5695 = 0.2452**
4. **Variance sum = 0.2419 + 0.2452 = 0.4871**
5. **(p₂ - p₁)² = (0.0205)² = 0.00042025**
6. **n = 7.84 × 0.4871 / 0.00042025 ≈ 9,097**

---

## 📊 Scenarios Comparison

| Scenario | MDE | Power | Type | n/group | Total | When to Use |
|----------|-----|-------|------|---------|-------|-------------|
| **Main** | **5%** | **80%** | **Two-sided** | **9,097** | **18,194** | **Standard recommendation** |
| High Power | 5% | 90% | Two-sided | 12,179 | 24,357 | Critical decisions |
| Large Effect | 10% | 80% | Two-sided | 2,286 | 4,572 | Quick validation |
| One-sided | 5% | 80% | One-sided | 7,166 | 14,332 | Only positive expected |

---

## ⏱️ Timeline

```
Day 0        Day 1-2           Day 8-9              Day 14-21
  │             │                  │                     │
  │             │                  │                     │
  ▼             ▼                  ▼                     ▼
Setup    Data Collection    First Results      Final Analysis
         (100k/day)         (Minimum)          (Recommended)
         
         ◄────────────────────────────────────────►
                     Test Duration
```

### Breakdown:
- **Setup:** 1 day (infrastructure, tracking, QA)
- **Collection:** 1-2 days (need ~18k users, have 200k DAU)
- **Observation:** 7 days (for 7-day retention metric)
- **Buffer:** 5-12 days (account for weekly patterns, stability)

**Total: 14-21 days recommended**

---

## ✅ Feasibility Check

### Resource Requirements:
```
Available Resources:
  • Total users:    1,000,000
  • Daily Active:   200,000 (20%)
  
Required Sample:
  • Total needed:   18,194 users
  • % of DAU:       9.1%
  • Days to fill:   < 1 day (with 50/50 split)

Verdict: ✅ HIGHLY FEASIBLE
```

### Traffic Allocation:
- **Control Group:** 50% → 100,000 users/day
- **Test Group:** 50% → 100,000 users/day
- Sample fills in **< 1 day** → plenty of buffer time

---

## 🎯 Success Criteria

### Primary Metric:
✅ **7-day retention increases from 41% to ≥43.05%**
- Statistical significance: p-value < 0.05
- Practical significance: +2.05 percentage points

### Guardrail Metrics:
- ARPPU: No significant decrease
- Revenue: Stable or increased
- Technical stability: No increase in errors
- App performance: No degradation

### Secondary Metrics:
- Session duration
- Tracks played per session
- Playlist engagement
- Feature adoption rate

---

## 🔍 Statistical Concepts

### What is MDE (Minimum Detectable Effect)?
> The smallest effect size that the test can reliably detect.
> **Our MDE:** 5% relative improvement (2.05 pp absolute)
> 
> **Why 5%?** 
> - Smaller = needs more users (expensive, long)
> - Larger = might miss smaller valuable effects
> - 5% = good balance for AI feature impact

### What is Statistical Power?
> Probability of detecting an effect when it truly exists.
> **Our Power:** 80%
> 
> **Interpretation:** 
> - If the true effect is 5%, we have 80% chance to detect it
> - 20% risk of "false negative" (missing real effect)

### What is Significance Level (α)?
> Probability of false positive (claiming effect when none exists).
> **Our α:** 0.05 (5%)
> 
> **Interpretation:**
> - 5% chance of incorrectly claiming success
> - 95% confidence in positive results

### Two-sided vs One-sided Test?
> **Two-sided:** Tests both increase AND decrease
> **One-sided:** Tests only one direction
> 
> **We chose two-sided because:**
> - AI feature could potentially hurt retention (bugs, poor UX)
> - More conservative and safer
> - Industry standard for product tests

---

## 📝 Key Assumptions

1. **Randomization:** Users randomly assigned to control/test
2. **Independence:** User behaviors are independent
3. **Stable baseline:** 41% retention is stable during test
4. **No contamination:** Control users don't see test feature
5. **Consistent environment:** No major external factors (holidays, campaigns)
6. **Sample representative:** Test users represent overall population

---

## ⚠️ Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Seasonality effects | ⚠️ Medium | Extend test to 21 days, cover full weeks |
| Technical issues | ⚠️ Medium | Robust monitoring, quick rollback plan |
| Novelty effect | ⚠️ Low | Monitor engagement beyond initial period |
| Selection bias | 🛑 High | Ensure proper randomization |
| External events | ⚠️ Medium | Track external factors, have backup plan |

---

## 🚀 Implementation Checklist

- [ ] Setup A/B testing infrastructure
- [ ] Configure 50/50 traffic split
- [ ] Implement feature flag for test group
- [ ] Setup metric tracking and dashboards
- [ ] Define guardrail metrics and thresholds
- [ ] Create monitoring alerts
- [ ] Prepare rollback procedure
- [ ] QA test on staging environment
- [ ] Get stakeholder approval
- [ ] Launch test
- [ ] Monitor daily for first 3 days
- [ ] Check weekly patterns
- [ ] Analyze results after 14-21 days
- [ ] Make launch decision

---

## 📚 References

### Formulas:
- Sample size for two proportions (Fleiss, 1981)
- Effect size (Cohen's h) for binomial metrics

### Tools Used:
- Python with scipy.stats
- Mathematical verification by hand
- Cross-checked with industry calculators

### Standards Applied:
- Industry standard α = 0.05
- Minimum recommended power = 0.80
- Conservative two-sided approach

---

**Document Version:** 1.0  
**Author:** Fefelov  
**Date:** October 31, 2025  
**Course:** GoIT Product Analytics - Assignment 5
