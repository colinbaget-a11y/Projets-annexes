"""Très hauts revenus dans le modèle à foyers purs, selon la répartition (non publiée) des revenus au PFU entre tranches.

La DGFiP ne publie pas, par tranche de revenu fiscal, la part des revenus imposés au prélèvement forfaitaire unique.
Le modèle (ir_csg/ir_csg.py, variable d'environnement CAPITAL) a trois conventions : prorata (même part dans chaque
tranche), haut (revenus au PFU logés d'abord dans les tranches les plus hautes), mixte (moyenne, convention
centrale). La convention change le revenu du barème des tranches du haut et la charge actuelle qui lui est
attribuée, donc l'effet de la fusion sur ces tranches. Pour chaque convention, on recale le taux à z1 du barème neutre et de la
proposition (sorties/architectures_ircsg.json) sur la recette, et on lit, pour les tranches au-delà de 1 M€ de revenu fiscal :
le nombre de foyers, la variation de charge (€ par foyer et points du revenu du barème après cotisations) et le taux
moyen actuel IR + CSG + CRDS attribué à ce revenu.

Lancer depuis fiscalite/ : python3 synthese/controle_hauts_purs.py -> synthese/sorties/controle_hauts_purs.txt
"""
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

if len(sys.argv) > 1 and sys.argv[1] == "--un":
    sys.path[:0] = [str(HERE)]
    import pandas as pd
    import modele_purs as M
    ex = M.ex
    cap = {}
    _rep = M.repartition

    def rep(res):
        cap["res"] = res
        return _rep(res)
    M.repartition = rep

    def bareme(b):
        t0, tb, z1, t1, z2 = b
        return ex.bareme_lineaire([0, 20e3, z1, z2], [t0, tb, t1, 0.50])

    A = json.loads((HERE / "sorties/architectures_ircsg.json").read_text(encoding="utf-8"))
    P4 = A["propositions"]["4000"]
    out = {}
    for nom, (t0, tb, z1, _, z2), o in (("neutre", A["neutre"], dict(M.OPT0)),
                                         ("proposition", P4["bareme"], P4["options"])):
        lo, hi = 0.0, 0.50
        for _ in range(32):
            t1 = (lo + hi) / 2
            lo, hi = (t1, hi) if M.recette(*bareme((t0, tb, z1, t1, z2)), o) < M.CIBLE else (lo, t1)
        b = (t0, tb, z1, (lo + hi) / 2, z2)
        r = M.evalue(nom, *bareme(b), o, sorties=True)
        res = cap["res"]
        df = pd.DataFrame({"tr": M.TR, "w": M.W, "zn": M.W * M.ZN,
                           "dn": sum(w * (imp - cur) for w, imp, cur, *_ in res.values()),
                           "cur": sum(w * cur for w, imp, cur, *_ in res.values())})
        g = df.groupby("tr", sort=False).sum().iloc[-10:]
        out[nom] = dict(t1=b[3], cen=r["v2"], top1=r["top1_Md"], dec=r["dec_eur"],
                        tranches=[dict(tr=i, foyers=float(u.w), eur=float(u.dn / u.w), pts=float(100 * u.dn / u.zn),
                                       taux_auj=float(100 * u.cur / u.zn)) for i, u in g.iterrows()])
    print("JSON" + json.dumps(out))
    sys.exit()

L = ["Très hauts revenus selon la convention de répartition des revenus au PFU (modèle à foyers purs)",
     "pts : variation de la charge IR + CSG + CRDS en points du revenu du barème après cotisations ; taux_auj : charge"
     " actuelle attribuée à ce revenu, en % ; une hausse de cette charge actuelle signale une convention plus proche"
     " du barème légal (un salaire de plusieurs millions paie environ 50 % aujourd'hui).", ""]
for conv in ("mixte", "haut", "prorata"):
    env = dict(os.environ, CAPITAL=conv)
    o = subprocess.run([sys.executable, __file__, "--un"], env=env, capture_output=True, text=True, check=True,
                       cwd=HERE.parent).stdout
    d = json.loads(o.split("JSON", 1)[1])
    for nom, r in d.items():
        L.append(f"[{conv} / {nom}] t1 {100*r['t1']:.1f} % ; perte sèche réelle {r['cen']:+.1f} Md€ ; 1 % du haut"
                 f" {r['top1']:+.1f} Md€ ; déciles € " + " ".join(f"{u:+.0f}" for u in r["dec"]))
        for t in r["tranches"]:
            L.append(f"    {t['tr']:<26} foyers {t['foyers']:>8,.0f}  € {t['eur']:>+12,.0f}  pts {t['pts']:+6.1f}"
                     f"  taux_auj {t['taux_auj']:5.1f}")
    L.append("")
(HERE / "sorties/controle_hauts_purs.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
