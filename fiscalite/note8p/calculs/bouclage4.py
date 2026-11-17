"""Bouclage v4 (scénario central unique) : solde ≥ 0,5 Md€ chaque année de 2027 à 2040, sans dette.

Entrées (années de caisse) : is4.json (`is_recette_nette_bloc_is_prudent` : taux réduit prudent, niches hors CIR
prudentes, suppression du CIR prudente, déduction immédiate et réinvestissement), foncier3.json (B_E10 : taxe nationale
sur le sol, DMTO, report, déductibilité, calendrier), ircsg4.json (`annuel_final` : fusion à recette constante et
financement externe reçu), pfu4.json/pfu3.json (fin de l'effacement, prudent : réserve). Séries IS déflatées de 3 %/an
(euros de 2027 environ). Marge de sécurité : 0,5 Md€ par an. Sorties : sorties/bouclage4.json et .txt.
"""
import json
from pathlib import Path

S = Path(__file__).resolve().parent.parent / "sorties"
L = lambda n: json.loads((S / n).read_text(encoding="utf-8"))
IS, FO, IR = L("is4.json")["annuel_caisse"], L("foncier3.json")["annuel_par_scenario"]["B_E10"], L("ircsg4.json")
PF = L("pfu3.json")["annuel"]
Y = [str(a) for a in range(2027, 2041)]
D = lambda y: 1.03 ** (int(y) - 2027)
res = {}
for y in Y:
    i, f, r = IS[y], FO[y], IR["annuel_final"][y]
    is_net = i.get("is_recette_nette_bloc_is_prudent", 0) / D(y)
    ligne = {"foncier_taxe_sol": f["taxe_fonciere_nouvelle"], "foncier_dmto": f["dmto"],
             "foncier_autres": f["net"] - f["taxe_fonciere_nouvelle"] - f["dmto"],
             "is_net_prudent": is_net,
             "ir_financement_externe": r["ircsg_total"],
             "reserve_plus_values": PF[y]["fin_effacement_prudent"]}
    ligne["solde"] = sum(v for k, v in ligne.items() if k != "reserve_plus_values")
    res[y] = ligne
(S / "bouclage4.json").write_text(json.dumps({"annuel": res, "notes": __doc__}, ensure_ascii=False, indent=1),
                                  encoding="utf-8")
txt = "\n".join(f"{y} " + " ".join(f"{k}={v:+.2f}" for k, v in res[y].items()) for y in Y)
(S / "bouclage4.txt").write_text(txt + "\n", encoding="utf-8")
print(txt)
print("solde min", round(min(res[y]["solde"] for y in Y), 2))
