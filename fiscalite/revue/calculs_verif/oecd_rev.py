import csv, sys, statistics as st
O = "AUS AUT BEL CAN CHL COL CRI CZE DNK EST FIN FRA DEU GRC HUN ISL IRL ISR ITA JPN KOR LVA LTU LUX MEX NLD NZL NOR POL PRT SVK SVN ESP SWE CHE TUR GBR USA".split()
for f in sys.argv[1:]:
    r = list(csv.DictReader(open(f, encoding="utf-8")))
    print(f.split("/")[-1], len(r), r[0].get("Unit of measure") if r else "")
    for y in ("2019", "2021", "2022", "2023", "2024"):
        d = {x["REF_AREA"]: float(x["OBS_VALUE"]) for x in r if x["TIME_PERIOD"] == y and x["OBS_VALUE"] and x["REF_AREA"] in O}
        if "FRA" in d and len(d) > 20:
            rk = sorted(d.values(), reverse=True).index(d["FRA"]) + 1
            print(f"  {y} FRA {d['FRA']:.2f} moy {st.mean(d.values()):.2f} med {st.median(d.values()):.2f} n {len(d)} rang {rk} | "
                  + " ".join(f"{c} {d.get(c, float('nan')):.1f}" for c in ("DEU", "ITA", "ESP", "GBR", "USA", "NLD", "BEL", "IRL")))
