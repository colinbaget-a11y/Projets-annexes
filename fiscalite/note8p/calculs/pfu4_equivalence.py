"""Bloc « fiscalité du capital », v4 (note8p/CONSIGNES_V4.md, section Capital) : conditions exactes de l'équivalence
« vendre puis transmettre » / « transmettre puis l'héritier vend » avec la règle retenue (correction à la marge), et ce
qui se passe hors de ces conditions.

Réutilise pfu3_neutralite.py (barème des droits, PFU) sans le modifier : il est importé avec --sans-figure et réécrit
pfu3.json et pfu3_calculs.txt à l'identique.
Lancer depuis fiscalite/ : python3 note8p/calculs/pfu4_equivalence.py  -> note8p/sorties/pfu4.json, pfu4_calculs.txt

Notations : V valeur transmise, B prix d'acquisition, G = V − B, t PFU, D(.) droits du bénéficiaire sur sa part.
Règle retenue : prix repris B + a, avec t·a = D(V) − D(V − tG).
  A (le parent vend, l'héritier reçoit le produit et le replace dans le même actif) ;
  B (l'héritier reçoit les titres et les vend n années plus tard).
Les droits sont payés à la transmission sur d'autres ressources dans les deux chemins. Valeur de l'actif multipliée par
F = (1+g)^n entre la transmission et la vente ; actualisation au taux ρ. Écart de patrimoine net, en valeur actuelle :
  Δ = W_B − W_A = [t·G·(1 − t)·(F − 1) + t·a] / (1+ρ)^n − t·a
(premier terme : l'impôt sur G est différé, sa valeur continue de rapporter ; second : le crédit t·a arrive à la vente
au lieu d'être déduit tout de suite). n = 0 : Δ = 0 exactement.
"""
import contextlib
import io
import json
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
OUT = ICI.parent / "sorties"
sys.path.insert(0, str(ICI))
_argv = sys.argv
sys.argv = [sys.argv[0], "--sans-figure"]
with contextlib.redirect_stdout(io.StringIO()):
    import pfu3_neutralite as p3  # noqa: E402
sys.argv = _argv
droits, T = p3.droits, p3.T
L, J = [], {}


def p(s=""):
    print(s)
    L.append(s)


def fr(x, d=0):
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",").replace("-", "−")


def maj(v, g, lien="ligne directe", t=T):
    return (droits(v, lien) - droits(v - t * g, lien)) / t


def chemins(V, B, n=0, g=0.0, rho=0.0, t=T, t_vente=None, lien="ligne directe"):
    """Patrimoine net de l'héritier (valeur actuelle, droits déduits) dans les deux chemins."""
    tv = T if t_vente is None else t_vente
    G, F, d = V - B, (1 + g) ** n, (1 + rho) ** -n
    a = maj(V, G, lien, t)
    XA = V - t * G
    WA = (XA * F - tv * XA * (F - 1)) * d - droits(V - t * G, lien)
    WB = (V * F - tv * (V * F - B - a)) * d - droits(V, lien)
    impA = t * G + droits(V - t * G, lien) + tv * XA * (F - 1) * d
    impB = droits(V, lien) + tv * (V * F - B - a) * d
    return dict(a=a, WA=WA, WB=WB, ecart=WB - WA, impots_A=impA, impots_B=impB,
                formule=(t * G * (1 - t) * (F - 1) + t * a) * d - t * a if tv == t else None)


V, B = 1e6, 1e5
p("ÉQUIVALENCE VENDRE / TRANSMETTRE — exemple 100 k€ devenus 1 M€, un enfant, droit de 2026")
base = chemins(V, B)
p(f"  majoration a = {fr(base['a'])} € ; revente immédiate : écart {fr(base['ecart'])} € (impôts A {fr(base['impots_A'])},"
  f" B {fr(base['impots_B'])})")
J["immediat"] = base
DIFF = {}
for n, g, rho, lib in ((10, 0.04, 0.04, "10 ans, rendement = actualisation = 4 %"),
                       (10, 0.02, 0.04, "10 ans, valeur +2 %/an (inflation), actualisation 4 %"),
                       (10, 0.0, 0.04, "10 ans, valeur constante, actualisation 4 %"),
                       (25, 0.04, 0.04, "25 ans, 4 % / 4 %")):
    c = chemins(V, B, n, g, rho)
    DIFF[lib] = c
    p(f"  {lib} : écart B − A {fr(c['ecart'])} € ({fr(100 * c['ecart'] / V, 1)} % de V) ; formule {fr(c['formule'])} ;"
      f" impôts en valeur actuelle A {fr(c['impots_A'])}, B {fr(c['impots_B'])}")
J["differe"] = DIFF
# Comparaison : le même héritier qui aurait reçu du numéraire et acheté l'actif garde le même avantage de report sur
# les gains postérieurs ; l'avantage propre à B porte sur l'impôt latent tG différé.
for tv, lib in ((0.309, "PFU ramené à 30,9 % à la vente (fin de la CRDS)"), (0.25, "PFU à 25 % à la vente")):
    c = chemins(V, B, t_vente=tv)
    DIFF[lib] = c
    p(f"  {lib}, revente immédiate : écart {fr(c['ecart'])} € = (t' − t)(G − a) = {fr((tv - T) * (V - B - c['a']))}")
for lien in ("frère ou sœur", "neveu", "conjoint"):
    c = chemins(V, B, lien=lien)
    p(f"  lien {lien} : a = {fr(c['a'])} € ; écart immédiat {fr(c['ecart'])} €")
    J[f"lien_{lien}"] = c

# Pluralité d'héritiers : deux enfants, titres de valeur VT (prix BT) et maison de même valeur.
PLUR = {}
for VT, BT in ((1e6, 1e5), (1.2e6, 1e5)):
    GT = VT - BT
    tG = T * GT
    A_tot = tG + 2 * droits((2 * VT - tG) / 2)              # le parent vend : impôt latent partagé par les deux enfants
    a_moitie = maj(VT, GT / 2)                              # (1) chaque enfant reçoit la moitié des titres
    B1 = 2 * droits(VT) + 2 * T * (GT / 2 - a_moitie)
    a_un = maj(VT, GT)                                      # (2) titres à l'un, maison à l'autre (partage en valeur)
    B2 = 2 * droits(VT) + T * (GT - a_un)
    PLUR[f"{VT:.0f}"] = dict(vendre_avant=A_tot, titres_partages=B1, titres_a_un=B2, impot_latent_un=T * (GT - a_un),
                             par_enfant_si_vente=tG / 2)
    p(f"  deux enfants (titres {fr(VT)} € dont prix {fr(BT)} € + maison {fr(VT)} €) : vendre avant {fr(A_tot)} € ;"
      f" titres partagés {fr(B1)} € (écart {fr(B1 - A_tot)}) ; titres à un seul enfant {fr(B2)} € (écart"
      f" {fr(B2 - A_tot)}) ; ce dernier supporte seul {fr(T * (GT - a_un))} € d'impôt net, contre {fr(tG / 2)} € par"
      f" enfant si le parent avait vendu")
J["pluralite"] = PLUR

# Baisse de valeur après le décès : vente à 0,5 M€
c = chemins(V, B, n=1, g=-0.5, rho=0.0)
p(f"  valeur divisée par deux avant la vente : prix repris {fr(B + c['a'])} €, plus-value imposable"
  f" {fr(5e5 - B - c['a'])} € ; écart {fr(c['ecart'])} €")
J["baisse"] = c

(OUT / "pfu4_calculs.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
(OUT / "pfu4.json").write_text(json.dumps(J, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
