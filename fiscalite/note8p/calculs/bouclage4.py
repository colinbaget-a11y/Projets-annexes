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
IS, FO, IR = L("is4.json")["annuel_caisse"], L("foncier3.json")["annuel_par_scenario"][json.loads((Path(__file__).resolve().parent.parent / "parametres.json").read_text(encoding="utf-8"))["scenario_foncier"]], L("ircsg4.json")
PF = L("pfu3.json")["annuel"]
_IX = L("pal.json")["pertes"]["national"]["indexation_cout_regime_Md"]
PERTES = {int(a): v for a, v in _IX["montee_en_charge_indicative"].items()}
PERTES_REGIME = _IX["central"]
Y = [str(a) for a in range(2027, 2041)]
_P = json.loads((S.parent / "parametres.json").read_text(encoding="utf-8"))
G, AREF = _P["croissance_nominale"], _P["annee_reference"]
D = lambda y: (1 + G) ** (int(y) - AREF)
K25 = (1 + G) ** (AREF - 2025)          # niveaux 2025 (foncier, impôt sur le revenu, pertes) portés en euros de l'année de référence
res = {}
for y in Y:
    i, f, r = IS[y], FO[y], IR["annuel_final"][y]
    is_net = i.get("is_recette_nette_bloc_is_prudent", 0) / D(y)
    ligne = {"foncier_taxe_sol": K25 * f["taxe_fonciere_nouvelle"], "foncier_dmto": K25 * f["dmto"],
             "foncier_autres": K25 * (f["net"] - f["taxe_fonciere_nouvelle"] - f["dmto"]),
             "is_net_prudent": is_net,
             "is_revalorisation_deficits": -K25 * PERTES.get(int(y), PERTES_REGIME if int(y) >= 2032 else 0.0),
             "ir_financement_externe": K25 * (r["ircsg_total"] - (_P.get("ajustement_droit_2032", 0.0) if int(y) >= 2029 else 0.0)),   # neutre par rapport au droit de 2032
             "reserve_plus_values": K25 * PF[y]["fin_effacement_prudent"]}
    ligne["solde"] = sum(v for k, v in ligne.items() if k != "reserve_plus_values")
    res[y] = ligne
(S / "bouclage4.json").write_text(json.dumps({"annuel": res, "notes": __doc__}, ensure_ascii=False, indent=1),
                                  encoding="utf-8")
txt = "\n".join(f"{y} " + " ".join(f"{k}={v:+.2f}" for k, v in res[y].items()) for y in Y)
(S / "bouclage4.txt").write_text(txt + "\n", encoding="utf-8")
print(txt)
print("solde min", round(min(res[y]["solde"] for y in Y), 2))
