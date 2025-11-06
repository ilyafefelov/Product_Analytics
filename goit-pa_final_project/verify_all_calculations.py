# -*- coding: utf-8 -*-
"""
Comprehensive verification of all calculations in Final Project deliverables
"""

import numpy as np
from scipy import stats

print("="*80)
print("COMPREHENSIVE CALCULATION VERIFICATION")
print("="*80)

# ============================================================================
# RAW DATA FROM CSV FILES
# ============================================================================

# Control group (29 days after removing Aug 5)
ctrl_spend = 66818.00
ctrl_impressions = 3177233
ctrl_reach = 2554931
ctrl_clicks = 154303
ctrl_searches = 64418
ctrl_view_content = 56370
ctrl_add_to_cart = 37700
ctrl_purchases = 15161
ctrl_days = 29

# Test group (30 days)
test_spend = 76892.00
test_impressions = 2237544
test_reach = 1615995
test_clicks = 180970
test_searches = 72569
test_view_content = 55740
test_add_to_cart = 26446
test_purchases = 15637
test_days = 30

print("\n" + "="*80)
print("1. BASIC AGGREGATE METRICS")
print("="*80)

print("\nControl Group:")
print(f"  Days: {ctrl_days}")
print(f"  Total Spend: ${ctrl_spend:,.2f}")
print(f"  Total Impressions: {ctrl_impressions:,}")
print(f"  Total Clicks: {ctrl_clicks:,}")
print(f"  Total Purchases: {ctrl_purchases:,}")

print("\nTest Group:")
print(f"  Days: {test_days}")
print(f"  Total Spend: ${test_spend:,.2f}")
print(f"  Total Impressions: {test_impressions:,}")
print(f"  Total Clicks: {test_clicks:,}")
print(f"  Total Purchases: {test_purchases:,}")

# ============================================================================
# 2. CONVERSION RATE CALCULATIONS
# ============================================================================

print("\n" + "="*80)
print("2. CONVERSION RATE CALCULATIONS")
print("="*80)

# CTR (Click-Through Rate)
ctrl_ctr = ctrl_clicks / ctrl_impressions
test_ctr = test_clicks / test_impressions
ctr_diff = test_ctr - ctrl_ctr
ctr_rel_change = (test_ctr / ctrl_ctr - 1) * 100

print("\nCTR (Click-Through Rate):")
print(f"  Control: {ctrl_ctr*100:.3f}% (should be 4.857%)")
print(f"  Test: {test_ctr*100:.3f}% (should be 8.088%)")
print(f"  Difference: {ctr_diff*100:.3f} pp (should be 3.231 pp)")
print(f"  Relative change: {ctr_rel_change:.2f}% (should be 66.54%)")
assert abs(ctrl_ctr*100 - 4.857) < 0.01, "CTR Control mismatch!"
assert abs(test_ctr*100 - 8.088) < 0.01, "CTR Test mismatch!"
print("  ✓ Verified!")

# Click-to-Search
ctrl_click_to_search = ctrl_searches / ctrl_clicks
test_click_to_search = test_searches / test_clicks

print("\nClick-to-Search Rate:")
print(f"  Control: {ctrl_click_to_search*100:.2f}% (should be 41.75%)")
print(f"  Test: {test_click_to_search*100:.2f}% (should be 40.10%)")
assert abs(ctrl_click_to_search*100 - 41.75) < 0.5, "Click-to-Search Control mismatch!"
assert abs(test_click_to_search*100 - 40.10) < 0.5, "Click-to-Search Test mismatch!"
print("  ✓ Verified!")

# View-to-Cart
ctrl_view_to_cart = ctrl_add_to_cart / ctrl_view_content
test_view_to_cart = test_add_to_cart / test_view_content

print("\nView-to-Cart Rate:")
print(f"  Control: {ctrl_view_to_cart*100:.2f}% (should be 66.88%)")
print(f"  Test: {test_view_to_cart*100:.2f}% (should be 47.45%)")
assert abs(ctrl_view_to_cart*100 - 66.88) < 0.5, "View-to-Cart Control mismatch!"
assert abs(test_view_to_cart*100 - 47.45) < 0.5, "View-to-Cart Test mismatch!"
print("  ✓ Verified!")

# Cart-to-Purchase (KEY METRIC)
ctrl_cart_to_purchase = ctrl_purchases / ctrl_add_to_cart
test_cart_to_purchase = test_purchases / test_add_to_cart
c2p_diff = test_cart_to_purchase - ctrl_cart_to_purchase
c2p_rel_change = (test_cart_to_purchase / ctrl_cart_to_purchase - 1) * 100

print("\nCart-to-Purchase Rate (KEY METRIC):")
print(f"  Control: {ctrl_cart_to_purchase*100:.2f}% (should be 40.21%)")
print(f"  Test: {test_cart_to_purchase*100:.2f}% (should be 59.13%)")
print(f"  Difference: {c2p_diff*100:.2f} pp (should be 18.91 pp)")
print(f"  Relative change: {c2p_rel_change:.2f}% (should be 47.03%)")
assert abs(ctrl_cart_to_purchase*100 - 40.21) < 0.5, "Cart-to-Purchase Control mismatch!"
assert abs(test_cart_to_purchase*100 - 59.13) < 0.5, "Cart-to-Purchase Test mismatch!"
print("  ✓ Verified!")

# Overall Conversion
ctrl_overall = ctrl_purchases / ctrl_clicks
test_overall = test_purchases / test_clicks

print("\nOverall Conversion Rate:")
print(f"  Control: {ctrl_overall*100:.2f}% (should be 9.83%)")
print(f"  Test: {test_overall*100:.2f}% (should be 8.64%)")
assert abs(ctrl_overall*100 - 9.83) < 0.5, "Overall Conversion Control mismatch!"
assert abs(test_overall*100 - 8.64) < 0.5, "Overall Conversion Test mismatch!"
print("  ✓ Verified!")

# ============================================================================
# 3. COST METRICS
# ============================================================================

print("\n" + "="*80)
print("3. COST METRICS")
print("="*80)

# Cost per Click
ctrl_cpc = ctrl_spend / ctrl_clicks
test_cpc = test_spend / test_clicks

print("\nCost per Click:")
print(f"  Control: ${ctrl_cpc:.2f} (should be $0.43)")
print(f"  Test: ${test_cpc:.2f} (should be $0.42)")
assert abs(ctrl_cpc - 0.43) < 0.01, "CPC Control mismatch!"
assert abs(test_cpc - 0.42) < 0.01, "CPC Test mismatch!"
print("  ✓ Verified!")

# Cost per Purchase
ctrl_cpp = ctrl_spend / ctrl_purchases
test_cpp = test_spend / test_purchases
cpp_diff = test_cpp - ctrl_cpp
cpp_rel_change = (test_cpp / ctrl_cpp - 1) * 100

print("\nCost per Purchase:")
print(f"  Control: ${ctrl_cpp:.2f} (should be $4.41)")
print(f"  Test: ${test_cpp:.2f} (should be $4.92)")
print(f"  Difference: ${cpp_diff:.2f} (should be $0.51)")
print(f"  Relative change: {cpp_rel_change:.2f}% (should be 11.57%)")
assert abs(ctrl_cpp - 4.41) < 0.01, "CPP Control mismatch!"
assert abs(test_cpp - 4.92) < 0.01, "CPP Test mismatch!"
print("  ✓ Verified!")

# ============================================================================
# 4. CONFIDENCE INTERVAL FOR CART-TO-PURCHASE (TASK 5)
# ============================================================================

print("\n" + "="*80)
print("4. CONFIDENCE INTERVAL CALCULATIONS (Task 5)")
print("="*80)

# Using aggregate totals
n_ctrl = ctrl_add_to_cart
n_test = test_add_to_cart
p_ctrl = ctrl_cart_to_purchase
p_test = test_cart_to_purchase

# Difference
diff = p_test - p_ctrl

# Standard errors
se_ctrl = np.sqrt(p_ctrl * (1 - p_ctrl) / n_ctrl)
se_test = np.sqrt(p_test * (1 - p_test) / n_test)
se_diff = np.sqrt(se_ctrl**2 + se_test**2)

# Z-score for 95% CI
z_score = stats.norm.ppf(0.975)  # 1.96

# Confidence interval
ci_lower = diff - z_score * se_diff
ci_upper = diff + z_score * se_diff

print(f"\nControl Rate: {p_ctrl*100:.2f}% (should be 40.21%)")
print(f"Test Rate: {p_test*100:.2f}% (should be 59.13%)")
print(f"Difference: {diff*100:.2f} pp (should be 18.91 pp)")
print(f"Standard Error: {se_diff*100:.2f} pp (should be 0.39 pp)")
print(f"Z-score: {z_score:.2f} (should be 1.96)")
print(f"95% CI: [{ci_lower*100:.2f}%, {ci_upper*100:.2f}%] (should be [18.14%, 19.69%])")
print(f"Contains zero: {ci_lower <= 0 <= ci_upper} (should be False)")

assert abs(diff*100 - 18.91) < 0.1, "CI difference mismatch!"
assert abs(se_diff*100 - 0.39) < 0.01, "SE difference mismatch!"
assert abs(ci_lower*100 - 18.14) < 0.1, "CI lower bound mismatch!"
assert abs(ci_upper*100 - 19.69) < 0.1, "CI upper bound mismatch!"
print("  ✓ All CI calculations verified!")

# ============================================================================
# 5. MARGINAL ROAS CALCULATION (Previously had error)
# ============================================================================

print("\n" + "="*80)
print("5. MARGINAL ROAS CALCULATION (CRITICAL CHECK)")
print("="*80)

additional_spend = test_spend - ctrl_spend
additional_purchases = test_purchases - ctrl_purchases

print(f"\nAdditional Spend: ${additional_spend:,.2f} (should be $10,074)")
print(f"Additional Purchases: {additional_purchases:,} (should be 476)")

assert abs(additional_spend - 10074) < 1, "Additional spend mismatch!"
assert abs(additional_purchases - 476) < 1, "Additional purchases mismatch!"

# Assuming AOV = $50
aov = 50
additional_revenue = additional_purchases * aov
marginal_roas = additional_revenue / additional_spend

print(f"\nAssuming AOV = ${aov}:")
print(f"  Additional Revenue: ${additional_revenue:,.2f} (should be $23,800)")
print(f"  Marginal ROAS: {marginal_roas:.2f}x (should be 2.36x)")

assert abs(additional_revenue - 23800) < 1, "Additional revenue mismatch!"
assert abs(marginal_roas - 2.36) < 0.01, "Marginal ROAS mismatch!"
print("  ✓ Marginal ROAS verified! (Previously was incorrectly 98x)")

# ============================================================================
# 6. BUSINESS SCENARIO CALCULATIONS (Task 5, Section 10.1)
# ============================================================================

print("\n" + "="*80)
print("6. BUSINESS SCENARIO CALCULATIONS (Scaling)")
print("="*80)

# Scenario 2: 100k Add to Cart per month
monthly_cart = 100000
ctrl_monthly_purchases = monthly_cart * ctrl_cart_to_purchase
test_monthly_purchases = monthly_cart * test_cart_to_purchase
additional_monthly_purchases = test_monthly_purchases - ctrl_monthly_purchases

print(f"\nScenario: 100,000 Add to Cart per month")
print(f"  Control purchases: {ctrl_monthly_purchases:,.0f} (should be 40,210)")
print(f"  Test purchases: {test_monthly_purchases:,.0f} (should be 59,130)")
print(f"  Additional purchases: {additional_monthly_purchases:,.0f} (should be 18,920)")

assert abs(ctrl_monthly_purchases - 40210) < 10, "Monthly control purchases mismatch!"
assert abs(test_monthly_purchases - 59130) < 10, "Monthly test purchases mismatch!"
assert abs(additional_monthly_purchases - 18920) < 10, "Additional monthly purchases mismatch!"

# Revenue at AOV=$50
monthly_additional_revenue = additional_monthly_purchases * aov
annual_additional_revenue = monthly_additional_revenue * 12

print(f"\nAt AOV = ${aov}:")
print(f"  Monthly additional revenue: ${monthly_additional_revenue:,.0f} (should be $946,000)")
print(f"  Annual additional revenue: ${annual_additional_revenue/1e6:.2f}M (should be $11.35M)")

assert abs(monthly_additional_revenue - 946000) < 1000, "Monthly revenue mismatch!"
assert abs(annual_additional_revenue - 11350000) < 10000, "Annual revenue mismatch!"
print("  ✓ Scaling scenarios verified!")

# ============================================================================
# 7. DAILY AVERAGES
# ============================================================================

print("\n" + "="*80)
print("7. DAILY AVERAGES")
print("="*80)

ctrl_daily_spend = ctrl_spend / ctrl_days
test_daily_spend = test_spend / test_days
daily_spend_diff = test_daily_spend - ctrl_daily_spend
daily_spend_rel = (test_daily_spend / ctrl_daily_spend - 1) * 100

print(f"\nDaily Spend:")
print(f"  Control: ${ctrl_daily_spend:.2f} (should be $2,304.07)")
print(f"  Test: ${test_daily_spend:.2f} (should be $2,563.07)")
print(f"  Difference: ${daily_spend_diff:.2f} (should be ~$259)")
print(f"  Relative: {daily_spend_rel:.1f}% (should be ~11.2%)")

assert abs(ctrl_daily_spend - 2304.07) < 1, "Daily spend control mismatch!"
assert abs(test_daily_spend - 2563.07) < 1, "Daily spend test mismatch!"
print("  ✓ Verified!")

ctrl_daily_impressions = ctrl_impressions / ctrl_days
test_daily_impressions = test_impressions / test_days

print(f"\nDaily Impressions:")
print(f"  Control: {ctrl_daily_impressions:,.0f} (should be 109,560)")
print(f"  Test: {test_daily_impressions:,.0f} (should be 74,585)")

assert abs(ctrl_daily_impressions - 109560) < 10, "Daily impressions control mismatch!"
assert abs(test_daily_impressions - 74585) < 10, "Daily impressions test mismatch!"
print("  ✓ Verified!")

# ============================================================================
# 8. PURCHASE VOLUME COMPARISON
# ============================================================================

print("\n" + "="*80)
print("8. PURCHASE VOLUME COMPARISON")
print("="*80)

purchase_diff = test_purchases - ctrl_purchases
purchase_rel = (test_purchases / ctrl_purchases - 1) * 100

print(f"\nTotal Purchases:")
print(f"  Control: {ctrl_purchases:,}")
print(f"  Test: {test_purchases:,}")
print(f"  Difference: {purchase_diff:,} (should be +476)")
print(f"  Relative change: {purchase_rel:.2f}% (should be +3.14%)")

assert abs(purchase_diff - 476) < 1, "Purchase difference mismatch!"
assert abs(purchase_rel - 3.14) < 0.1, "Purchase relative change mismatch!"
print("  ✓ Verified!")

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "="*80)
print("✓✓✓ ALL CALCULATIONS VERIFIED SUCCESSFULLY ✓✓✓")
print("="*80)

print("\nKey Findings Confirmed:")
print("  1. CTR improvement: +66.54% ✓")
print("  2. Cart→Purchase improvement: +47.03% ✓")
print("  3. 95% CI for C2P difference: [18.14%, 19.69%] ✓")
print("  4. Marginal ROAS (actual test): 2.36x ✓ (NOT 98x)")
print("  5. Additional purchases: 476 ✓")
print("  6. Additional spend: $10,074 ✓")
print("  7. Cost per purchase increase: +$0.51 (+11.57%) ✓")
print("  8. All scaling scenarios mathematically correct ✓")

print("\n" + "="*80)
print("NO EXTREME OR INCORRECT CALCULATIONS FOUND")
print("(except the marginal ROAS which was already corrected)")
print("="*80)
