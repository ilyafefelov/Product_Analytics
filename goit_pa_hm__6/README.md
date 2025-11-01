# PA Assignment 6 — LTV Cohort Heatmap (Excel)

This folder contains the final deliverable for Assignment 6.

## Files
- `Fefelov_PA_assignment_6.xlsx` — Excel workbook with two heatmap tabs:
  - `Cohort_LTV_by_Age`: cumulative LTV per customer by cohort age (Y0, Y1, ...)
  - `Cohort_LTV_by_Year`: cumulative LTV per customer by calendar year
- `Fefelov_PA_assignment_6_by_age.png` — quick PNG snapshot of the age heatmap
- `Fefelov_PA_assignment_6_by_year.png` — quick PNG snapshot of the calendar-year heatmap
- `generate_ltv_cohort.py` — script used to generate the Excel and PNGs

## Cohort and Metric
- Cohort = quarter of first purchase (YYYY-Q#)
- LTV = cumulative Sales per acquired customer in cohort

## Re-run (optional)
If you need to regenerate the Excel/PNGs:

```powershell
python "goit_pa_hm__6/generate_ltv_cohort.py" --input "goit_pa_hm_3/Sample - Superstore.xls" --out "Fefelov_PA_assignment_6.xlsx"
```

Output will be written into `goit_pa_hm__6/`.

## Submission notes
- Upload `Fefelov_PA_assignment_6.xlsx` to LMS (and optionally add the PNG as a preview).
- Also upload it to Google Drive and share a view link.
