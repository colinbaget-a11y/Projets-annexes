"""Coût d'une baisse du prélèvement forfaitaire unique (PFU) à 30 % ou 25 %, calcul de coin de table.
Assiette au taux forfaitaire de 12,8 % hors assurance-vie, revenus 2024 : 79,6 Md€ (dividendes 50,1, intérêts 10,4,
plus-values 18,8 ; totaux DGFiP de la 2042, pfu/donnees/pfu_chiffres.csv). PFU 2026 : 12,8 % d'IR + 18,6 % de
prélèvements sociaux (LFSS 2026). Hausse de 1,4 point des prélèvements sociaux en 2026 : 1,5 Md€ (source secondaire).
Réaction : élasticité des revenus du capital déclarés au taux net de prélèvement de 0,77 (0,22 à 0,96 ; Lefebvre,
Lehmann et Sicsic). Hypothèse : la réaction porte sur l'assiette forfaitaire seule, taxée au nouveau taux global.
- PFU à 30 % : retour au taux d'avant 2026 (prélèvements sociaux 17,2 %).
- PFU à 25 % : part d'IR ramenée à 6,4 %, prélèvements sociaux inchangés à 18,6 %.
"""
import json
from pathlib import Path

B, T0 = 79.6 * 1.03, 0.314          # revenus 2024 portés en euros de 2025 (+3 % par an)
OPT = {"30": dict(taux=0.30, statique=1.5), "25": dict(taux=0.25, statique=(T0 - 0.25) * B)}
res = {}
for k, o in OPT.items():
    dnet = (1 - o["taux"]) / (1 - T0) - 1
    res[k] = dict(statique=o["statique"], hausse_taux_net_pct=100 * dnet)
    for nom, e in (("bas", 0.22), ("central", 0.77), ("haut", 0.96)):
        retour = o["taux"] * B * e * dnet          # impôt sur le surcroît d'assiette déclaré
        res[k][nom] = o["statique"] - retour
out = Path(__file__).resolve().parent.parent / "sorties" / "pfu_options.json"
out.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
for k, v in res.items():
    print(f"PFU {k} % : statique {v['statique']:.1f} ; après réaction {v['central']:.1f} (de {v['haut']:.1f} à {v['bas']:.1f}) Md€ ; taux net +{v['hausse_taux_net_pct']:.1f} %")
