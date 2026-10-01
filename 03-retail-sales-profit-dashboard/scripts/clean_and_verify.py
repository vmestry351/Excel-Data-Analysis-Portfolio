"""Reproduce the Power Query cleaning in pandas and reconcile it to the workbook.

Run from the repo folder:   python scripts/clean_and_verify.py
Needs: pandas, openpyxl
Writes data/clean/Sales_Clean.csv and prints a reconciliation table.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
files = sorted((ROOT / "data" / "raw").glob("Sales_2025-*.csv"))
assert len(files) == 12, f"expected 12 monthly files, found {len(files)}"

# 1. Combine the 12 files (everything as text so nothing is silently changed)
raw = pd.concat([pd.read_csv(f, encoding="utf-8-sig", dtype=str, keep_default_na=False) for f in files],
                ignore_index=True)

# 2. Planted issues 1 to 3: trim + proper-case names and region, standardise Returned
df = raw.copy()
for col in ("Customer Name", "Region"):
    df[col] = df[col].str.strip().str.title()
df["Returned"] = df["Returned"].str.strip().replace({"Yes": "Y", "No": "N"})

# 3. Planted issue 4: exact duplicate rows
clean = df.drop_duplicates().reset_index(drop=True)

# 4. Types
for col in ("Order Date", "Ship Date"):
    clean[col] = pd.to_datetime(clean[col])
for col in ("Qty", "Unit Price (₹)", "Discount", "Sales (₹)", "Cost (₹)", "Profit (₹)"):
    clean[col] = pd.to_numeric(clean[col])

out = ROOT / "data" / "clean" / "Sales_Clean.csv"
clean.to_csv(out, index=False, encoding="utf-8-sig", date_format="%Y-%m-%d")

report = {
    "Rows before cleaning": len(raw),
    "Duplicate rows removed": len(df) - len(clean),
    "Rows after cleaning": len(clean),
    "Total Sales (Rs)": int(clean["Sales (₹)"].sum()),
    "Distinct Customer Names": clean["Customer Name"].nunique(),
    "Distinct Regions": clean["Region"].nunique(),
    "Returned = Y": int((clean["Returned"] == "Y").sum()),
}
print("Reconciliation")
for k, v in report.items():
    print(f"  {k:<26}{v:>12,}")

expected = {"Rows before cleaning": 1210, "Duplicate rows removed": 10, "Rows after cleaning": 1200,
            "Total Sales (Rs)": 5426671, "Distinct Customer Names": 220, "Distinct Regions": 4, "Returned = Y": 48}
assert report == expected, "Cleaned data does not match the expected control totals"

# 5. Compare cell by cell with the 'Sales Data' sheet of the workbook, if present
book = ROOT / "Retail_Sales_Profit_Dashboard.xlsx"
if book.exists():
    sheet = pd.read_excel(book, sheet_name="Sales Data").iloc[:, :19]   # first 19 columns = original data
    match = sheet.shape == clean.shape and bool((sheet.astype(str).values == clean.astype(str).values).all())
    print(f"  Matches 'Sales Data' sheet: {'YES' if match else 'NO':>7}")
    assert match, "Sales_Clean.csv differs from the Sales Data sheet"
print("All checks passed. Wrote", out.relative_to(ROOT))
