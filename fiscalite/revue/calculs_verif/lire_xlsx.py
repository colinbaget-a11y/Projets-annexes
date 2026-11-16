import sys, openpyxl
p = sys.argv[1]
pat = [s.lower() for s in sys.argv[2:]]
wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
for ws in wb.worksheets:
    print("### sheet", ws.title)
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        txt = " | ".join("" if v is None else str(v) for v in row)
        if i < 6 or any(s in txt.lower() for s in pat):
            print(i, txt[:400])
