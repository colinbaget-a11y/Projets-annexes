import csv, sys, statistics as st, collections
O = "AUS AUT BEL CAN CHL COL CRI CZE DNK EST FIN FRA DEU GRC HUN ISL IRL ISR ITA JPN KOR LVA LTU LUX MEX NLD NZL NOR POL PRT SVK SVN ESP SWE CHE TUR GBR USA".split()
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
combos = collections.Counter((r["MEASURE"],r["TARGETING"],r["SECTOR"],r["DIV_TREATMENT"],r["RATE_STRUCTURE"],r["TAX_BASE"]) for r in rows if r["REF_AREA"]=="FRA")
for c,n in combos.most_common(12): print(n,c)
for meas in ("CIT_C",):
  for y in ("2022","2024","2025","2026"):
    d = {r["REF_AREA"]: float(r["OBS_VALUE"]) for r in rows if r["MEASURE"]==meas and r["TARGETING"]=="ST" and r["TIME_PERIOD"]==y and r["REF_AREA"] in O and r["OBS_VALUE"]}
    if "FRA" in d:
        rk = sorted(d.values(), reverse=True).index(d["FRA"])+1
        top = sorted(d.items(), key=lambda kv:-kv[1])[:5]
        print(meas, y, "FRA", d["FRA"], "moy %.2f med %.2f n %d rang %d" % (st.mean(d.values()), st.median(d.values()), len(d), rk), top, "DEU",d.get("DEU"),"ITA",d.get("ITA"),"ESP",d.get("ESP"),"GBR",d.get("GBR"),"USA",d.get("USA"),"NLD",d.get("NLD"),"BEL",d.get("BEL"))
