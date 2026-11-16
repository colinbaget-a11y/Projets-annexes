import csv, sys, statistics as st
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
def get(measure, scen, asset, year="2025"):
    d = {r["REF_AREA"]: float(r["OBS_VALUE"]) for r in rows if r["MEASURE"]==measure and r["ETR_SCENARIO"]==scen
         and r["ETR_TAX_TYPE"]==asset and r["TIME_PERIOD"]==year and r["OBS_VALUE"] not in ("",)}
    return d
assets = sorted({r["ETR_TAX_TYPE"]+":"+r["Tax type"] for r in rows})
print(assets)
years = sorted({r["TIME_PERIOD"] for r in rows}); print(years)
for m in ("EATR","EMTR"):
    for a in ("COMP","TAN","BLD","AWS","INT"):
        for y in ("2024","2025"):
            d = get(m,"FIXED",a,y)
            if "FRA" in d:
                rk = sorted(d.values(), reverse=True).index(d["FRA"])+1
                print(m,a,y,"FRA",round(d["FRA"],2),"moy",round(st.mean(d.values()),2),"n",len(d),"rang",rk,
                      "DEU",d.get("DEU"),"GBR",d.get("GBR"),"USA",d.get("USA"),"ITA",d.get("ITA"),"ESP",d.get("ESP"))
