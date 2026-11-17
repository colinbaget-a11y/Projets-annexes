"""« Pour aller plus loin » : lecture paramétrable du barème final du nouvel impôt sur le revenu (individuel, assiette =
revenu après cotisations sociales). Taux marginal affine par morceaux entre les points (revenu, taux), constant au-delà
du dernier point ; impôt = intégrale exacte du taux marginal (même convention que ircsg3_modele.continu).

Ordre de recherche : sorties/ircsg4.json (barème recalibré par le bloc IR-CSG, s'il existe), puis sorties/ircsg3.json
(clé « final »), puis le barème de repli ci-dessous (celui de la note au 18/11/2026). Le premier trouvé est utilisé ;
la source est renvoyée pour être écrite dans pal.json.
"""
import json
from pathlib import Path

import numpy as np

SORTIES = Path(__file__).resolve().parents[1] / "sorties"
REPLI = {"points": [0.0, 19176.48, 28764.72, 38352.96, 67117.68, 163424.67],
         "taux": [0.014717, 0.154717, 0.224717, 0.287358, 0.363645, 0.48]}


def _cherche(o, chemin=""):
    """Parcourt un JSON et renvoie les dictionnaires {points, taux} trouvés, avec leur chemin."""
    out = []
    if isinstance(o, dict):
        if isinstance(o.get("points"), list) and isinstance(o.get("taux"), list) and len(o["points"]) == len(o["taux"]):
            out.append((chemin, o))
        for k, v in o.items():
            out += _cherche(v, f"{chemin}/{k}")
    return out


def charge():
    """Renvoie (points, taux, source). Dans ircsg4.json, préfère une clé dont le chemin contient « final »."""
    f4 = SORTIES / "ircsg4.json"
    if f4.exists():
        cands = _cherche(json.loads(f4.read_text(encoding="utf-8")))
        if cands:
            cands.sort(key=lambda c: (0 if "final" in c[0].lower() else 1, len(c[0])))
            ch, d = cands[0]
            return list(map(float, d["points"])), list(map(float, d["taux"])), f"sorties/ircsg4.json{ch}"
    f3 = SORTIES / "ircsg3.json"
    if f3.exists():
        d = json.loads(f3.read_text(encoding="utf-8")).get("final", {})
        if "points" in d:
            return list(map(float, d["points"])), list(map(float, d["taux"])), "sorties/ircsg3.json/final"
    return REPLI["points"], REPLI["taux"], "barème de repli (pal_bareme.REPLI)"


class Bareme:
    def __init__(self, points=None, taux=None, source="fourni"):
        if points is None:
            points, taux, source = charge()
        self.x, self.t, self.source = np.asarray(points, float), np.asarray(taux, float), source
        self.cum = np.r_[0.0, np.cumsum(np.diff(self.x) * (self.t[1:] + self.t[:-1]) / 2)]

    def tm(self, z):
        """Taux marginal au revenu z."""
        return float(np.interp(z, self.x, self.t))

    def T(self, z):
        """Impôt dû sur un revenu annuel z (nul si z ≤ 0)."""
        z = max(float(z), 0.0)
        i = int(np.clip(np.searchsorted(self.x, z, side="right") - 1, 0, len(self.x) - 1))
        d = z - self.x[i]
        if i + 1 < len(self.x):
            pente = (self.t[i + 1] - self.t[i]) / (self.x[i + 1] - self.x[i])
            return float(self.cum[i] + self.t[i] * d + 0.5 * pente * d * d)
        return float(self.cum[i] + self.t[i] * d)

    def decrit(self):
        return {"source": self.source, "points": self.x.tolist(), "taux": self.t.tolist()}
