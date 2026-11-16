import pandas as pd
pd.set_option("display.width", 250)
c = pd.read_csv("donnees/communes.csv.gz", dtype={"codgeo": str, "dep": str, "epci": str})
print(c.shape)
print(c.dtypes.to_string())
print(c.describe().T.to_string())
print(c[c.codgeo.isin(["75056", "69123", "44109", "33009", "92012", "92050"])].T.to_string())
print(open("donnees/terrains_dep.csv").read()[:600])
print(open("donnees/tfpb2017_communes.csv").read()[:300])
