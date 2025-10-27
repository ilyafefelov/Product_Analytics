import pandas as pd
import matplotlib.pyplot as plt
import shutil
from pathlib import Path

# Налаштування шляхів
BASE_DIR = Path(__file__).resolve().parent
INPUT_PATH = BASE_DIR / "data_input.csv"
OUTPUT_PATH = BASE_DIR / "results.xlsx"
FINAL_OUTPUT_PATH = BASE_DIR / "Fefelov_PA_assignment_1.xlsx"
PLOT_HISTOGRAM = BASE_DIR / "histogram.png"
PLOT_BOXPLOT = BASE_DIR / "boxplot.png"


def build_interpretation(mean_val: float, median_val: float, mode_text: str, std_val: float) -> str:
    """Формує коротке текстове пояснення для менеджера."""
    diff = mean_val - median_val
    if abs(diff) <= 0.1:
        balance = "Середнє практично дорівнює медіані — розподіл симетричний."  # noqa: E501
    elif diff > 0:
        balance = (
            "Середнє вище за медіану, отже розподіл зміщений вправо через великі значення."  # noqa: E501
        )
    else:
        balance = (
            "Середнє нижче за медіану, отже розподіл зміщений вліво через малі значення."  # noqa: E501
        )

    if mode_text:
        mode_phrase = f"Мода: {mode_text}."
    else:
        mode_phrase = "Мода відсутня — усі значення зустрічаються однаково часто."

    cv = std_val / mean_val if mean_val != 0 else float("nan")
    if pd.isna(cv):
        dispersion = "Стандартне відхилення не можна нормалізувати через нульове середнє."
    elif cv < 0.1:
        dispersion = (
            f"Стандартне відхилення {std_val:.2f} (коефіцієнт варіації {cv:.1%}) свідчить про дуже стабільні дані."  # noqa: E501
        )
    elif cv < 0.3:
        dispersion = (
            f"Стандартне відхилення {std_val:.2f} (коефіцієнт варіації {cv:.1%}) відповідає помірній варіативності."  # noqa: E501
        )
    else:
        dispersion = (
            f"Стандартне відхилення {std_val:.2f} (коефіцієнт варіації {cv:.1%}) вказує на значні коливання показників."  # noqa: E501
        )

    return " ".join([balance, mode_phrase, dispersion])


# Завантаження даних
raw_df = pd.read_csv(INPUT_PATH)
raw_df = raw_df.sort_values(["dataset", "value"]).reset_index(drop=True)

# Розрахунок метрик для кожного датасету
metrics = []
interpretations = []
for dataset_name, group in raw_df.groupby("dataset"):
    values = group["value"].astype(float)
    mean_val = values.mean()
    median_val = values.median()
    mode_values = values.mode().tolist()
    if len(mode_values) == len(values):
        mode_text = ""
    else:
        mode_text = ", ".join(map(str, mode_values))
    std_val = values.std(ddof=0)
    metric_row = {
        "dataset": dataset_name,
        "count": len(values),
        "mean": mean_val,
        "median": median_val,
        "mode": mode_text,
        "variance": values.var(ddof=0),  # дисперсія генеральної сукупності
        "std_dev": std_val,
        "coef_of_variation": std_val / mean_val if mean_val != 0 else float("nan"),
    }
    metrics.append(metric_row)
    interpretations.append(
        {
            "dataset": dataset_name,
            "human_readable_summary": build_interpretation(mean_val, median_val, mode_text, std_val),
        }
    )

metrics_df = pd.DataFrame(metrics).rename(
    columns={
        "dataset": "Dataset",
        "count": "Кількість спостережень",
        "mean": "Середнє значення",
        "median": "Медіана",
        "mode": "Мода",
        "variance": "Дисперсія (σ²)",
        "std_dev": "Стандартне відхилення (σ)",
        "coef_of_variation": "Коефіцієнт варіації",
    }
)

summary_df = pd.DataFrame(interpretations).rename(
    columns={
        "dataset": "Dataset",
        "human_readable_summary": "Пояснення для менеджера",
    }
)

# Експорт до Excel з окремими аркушами та форматуванням для зручності читання
with pd.ExcelWriter(OUTPUT_PATH, engine="xlsxwriter") as writer:
    raw_df.to_excel(writer, sheet_name="data", index=False)
    metrics_df.to_excel(writer, sheet_name="metrics", index=False)
    summary_df.to_excel(writer, sheet_name="summary", index=False)

    workbook = writer.book

    header_fmt = workbook.add_format({"bold": True, "bg_color": "#D9E1F2", "border": 1})
    number_fmt = workbook.add_format({"num_format": "#,##0.00", "border": 1})
    percent_fmt = workbook.add_format({"num_format": "0.0%", "border": 1})
    text_fmt = workbook.add_format({"text_wrap": True, "valign": "top", "border": 1})

    # Форматування аркуша з метриками
    metrics_sheet = writer.sheets["metrics"]
    metrics_sheet.freeze_panes(1, 0)
    metrics_sheet.set_column("A:A", 14, text_fmt)
    metrics_sheet.set_column("B:B", 20, number_fmt)
    metrics_sheet.set_column("C:E", 18, number_fmt)
    metrics_sheet.set_column("F:F", 20, number_fmt)
    metrics_sheet.set_column("G:G", 28, number_fmt)
    metrics_sheet.set_column("H:H", 22, percent_fmt)
    metrics_sheet.set_row(0, None, header_fmt)

    # Форматування аркуша з даними
    data_sheet = writer.sheets["data"]
    data_sheet.freeze_panes(1, 0)
    data_sheet.set_column("A:A", 12, text_fmt)
    data_sheet.set_column("B:B", 12, number_fmt)
    data_sheet.set_row(0, None, header_fmt)

    # Форматування аркуша з поясненнями
    summary_sheet = writer.sheets["summary"]
    summary_sheet.freeze_panes(1, 0)
    summary_sheet.set_column("A:A", 12, text_fmt)
    summary_sheet.set_column("B:B", 80, text_fmt)
    summary_sheet.set_row(0, None, header_fmt)

# Копіювання файлу для здачі
shutil.copyfile(OUTPUT_PATH, FINAL_OUTPUT_PATH)

# Генерація візуалізацій
plt.style.use('seaborn-v0_8-darkgrid')

# Гістограми для кожного датасету
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
fig.suptitle('Розподіл значень по датасетам', fontsize=14, fontweight='bold')

for idx, (dataset_name, group) in enumerate(raw_df.groupby("dataset")):
    values = group["value"].astype(float)
    axes[idx].hist(values, bins=10, color='steelblue', edgecolor='black', alpha=0.7)
    axes[idx].set_title(f'{dataset_name}', fontsize=12)
    axes[idx].set_xlabel('Значення', fontsize=10)
    axes[idx].set_ylabel('Частота', fontsize=10)
    axes[idx].axvline(values.mean(), color='red', linestyle='--', linewidth=2, label=f'Середнє: {values.mean():.2f}')
    axes[idx].axvline(values.median(), color='green', linestyle='--', linewidth=2, label=f'Медіана: {values.median():.2f}')
    axes[idx].legend(fontsize=8)
    axes[idx].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(PLOT_HISTOGRAM, dpi=300, bbox_inches='tight')
plt.close()

# Boxplot для порівняння датасетів
fig, ax = plt.subplots(figsize=(10, 6))
datasets_list = []
labels_list = []

for dataset_name, group in raw_df.groupby("dataset"):
    datasets_list.append(group["value"].astype(float).tolist())
    labels_list.append(dataset_name)

bp = ax.boxplot(datasets_list, tick_labels=labels_list, patch_artist=True,
                showmeans=True, meanline=True,
                boxprops=dict(facecolor='lightblue', edgecolor='black', linewidth=1.5),
                medianprops=dict(color='red', linewidth=2),
                meanprops=dict(color='green', linestyle='--', linewidth=2),
                whiskerprops=dict(color='black', linewidth=1.5),
                capprops=dict(color='black', linewidth=1.5),
                flierprops=dict(marker='o', markerfacecolor='red', markersize=8, linestyle='none'))

ax.set_title('Порівняння розподілів датасетів (Boxplot)', fontsize=14, fontweight='bold')
ax.set_ylabel('Значення', fontsize=12)
ax.set_xlabel('Dataset', fontsize=12)
ax.grid(True, alpha=0.3, axis='y')

# Додаємо легенду
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color='red', linewidth=2, label='Медіана'),
    Line2D([0], [0], color='green', linestyle='--', linewidth=2, label='Середнє'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=8, label='Викиди')
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=10)

plt.tight_layout()
plt.savefig(PLOT_BOXPLOT, dpi=300, bbox_inches='tight')
plt.close()

if __name__ == "__main__":
    print("Результати збережено до:", OUTPUT_PATH)
    print("Файл для здачі збережено до:", FINAL_OUTPUT_PATH)
    print("Гістограми збережено до:", PLOT_HISTOGRAM)
    print("Boxplot збережено до:", PLOT_BOXPLOT)
