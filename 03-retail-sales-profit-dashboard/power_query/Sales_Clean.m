// Sales_Clean: merge and clean the 12 monthly CSV files
// How to use: Excel > Data > Get Data > From Other Sources > Blank Query > Advanced Editor,
// paste this script, change FolderPath, click Done, then Home > Close & Load To... > Connection + Table.
// Name the query Sales_Clean.
let
    // 1. Folder that holds Sales_2025-01.csv ... Sales_2025-12.csv  (CHANGE THIS PATH)
    FolderPath = "C:\Users\YourName\Excel-Data-Analysis-Portfolio\03-retail-sales-profit-dashboard\data\raw",

    // 2. Read every CSV in the folder and stack them (1,210 rows)
    Source     = Folder.Files(FolderPath),
    CsvFiles   = Table.SelectRows(Source, each Text.EndsWith([Name], ".csv")),
    Parsed     = Table.AddColumn(CsvFiles, "Data", each
                    Table.PromoteHeaders(
                        Csv.Document([Content], [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
                        [PromoteAllScalars = true])),
    Combined   = Table.Combine(Parsed[Data]),

    // 3. Planted issues 1 to 3: names, region and the Returned flag
    CleanedText = Table.TransformColumns(Combined, {
        {"Customer Name", each Text.Proper(Text.Trim(_)), type text},
        {"Region",        each Text.Proper(Text.Trim(_)), type text},
        {"Returned",      each let t = Text.Upper(Text.Trim(_)) in
                              if t = "YES" then "Y" else if t = "NO" then "N" else t, type text}
    }),

    // 4. Correct data types
    ChangedType = Table.TransformColumnTypes(CleanedText, {
        {"Order Date", type date}, {"Ship Date", type date},
        {"Qty", Int64.Type}, {"Unit Price (₹)", type number}, {"Discount", type number},
        {"Sales (₹)", type number}, {"Cost (₹)", type number}, {"Profit (₹)", type number}
    }, "en-US"),

    // 5. Planted issue 4: exact duplicate rows (all columns) -> 1,200 rows
    RemovedDuplicates = Table.Distinct(ChangedType)
in
    RemovedDuplicates
