"""« Pour aller plus loin » : assemble les trois pistes (maires, pertes, revenus irréguliers) dans sorties/pal.json et
régénère la figure gpal_revenus_irreguliers. Hors scénario budgétaire central : pas de table « annuel » de bouclage ;
les coûts sont donnés comme ordres de grandeur. Lancer depuis fiscalite/ : python3 note8p/calculs/pal_calculs.py
"""
import json
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import pal_figure  # noqa: E402
import pal_maires  # noqa: E402
import pal_pertes  # noqa: E402
import pal_revenus  # noqa: E402

OUT = ICI.parent / "sorties"

rev = pal_revenus.calcule()
J = {
    "statuts": "[E] empirique publié ; [S] simulation des auteurs ; [H] hypothèse ; [C] choix de politique",
    "hors_scenario_central": True,
    "maires": pal_maires.calcule(),
    "pertes": {"simulation_r5": pal_pertes.resultats(0.05), "simulation_r8": pal_pertes.resultats(0.08),
               "simulation_r_egal_oat": pal_pertes.resultats(pal_pertes.I_OAT), "national": pal_pertes.national()},
    "revenus_irreguliers": rev,
}
pal_figure.trace(rev)
(OUT / "pal.json").write_text(json.dumps(J, ensure_ascii=False, indent=1, default=float), encoding="utf-8")

g = rev["regimes"]
print("barème :", rev["bareme"]["source"], [round(100 * t, 2) for t in rev["bareme"]["taux"]])
for k in ("annuel", "glissant_3", "quotient_5"):
    print(f"{k}: A {g[k]['A']['total']:.0f} B {g[k]['B']['total']:.0f} écart {g[k]['ecart_B_moins_A']:+.0f}")
s = J["pertes"]["simulation_r_egal_oat"]["jeune_pme"]["regimes"]
print("r = OAT, jeune PME : surcoût actuel", round(s["actuel"]["surcout_vs_symetrie"], 4), "indexation",
      round(s["indexation"]["surcout_vs_symetrie"], 4))
print("écrit :", OUT / "pal.json")
