"""Contrôle transversal : effet de la proposition IR-CSG sur les très hauts revenus, selon la répartition
(non publiée) des revenus au PFU entre tranches.

Lancer depuis fiscalite/ir_csg/ : python3 controle_hauts.py  ->  sorties/controle_hauts.txt
Chaque convention (CAPITAL=prorata, mixte, haut ; voir ir_csg.py) change les foyers représentatifs : on relance
donc le calcul dans un sous-processus, on recale le taux t1 de la proposition (t0, tb, z1, z2 fixés) pour garder
la recette, et on lit la variation de la charge fusionnée des foyers représentatifs du haut de la distribution,
en points de revenu fiscal de référence. Les revenus au PFU gardent leur régime (et, selon la note PFU, la
majoration de 4 points qui remplace la CEHR) : la variation lue ici est donc celle de la facture totale.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

if len(sys.argv) > 1 and sys.argv[1] == "--un":
    sys.path[:0] = [str(HERE), str(HERE.parent)]
    import numpy as np
    import proposition as pr
    v = pr.v
    b = json.loads((HERE / "sorties/proposition_baremes.json").read_text())["proposition"]
    t1, (tm, T) = pr.cale(b["t0"], b["tb"], b["z1"], b["z2"], b["F"], b["fam"])
    n, pt, _ = pr.systeme(tm, T, b["F"], b["fam"])
    rfr = v._RFR_F
    dw = sum(w * (imp - cur) for w, imp, cur in pt.values())
    ww = sum(w for w, _, _ in pt.values())
    out = []
    for lo, hi in ((250e3, 500e3), (500e3, 1e6), (1e6, 3e6), (3e6, 9e6), (9e6, np.inf)):
        m = (rfr >= lo) & (rfr < hi)
        if m.any():
            out.append(dict(lo=lo, hi=hi, foyers=float(ww[m].sum()), pts=float(100 * dw[m].sum() / (ww[m] * rfr[m]).sum()),
                            pct=float(100 * dw[m].sum() / (ww[m] * v.CUR[m]).sum())))
    print(json.dumps(dict(t1=t1, res=out)))
    sys.exit()

L = []
for conv in ("prorata", "mixte", "haut"):
    env = dict(os.environ, CAPITAL=conv)
    r = subprocess.run([sys.executable, str(Path(__file__)), "--un"], env=env, capture_output=True, text=True,
                       cwd=HERE)
    d = json.loads(r.stdout.strip().splitlines()[-1])
    L.append(f"CAPITAL={conv} : t1 recalé {100*d['t1']:.1f} %")
    for u in d["res"]:
        hi = "+" if u["hi"] == float("inf") else f"{u['hi']/1e6:g} M€"
        L.append(f"  RFR {u['lo']/1e6:g} M€ à {hi} : {u['foyers']:,.0f} foyers ; charge fusionnée {u['pts']:+.1f} pts de RFR "
                 f"({u['pct']:+.0f} % de la charge actuelle sur les revenus du barème)".replace(",", " "))
(HERE / "sorties/controle_hauts.txt").write_text("\n".join(L) + "\n")
print("\n".join(L))
