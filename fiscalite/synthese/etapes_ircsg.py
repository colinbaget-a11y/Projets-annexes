"""Fusion IR-CSG-CRDS en quatre étapes (méthode v2), pour la partie IR-CSG de la note fusionnée.

Étape 1, la fusion la plus simple : même assiette large pour tous (revenu après cotisations, sans niche ni taux
réduit), impôt individuel ; on garde le barème de l'IR (revenus 2024) appliqué à chaque adulte, et la CSG et la
CRDS deviennent un taux proportionnel unique, calé sur la recette (220 Md€).
Étape 2, simplifier sans effets de seuil : le barème neutre (taux marginal en ligne droite, le plus proche de ce
que chaque foyer paie aujourd'hui ; architectures_ircsg.py).
Étape 3, moins de perte sèche : franchise d'activité, puis aplatissement vers l'optimum (architectures_ircsg.py).
Étape 4, les redistributions implicites : retraités, familles, couples à un seul revenu, très hauts revenus ;
la proposition les corrige en partie.

Lancer depuis fiscalite/, après architectures_ircsg.py : python3 synthese/etapes_ircsg.py
Sorties : synthese/sorties/etapes_ircsg.txt et .json
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE)]
import architectures_ircsg as A  # noqa: E402

M, ex = A.M, A.M.ex
J = json.loads((HERE / "sorties/architectures_ircsg.json").read_text(encoding="utf-8"))
CAS = A.CAS + (("couple avec deux enfants 50 000 €, un seul revenu", "couple_2enf_mono", 50e3),
               ("couple avec deux enfants 80 000 €, un seul revenu", "couple_2enf_mono", 80e3),
               ("couple avec deux enfants 80 000 €, partage 60/40", "couple_2enf", 80e3))
L = []


def p(s=""):
    print(s, flush=True)
    L.append(s)


def evalue(nom, sched, o):
    r = {j: M.evalue(nom, *sched, o, jeu=j, sorties=(j == "central")) for j in A.JEUX}
    c = r["central"]
    g = c["groupes"]
    out = dict(nom=nom, **{f"v2_{j}": r[j]["v2"] for j in A.JEUX}, reel=c["v2_reel"], ext=c["v2_ext"],
               decl=c["v2_decl_recette"], perdants500=c["perdants500"], ecart_moyen=c["ecart_moyen"],
               dec_eur=c["dec_eur"], top1_Md=c["top1_Md"], top10_Md=c["top10_Md"],
               groupes={k: dict(Md=v["Md"], eur=v["eur"]) for k, v in g.items()},
               cas={n: M.cas_type(*sched, o, prof, brut) for n, prof, brut in CAS})
    p(f"[{nom}] gain réel {-out['v2_central']:.1f} Md€ ({-out['v2_bas']:.1f} à {-out['v2_haut']:.1f}) dont intensif"
      f" {-out['reel']:.1f}, participation {-out['ext']:.1f} ; revenu déclaré {out['decl']:+.1f} ; perdants > 500 €"
      f" {out['perdants500']:.0f} % ; écart moyen {out['ecart_moyen']:.0f} €")
    p("    déciles € " + " ".join(f"{u:+.0f}" for u in out["dec_eur"]) + f" ; 1 % {out['top1_Md']:+.1f} Md€ ; 10 %"
      f" {out['top10_Md']:+.1f} Md€")
    p("    Md€ : " + " ; ".join(f"{k} {v['Md']:+.1f}" for k, v in out["groupes"].items()))
    p("    € par foyer : " + " ; ".join(f"{k} {v['eur']:+,.0f}" for k, v in out["groupes"].items()))
    p("    cas-types : " + " ; ".join(f"{n} {u:+,.0f}" for n, u in out["cas"].items()))
    return out


if __name__ == "__main__":
    o0 = A.options()
    # étape 1 : barème de l'IR par adulte + taux proportionnel calé sur la recette
    lo, hi = -0.10, 0.20
    for _ in range(40):
        tau = (lo + hi) / 2
        lo, hi = (tau, hi) if M.recette(*ex.bareme_empile(tau), o0) < M.CIBLE else (lo, tau)
    tau = (lo + hi) / 2
    r_ir = M.recette(*ex.bareme_empile(0.0), o0)
    p(f"[ÉTAPE 1] barème de l'IR (seuils {ex.IR_SEUILS}, taux {ex.IR_TAUX}) par adulte sur l'assiette large :"
      f" {r_ir:.1f} Md€ ; taux proportionnel qui remplace CSG et CRDS : {100*tau:.2f} %")
    e1 = evalue("Étape 1 : barème de l'IR gardé, CSG-CRDS en taux proportionnel", ex.bareme_empile(tau), o0)
    bN = J["neutre"]
    e2 = evalue("Étape 2 : barème neutre, sans marche", A.bareme(bN), o0)
    o4 = A.options(F=4000.0)
    d4 = A.cale_d(bN, o4)
    e3 = evalue("Étape 3 : barème neutre + franchise d'activité 4 000 €", A.bareme(bN, d4), o4)
    P4 = J["propositions"]["4000"]
    e4 = evalue("Proposition", A.bareme(P4["bareme"]), P4["options"])
    json.dump(dict(tau=tau, recette_ir=r_ir, etape1=e1, etape2=e2, etape3=e3, proposition=e4,
                   atteignable=dict(v2_central=J["atteignable"]["v2_central"], v2_bas=J["atteignable"]["v2_bas"],
                                    v2_haut=J["atteignable"]["v2_haut"],
                                    perdants500=J["atteignable"]["perdants500"])),
              open(HERE / "sorties/etapes_ircsg.json", "w"), ensure_ascii=False, indent=1, default=float)
    (HERE / "sorties/etapes_ircsg.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
