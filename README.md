# Excel Data Analysis Portfolio

Hi, I'm Vinayak M. This repo collects the Excel projects I've built while learning data analysis. Each project has its own folder with the workbook and a short write-up of how I did it.

**Skills shown:** data cleaning, SUMIFS / COUNTIFS, TRIM / PROPER, IF logic, RANK, INDEX / MATCH, conditional formatting, charts, summary reports.

---

## Projects

| # | Project | What it covers | Files |
|---|---------|----------------|-------|
| 1 | [Café Sales Analysis](01-cafe-sales-analysis) | Cleaning 170 messy order rows and finding where a café loses money | [Workbook](01-cafe-sales-analysis/Cafe_Sales_Analysis_Project.xlsx) · [Method (PDF)](01-cafe-sales-analysis/Cafe_Sales_Analysis_Method.pdf) |

More projects will be added here.

---

## Project 1: Café Sales Analysis

<!-- Add a screenshot of the Summary sheet to 01-cafe-sales-analysis/screenshots/ and uncomment the line below -->
<!-- ![Summary sheet](01-cafe-sales-analysis/screenshots/summary.png) -->

**Data:** 160 café orders (March 2026) across Bengaluru, Chennai, Delhi, Mumbai and Pune.

**Questions I wanted to answer**
- Which city earns the most?
- How much money is lost to cancelled and refunded orders?
- Which payment method do customers prefer?

**What I did**
1. Removed 10 duplicate orders (170 rows down to 160).
2. Fixed spelling, spacing and capital letters in city, customer and status using `TRIM(PROPER())`.
3. Flagged 21 orders with a missing or invalid quantity or price and counted them as ₹0.
4. Added calculated columns: sales value, order size and whether the order counted as a sale.
5. Built summary tables with `SUMIFS` and `COUNTIFS`, plus a formula-based pivot of city by status.
6. Added four charts and a findings section on the Summary sheet.

**What I found**
- Total sales were ₹46,500, but only ₹32,990 (71%) was kept from completed orders.
- Pune is the strongest city and loses the least (15%).
- Mumbai sells the most on paper but drops to #2 after cancellations and refunds.
- Chennai is the problem: 58% of its sales are lost, against 29% overall.
- Beverages bring in about two thirds of kept sales.

**Recommendation:** find out why Chennai orders fail (payments, delays or stock) and see what Pune does differently.

---

## Contact

- LinkedIn: [https://www.linkedin.com/in/vinayak-sunil-mestry-953568386/]
- Email: [vmestry351@gmail.com]
