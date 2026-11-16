import sys, openpyxl, warnings
warnings.filterwarnings("ignore")
wb = openpyxl.load_workbook(sys.argv[1], read_only=True, data_only=True)
for ws in wb.worksheets:
    print("### sheet", ws.title)
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        if i > int(sys.argv[2]) if len(sys.argv) > 2 else 60: break
        if any(v is not None for v in row):
            print(i, " | ".join("" if v is None else str(v) for v in row)[:300])
