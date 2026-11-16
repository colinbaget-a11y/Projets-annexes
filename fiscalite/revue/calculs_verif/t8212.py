import sys, openpyxl, warnings
warnings.filterwarnings("ignore")
wb = openpyxl.load_workbook(sys.argv[1], read_only=True, data_only=True)
ws = wb["T_8212"]
rows = list(ws.iter_rows(values_only=True))
years, ops = rows[3], rows[4]
want = {"N113","N1131","N1132","N1139","N111","N112","N1121","N1122","N117","N11","N1171","N1173"}
for r in rows[5:]:
    if r[0] in want:
        out=[]
        for j,(y,o) in enumerate(zip(years,ops)):
            if str(y) in ("2019","2022","2023","2024","2025") and j>1:
                out.append(f"{y}:{str(o)[:12]}={r[j]}")
        print(r[0], r[1].strip()); print("   ", "; ".join(out))
