import math
from dataclasses import dataclass
from typing import Tuple

import pandas as pd
import xlwt

Z_95 = 1.96


def ci_wald(p_hat: float, n: int, z: float = Z_95) -> Tuple[float, float, float, float]:
    """
    Wald 95% CI for a single proportion.
    Returns: (lower, upper, se, margin)
    """
    se = math.sqrt(p_hat * (1 - p_hat) / n)
    margin = z * se
    lower = max(0.0, p_hat - margin)
    upper = min(1.0, p_hat + margin)
    return lower, upper, se, margin


def norm_cdf(z: float) -> float:
    """Standard normal CDF using math.erf."""
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def two_proportion_z_test(p_a: float, n_a: int, p_b: float, n_b: int):
    """
    Two-proportion z-test (H0: p_a == p_b). Returns dict with pooled SE, z, p-value, diff, and CI for diff (unpooled).
    """
    x_a = int(round(p_a * n_a))
    x_b = int(round(p_b * n_b))

    p_pool = (x_a + x_b) / (n_a + n_b)
    se_pooled = math.sqrt(p_pool * (1 - p_pool) * (1 / n_a + 1 / n_b))
    diff = p_b - p_a
    z = diff / se_pooled if se_pooled > 0 else float("inf")
    # two-sided p-value
    p_value = 2 * (1 - norm_cdf(abs(z)))

    # 95% CI for difference using unpooled SE
    se_unpooled = math.sqrt(p_a * (1 - p_a) / n_a + p_b * (1 - p_b) / n_b)
    margin = Z_95 * se_unpooled
    ci_diff_lower = diff - margin
    ci_diff_upper = diff + margin

    return {
        "x_a": x_a,
        "x_b": x_b,
        "p_pool": p_pool,
        "se_pooled": se_pooled,
        "z": z,
        "p_value_two_sided": p_value,
        "diff_b_minus_a": diff,
        "se_unpooled": se_unpooled,
        "ci_diff_lower": ci_diff_lower,
        "ci_diff_upper": ci_diff_upper,
    }


def main():
    # Task 1 inputs
    p_hat = 0.45
    n = 8000

    ci1_low, ci1_up, se1, margin1 = ci_wald(p_hat, n)

    df_task1 = pd.DataFrame(
        [
            {
                "Metric": "Observed conversion (p_hat)",
                "Value": p_hat,
            },
            {
                "Metric": "Sample size (n)",
                "Value": n,
            },
            {
                "Metric": "Z (95%)",
                "Value": Z_95,
            },
            {
                "Metric": "Std. error",
                "Value": se1,
            },
            {
                "Metric": "Margin",
                "Value": margin1,
            },
            {
                "Metric": "CI 95% lower",
                "Value": ci1_low,
            },
            {
                "Metric": "CI 95% upper",
                "Value": ci1_up,
            },
            {
                "Metric": "CI 95% lower (%)",
                "Value": ci1_low * 100,
            },
            {
                "Metric": "CI 95% upper (%)",
                "Value": ci1_up * 100,
            },
        ]
    )

    # Task 2 inputs
    p_a = 0.55
    n_a = 12000
    p_b = 0.58
    n_b = 12000

    res2 = two_proportion_z_test(p_a, n_a, p_b, n_b)

    # Build a symmetric overview table for A and B in one sheet
    df_task2_overview = pd.DataFrame(
        [
            {"Metric": "p_hat", "A": p_a, "B": p_b},
            {"Metric": "n", "A": n_a, "B": n_b},
            {"Metric": "successes (x)", "A": res2["x_a"], "B": res2["x_b"]},
        ]
    )

    df_task2_stats = pd.DataFrame(
        [
            {"Stat": "Pooled proportion", "Value": res2["p_pool"]},
            {"Stat": "SE (pooled)", "Value": res2["se_pooled"]},
            {"Stat": "z-statistic", "Value": res2["z"]},
            {"Stat": "p-value (two-sided)", "Value": res2["p_value_two_sided"]},
            {"Stat": "Difference (B - A)", "Value": res2["diff_b_minus_a"]},
            {"Stat": "SE (unpooled)", "Value": res2["se_unpooled"]},
            {"Stat": "95% CI lower (diff)", "Value": res2["ci_diff_lower"]},
            {"Stat": "95% CI upper (diff)", "Value": res2["ci_diff_upper"]},
            {"Stat": "95% CI lower (%)", "Value": res2["ci_diff_lower"] * 100},
            {"Stat": "95% CI upper (%)", "Value": res2["ci_diff_upper"] * 100},
        ]
    )

    notes_rows = [
        [
            "Task 1: Wald CI for a single proportion: p_hat +/- 1.96 * sqrt(p_hat*(1-p_hat)/n).",
        ],
        [
            "Task 2: Two-proportion z-test with pooled SE under H0: p_A = p_B.",
        ],
        [
            "95% CI for difference uses unpooled SE: sqrt(p_A*(1-p_A)/n_A + p_B*(1-p_B)/n_B).",
        ],
        [
            "All values are reported both in proportions and percentage points for clarity.",
        ],
    ]
    df_notes = pd.DataFrame(notes_rows, columns=["Notes"])

    out_path = "Fefelov_PA_assignment_7.xls"
    wb = xlwt.Workbook()

    # Write Task1
    sh1 = wb.add_sheet("Task1")
    headers1 = ["Metric", "Value"]
    for c, h in enumerate(headers1):
        sh1.write(0, c, h)
    for r, row in enumerate(df_task1.to_dict(orient="records"), start=1):
        sh1.write(r, 0, row["Metric"])
        sh1.write(r, 1, row["Value"])

    # Write Task2_Overview
    sh2 = wb.add_sheet("Task2_Overview")
    headers2 = ["Metric", "A", "B"]
    for c, h in enumerate(headers2):
        sh2.write(0, c, h)
    for r, row in enumerate(df_task2_overview.to_dict(orient="records"), start=1):
        sh2.write(r, 0, row.get("Metric", ""))
        sh2.write(r, 1, row.get("A", ""))
        sh2.write(r, 2, row.get("B", ""))

    # Write Task2_Stats
    sh3 = wb.add_sheet("Task2_Stats")
    headers3 = ["Stat", "Value"]
    for c, h in enumerate(headers3):
        sh3.write(0, c, h)
    for r, row in enumerate(df_task2_stats.to_dict(orient="records"), start=1):
        sh3.write(r, 0, row["Stat"])
        sh3.write(r, 1, row["Value"])

    # Write README/Notes
    sh4 = wb.add_sheet("README")
    sh4.write(0, 0, "Notes")
    for r, row in enumerate(df_notes["Notes"].tolist(), start=1):
        sh4.write(r, 0, row)

    wb.save(out_path)

    # Console summary
    print("Task 1: 95% CI for conversion (p=0.45, n=8000)")
    print(f"SE={se1:.6f}, margin={margin1:.6f}, CI=({ci1_low:.4f}, {ci1_up:.4f}) -> ({ci1_low*100:.2f}%, {ci1_up*100:.2f}%)")

    print("\nTask 2: Two-proportion z-test (A: 0.55, n=12000 vs B: 0.58, n=12000)")
    print(
        f"z={res2['z']:.4f}, p-value={res2['p_value_two_sided']:.6g}, diff={res2['diff_b_minus_a']:.4f}\n"
        f"95% CI for diff=({res2['ci_diff_lower']:.4f}, {res2['ci_diff_upper']:.4f}) -> "
        f"({res2['ci_diff_lower']*100:.2f} pp, {res2['ci_diff_upper']*100:.2f} pp)"
    )


if __name__ == "__main__":
    main()
