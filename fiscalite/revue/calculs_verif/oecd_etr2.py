import csv, sys, statistics as st
O = "AUS AUT BEL CAN CHL COL CRI CZE DNK EST FIN FRA DEU GRC HUN ISL IRL ISR ITA JPN KOR LVA LTU LUX MEX NLD NZL NOR POL PRT SVK SVN ESP SWE CHE TUR GBR USA".split()
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
def get(measure, scen, asset):
    return {r["REF_AREA"]: float(r["OBS_VALUE"]) for r in rows if r["MEASURE"]==measure and r["ETR_SCENARIO"]==scen
            and r["ETR_TAX_TYPE"]==asset and r["OBS_VALUE"]!="" and r["REF_AREA"] in O}
for scen in ("FIXED","CS"):
  for m in ("EATR","EMTR"):
    for a in ("COMPOSITE","TAN","NRS","AWS","INV"):
        d = get(m,scen,a)
        if "FRA" in d:
            rk = sorted(d.values(), reverse=True).index(d["FRA"])+1
            print(scen,m,a,"FRA %.2f moy %.2f n %d rang %d | DEU %.1f GBR %.1f USA %.1f ITA %.1f ESP %.1f IRL %.1f" % (
                d["FRA"], st.mean(d.values()), len(d), rk, d["DEU"], d["GBR"], d["USA"], d["ITA"], d["ESP"], d["IRL"]))
