"""Bloc IR-CSG v3 : barèmes continus candidats, calage sur la recette (constante, ou 3 et 6 Md€ de baisse nette
financée par d'autres blocs), indicateurs (cas-types, retraités, familles, efficacité).

Barème : taux marginal affine par morceaux entre des points de référence exprimés en revenu après cotisations par adulte
(0 ; 1 ; 1,5 ; 2 ; 3,5 Smic ; point où le plafond est atteint) ; impôt = intégrale. Smic 2025 : 21 622 € brut par an,
19 176 € après cotisations salariales (rapport 0,887 au niveau du Smic, OpenFisca). Calage : on ajoute le même nombre
de points d aux taux des points 1 à 1,5 Smic, 2 Smic et 3,5 Smic (« taux du bas et du milieu ») ; taux au premier euro
et plafond fixes.
"""
import json

import numpy as np
import pandas as pd

import ircsg3_modele as N

M, R, U = N.M, N.R, N.U
SZ = N.SMIC_Z
CT = U.CTN


def z_brut(b):
    g = CT[CT.profil == "seul"].sort_values("brut")
    return np.interp(b, g.brut, g.base_a)


def auj(profil, b):
    g = CT[CT.profil == profil].sort_values("brut")
    return float(np.interp(b, g.brut, g.ir + g.csg + g.crds))


def bases(profil, b):
    g = CT[CT.profil == profil].sort_values("brut")
    return float(np.interp(b, g.brut, g.base_a)), float(np.interp(b, g.brut, g.base_b))


def candidat(t, top, zp, d=0.0):
    """t : taux au premier euro, à 1 Smic, 1,5, 2 et 3,5 Smic ; plafond top atteint à zp."""
    pts = [0.0, SZ, 1.5 * SZ, 2 * SZ, 3.5 * SZ, zp]
    tt = [t[0]] + [x + d for x in t[1:]] + [top]
    tt = list(np.minimum.accumulate(np.array(tt)[::-1])[::-1])   # pas de taux décroissant (garde-fou)
    return pts, tt


def cale(t, top, zp, financement=0.0, o=None):
    o = o or N.options()
    d = N.cale(lambda d_: N.continu(*candidat(t, top, zp, d_)), o, N.CIBLE - financement)
    return d, candidat(t, top, zp, d)


CAS_SAL = {"smic": N.SMIC_BRUT, "smic15": 1.5 * N.SMIC_BRUT, "net2000": 30318.48, "smic2": 2 * N.SMIC_BRUT,
           "smic3": 3 * N.SMIC_BRUT, "cadre80": 80000.0, "cadre120": 120000.0, "cadre250": 250000.0}
RET = [12e3, 16e3, 20e3, 30e3, 60e3, 100e3]


def indicateurs(sched, o, eff=True):
    out = {}
    for k, b in CAS_SAL.items():
        z = z_brut(b)
        nv = float(N.impot_z(sched, o, [z])[0])
        out[f"sal_{k}"] = dict(brut=b, z=z, auj=auj("seul", b), apres=nv, delta=nv - auj("seul", b),
                               mois=(nv - auj("seul", b)) / 12, tm=100 * float(sched[0](z)))
    for p in RET:
        nv = float(N.impot_z(sched, o, [p])[0])
        out[f"ret_{int(p / 1e3)}k"] = dict(pension=p, auj=auj("retraite_seul", p), apres=nv, delta=nv - auj("retraite_seul", p))
    for prof, kids, b in (("couple_2enf", 2, 60e3), ("couple_2enf_mono", 2, 40e3), ("couple_2enf_mono", 2, 60e3),
                          ("couple_3enf", 3, 60e3), ("couple_3enf_mono", 3, 45e3), ("parent_isole_2enf", 2, N.SMIC_BRUT),
                          ("couple_0enf_mono", 0, 80e3), ("retraite_couple", 0, 30e3), ("retraite_couple", 0, 60e3)):
        za, zb = bases(prof, b)
        zs = [za] + ([zb] if prof.startswith(("couple", "retraite_couple")) else [])
        nv = float(N.impot_z(sched, o, zs, kids)[0])
        out[f"{prof}_{int(b / 1e3)}k"] = dict(auj=auj(prof, b), apres=nv, delta=nv - auj(prof, b))
    if eff:
        e = N.evalue(sched, o, repart=True)
        g = e["groupes"]
        out["agregats"] = dict(recette=e["recette"], gain=e["gain"], emplois=e["emplois"], intensif=-e["reel"],
                               extensif=-e["ext"], retraites=g["retraites"]["Md"], actifs=g["actifs"]["Md"],
                               top1=e["top1_Md"], top10=e["top10_Md"], couples_enfants=g["couples2"]["eur"],
                               parents_isoles=g["parents_isoles"]["eur"], deciles=e["dec_eur"],
                               perdants500=e["perdants500"], **{k: v for k, v in N.R.effets_reels(e).items()})
    return out


# familles de barèmes : taux au premier euro, 1, 1,5, 2, 3,5 Smic (avant calage) ; plafond ; point du plafond
FAMILLES = {
    "A_douce48": ([0.02, 0.12, 0.19, 0.25, 0.33], 0.48, 160e3),
    "B_precoce45": ([0.00, 0.12, 0.20, 0.27, 0.36], 0.45, 110e3),
    "C_lineaire50": ([0.03, 0.12, 0.18, 0.24, 0.32], 0.50, 200e3),
    "D_douce45": ([0.02, 0.12, 0.19, 0.25, 0.33], 0.45, 140e3),
    "E_douce50": ([0.02, 0.12, 0.19, 0.25, 0.33], 0.50, 180e3),
}

if __name__ == "__main__":
    o = N.options()
    rows = {}
    for nom, (t, top, zp) in FAMILLES.items():
        for F in (0.0, 3.0, 6.0):
            d, (pts, tt) = cale(t, top, zp, F, o)
            s = N.continu(pts, tt)
            ind = indicateurs(s, o, eff=(F == 0.0))
            rows[f"{nom}_F{int(F)}"] = dict(points=pts, taux=tt, d=d, ind=ind)
            a = ind.get("agregats", {})
            print(f"{nom} F{F:.0f} taux {[round(100 * x, 1) for x in tt]} | smic {ind['sal_smic']['mois']:+.0f} €/m,"
                  f" 1,5S {ind['sal_smic15']['mois']:+.0f}, 2000net {ind['sal_net2000']['mois']:+.0f}, 3S"
                  f" {ind['sal_smic3']['mois']:+.0f}, 120k {ind['sal_cadre120']['delta']:+.0f} €/an, 250k"
                  f" {ind['sal_cadre250']['delta']:+.0f} | ret " + " ".join(f"{ind[f'ret_{int(p / 1e3)}k']['delta']:+.0f}" for p in RET)
                  + (f" | gain {a['gain']:.2f} emplois {a['emplois'] / 1e3:.0f}k ret {a['retraites']:+.1f} top1 {a['top1']:+.2f}"
                     f" top10 {a['top10']:+.1f}" if a else ""), flush=True)
    json.dump(rows, open(N.SORTIES / "ircsg3_baremes.json", "w"), ensure_ascii=False, indent=1, default=float)
