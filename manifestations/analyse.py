"""
Effet des émeutes sur les intentions de vote : écart à la tendance d'avant, comparé aux dates placebo.

Pour chaque épisode (pays, date) et chaque bloc :
  1. série : sondages d'une seule page Wikipédia (un cycle électoral, une liste de partis stable),
     la plus fournie autour de la date ; part du bloc = somme des partis du bloc ;
  2. tendance d'avant : sur les 26 semaines précédentes, part = effet institut + pente x temps
     (MCO). L'effet institut neutralise les écarts habituels entre sondeurs ;
  3. écart : sondages des 12 semaines suivantes moins le prolongement de la tendance (instituts
     présents avant seulement), moyenné sur les semaines 0-6 et 6-12 ;
  4. placebo : la même procédure à toutes les dates (pas d'une semaine) de la même série, loin de
     tout épisode, donne la distribution des écarts « normaux » ; p-valeur = part des placebos dont
     l'écart absolu dépasse celui de l'épisode.

    python analyse.py episodes.csv      écrit resultats.csv et figures/<episode>.png
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import blocs as bl  # noqa: E402

ICI = Path(__file__).resolve().parent
FIG = ICI / "figures"
AVANT, APRES = 26, 12          # semaines
MIN_AVANT, MIN_APRES = 8, 4    # sondages minimum de part et d'autre
EXCLUSION_PLACEBO = 16         # semaines autour de chaque épisode exclues des placebos
PLACEBO_ANNEES = 4             # placebos pris dans les 4 ans autour de l'épisode (même époque)
# élections nationales : les fenêtres s'arrêtent aux élections (les sondages changent de nature après)
ELECTIONS = {
    "UK": ["2005-05-05", "2010-05-06", "2015-05-07", "2017-06-08", "2019-12-12", "2024-07-04"],
    "FR": ["2007-04-22", "2007-06-10", "2009-06-07", "2012-04-22", "2012-06-10", "2014-05-25", "2017-04-23",
           "2017-06-11", "2019-05-26", "2022-04-10", "2022-06-12", "2024-06-09", "2024-06-30"],
    "DE": ["2002-09-22", "2005-09-18", "2009-09-27", "2013-09-22", "2017-09-24", "2021-09-26", "2025-02-23"],
    "ES": ["2008-03-09", "2011-11-20", "2015-12-20", "2016-06-26", "2019-04-28", "2019-11-10", "2023-07-23"],
    "IT": ["2008-04-13", "2013-02-24", "2018-03-04", "2022-09-25"],
}
ELECTIONS = {k: [pd.Timestamp(d) for d in v] for k, v in ELECTIONS.items()}


def charger():
    """Une ligne par sondage : part de chaque bloc (moyenne des scénarios de candidats s'il y en a).
    La colonne « institut » devient « série | institut » : l'effet fixe absorbe à la fois l'écart
    habituel du sondeur et la différence de niveau entre questions (présidentielle, européennes…)."""
    s = pd.read_csv(ICI / "sondages.csv.gz", parse_dates=["date"])
    s["bloc"] = [bl.bloc(p, str(x)) for p, x in zip(s.pays, s.parti)]
    s = s[s.bloc.notna() & (s.bloc != "non classé")]
    w = (s.groupby(["pays", "page", "institut", "date", "scenario", "bloc"]).part.sum()
         .unstack("bloc").fillna(0).reset_index()
         .groupby(["pays", "page", "institut", "date"])[[b for b in bl.BLOCS if b in s.bloc.unique()]].mean()
         .reset_index())
    w["institut"] = w.page + " | " + w.institut
    total = w[[b for b in bl.BLOCS if b in w]].sum(axis=1)
    return w[(total >= 70) & (total <= 105)]           # lignes mal lues ou intentions brutes


def fenetre(w, pays, jour):
    """Sondages autour de la date, coupés aux élections ; toutes les séries du pays."""
    jour = pd.Timestamp(jour)
    x = w[(w.pays == pays) & (w.date >= jour - pd.Timedelta(weeks=AVANT))
          & (w.date < jour + pd.Timedelta(weeks=APRES))]
    avant = [d for d in ELECTIONS[pays] if d < jour]
    apres = [d for d in ELECTIONS[pays] if d >= jour]
    if avant:
        x = x[x.date > max(avant)]
    if apres:
        x = x[x.date < min(apres)]
    x = x.copy()
    x["t"] = (x.date - jour).dt.days / 7
    return x, " ; ".join(sorted(x.page.unique()))


def ecart(x, col):
    """Écart à la tendance d'avant : (semaines 0-6, semaines 6-12, effets institut, pente,
    écart 0-6 sans tendance). La variante sans tendance compare au niveau des 12 dernières semaines
    (effets institut seulement) : elle ne prolonge pas une baisse ou une hausse qui s'arrêterait d'elle-même."""
    av, ap = x[x.t < 0], x[x.t >= 0]
    if len(av) < MIN_AVANT or len(ap) < MIN_APRES or col not in x or x[col].abs().sum() == 0:
        return None

    def ajuste(d, pente=True):
        inst = sorted(d.institut.unique())
        X = (np.asarray(d.institut, dtype=object)[:, None] == np.array(inst, dtype=object)).astype(float)
        if pente:
            X = np.column_stack([X, d.t.values])
        coef, *_ = np.linalg.lstsq(X, d[col].values, rcond=None)
        return dict(zip(inst, coef[:len(inst)])), (coef[-1] if pente else 0.0)

    effet, pente = ajuste(av)
    ap = ap[ap.institut.isin(effet)]
    if len(ap) < MIN_APRES:
        return None
    r = ap[col].values - (ap.institut.map(effet).values + pente * ap.t.values)
    debut = ap.t.values < 6
    e1 = r[debut].mean() if debut.any() else np.nan
    e2 = r[~debut].mean() if (~debut).any() else np.nan
    # variante sans tendance
    recent = av[av.t >= -12]
    e_niv = np.nan
    if len(recent) >= 4:
        eff_n, _ = ajuste(recent, pente=False)
        a2 = ap[ap.institut.isin(eff_n) & (ap.t < 6)]
        if len(a2):
            e_niv = (a2[col].values - a2.institut.map(eff_n).values).mean()
    return e1, e2, effet, pente, e_niv


_CACHE = {}


def placebos(w, pays, dates_episodes, centre):
    """Écarts (semaines 0-6) à toutes les dates placebo du pays, pour chaque bloc. Même traitement que
    les épisodes (fenêtres coupées aux élections), loin de toute émeute candidate."""
    cle = (pays, centre)
    if cle in _CACHE:
        return _CACHE[cle]
    serie = w[w.pays == pays]
    debut = max(serie.date.min() + pd.Timedelta(weeks=AVANT), centre - pd.DateOffset(years=PLACEBO_ANNEES))
    fin = min(serie.date.max() - pd.Timedelta(weeks=APRES), centre + pd.DateOffset(years=PLACEBO_ANNEES))
    out = {c: [] for c in bl.BLOCS}
    for jour in pd.date_range(debut, fin, freq="W-MON"):
        if any(abs((jour - d).days) < 7 * EXCLUSION_PLACEBO for d in dates_episodes):
            continue
        x, _ = fenetre(w, pays, jour)
        for c in bl.BLOCS:
            e = ecart(x, c)
            if e is not None and not np.isnan(e[0]):
                out[c].append((e[0], e[4]))
    _CACHE[cle] = {c: np.array(v).reshape(-1, 2) for c, v in out.items()}
    return _CACHE[cle]


COULEURS = dict(zip(bl.BLOCS, ["#6250d6", "#2a78d6", "#eda100", "#e34948", "#9b1c1c", "#898781"]))


def figure(x, jour, effets, pentes, titre, fichier):
    """Moyenne hebdomadaire des sondages corrigés des effets institut, et tendance d'avant prolongée.
    Seuls les sondages des instituts présents avant l'émeute sont montrés (ce sont ceux de l'estimation)."""
    fig, ax = plt.subplots(figsize=(9, 5))
    for c in bl.BLOCS:
        if c not in effets:
            continue
        y = x[x.institut.isin(effets[c])]
        base = np.mean(list(effets[c].values()))
        aj = y[c] - y.institut.map(effets[c]) + base
        sem = aj.groupby(np.floor(y.t)).mean()
        ax.plot(sem.index, sem.values, color=COULEURS[c], lw=2, label=c, marker="o", ms=3)
        tt = np.array([y.t.min(), 0])
        ax.plot(tt, base + pentes[c] * tt, color=COULEURS[c], lw=1, ls="-", alpha=0.5)
        tt = np.array([0, min(APRES, y.t.max())])
        ax.plot(tt, base + pentes[c] * tt, color=COULEURS[c], lw=1.2, ls="--")
    ax.axvline(0, color="#52514e", lw=1)
    ax.axvspan(0, 6, color="#f0efec", zorder=0)
    ax.set_xlabel(f"Semaines autour du début des émeutes ({jour}) ; zone grisée : semaines 0-6")
    ax.set_ylabel("Intentions de vote (%), corrigées des effets institut")
    ax.set_title(titre, loc="left", fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#e1e0d9", lw=0.6)
    ax.legend(frameon=False, fontsize=8, ncol=3, loc="upper left", bbox_to_anchor=(0, -0.13))
    fig.tight_layout()
    fig.savefig(fichier, dpi=140)
    plt.close(fig)


def synthese(R, P, fichier):
    """Écart à la tendance (semaines 0-6) par épisode, pour la droite radicale et le parti au pouvoir,
    avec l'intervalle 5-95 % des placebos du même pays."""
    blocs = ["droite radicale", "gouvernement"]
    ep = (R[R.bloc.isin(blocs) & R.ecart_0_6.notna()]
          .sort_values(["echantillon", "date"], key=lambda c: c.map({"principal": 0, "robustesse": 1,
                                                                     "hors_champ": 2}) if c.name == "echantillon" else c))
    noms = list(dict.fromkeys(ep.episode))
    fig, axes = plt.subplots(1, 2, figsize=(11, 0.42 * len(noms) + 1.6), sharey=True)
    for ax, b in zip(axes, blocs):
        for i, n in enumerate(noms):
            r = ep[(ep.episode == n) & (ep.bloc == b)]
            if r.empty:
                continue
            r = r.iloc[0]
            pl = P[(n, r.bloc_reel)]
            lo, hi = np.percentile(pl, [5, 95])
            ax.plot([lo, hi], [i, i], color="#d9d8d2", lw=6, solid_capstyle="round", zorder=1)
            ax.plot(r.ecart_0_6, i, "o", color="#2a78d6", ms=7, zorder=3)
            if not np.isnan(r.ecart_0_6_sans_tendance):
                ax.plot(r.ecart_0_6_sans_tendance, i, "o", mfc="#fcfcfb", mec="#2a78d6", ms=6, zorder=2)
        ax.axvline(0, color="#c3c2b7", lw=1)
        ax.set_title(b, loc="left", fontsize=10)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.grid(axis="x", color="#e1e0d9", lw=0.6)
        ax.tick_params(length=0)
        ax.set_xlabel("Écart à la tendance d'avant, semaines 0-6 (points)")
    axes[0].set_yticks(range(len(noms)), [f"{n}  [{ep[ep.episode == n].echantillon.iloc[0]}]" for n in noms],
                       fontsize=8)
    axes[0].invert_yaxis()
    h = [plt.Line2D([], [], marker="o", color="#2a78d6", lw=0, ms=7),
         plt.Line2D([], [], marker="o", mfc="#fcfcfb", mec="#2a78d6", lw=0, ms=6),
         plt.Line2D([], [], color="#d9d8d2", lw=6)]
    fig.legend(h, ["avec tendance d'avant", "sans tendance (niveau des 12 dernières semaines)",
                   "placebos du pays, 5-95 %"], frameon=False, ncol=3, loc="lower center", fontsize=8)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(fichier, dpi=150)
    plt.close(fig)


def regroupe(R, P, tirages=10000, graine=1):
    """Moyenne des écarts (semaines 0-6) sur les épisodes d'un échantillon, et sa distribution sous
    l'hypothèse nulle : on tire un placebo par épisode, dans sa propre distribution."""
    rng = np.random.default_rng(graine)
    out = []
    for (ech, bloc), g in R.groupby(["echantillon", "bloc"]):
        ligne = {"echantillon": ech, "bloc": bloc}
        for var, col, suff in (("tendance", "ecart_0_6", ()), ("sans_tendance", "ecart_0_6_sans_tendance",
                                                                ("sans_tendance",))):
            h = g.dropna(subset=[col])
            pls = [P[(e, b, *suff)] for e, b in zip(h.episode, h.bloc_reel)]
            if not len(h) or any(len(p) == 0 for p in pls):
                continue
            moy = h[col].mean()
            nul = np.mean([rng.choice(p, tirages) for p in pls], axis=0)
            ligne.update({f"n_episodes_{var}": len(h), f"ecart_moyen_{var}": moy,
                          f"ecart_type_nul_{var}": nul.std(), f"p_valeur_{var}": (np.abs(nul) >= abs(moy)).mean()})
        ligne["ecart_moyen_6_12"] = g.ecart_6_12.mean()
        ligne["episodes"] = ", ".join(g.dropna(subset=["ecart_0_6"]).episode)
        out.append(ligne)
    return pd.DataFrame(out)


def main(fichier_episodes):
    w = charger()
    ep = pd.read_csv(fichier_episodes, parse_dates=["date"])
    cand = pd.read_csv(ICI / "episodes_candidats.csv", parse_dates=["date_debut"])
    code = {"France": "FR", "Royaume-Uni": "UK", "Allemagne": "DE", "Espagne": "ES", "Italie": "IT"}
    cand["c"] = cand.pays.map(lambda p: code.get(p.split(" (")[0]))
    FIG.mkdir(exist_ok=True)
    lignes, P = [], {}
    for _, e in ep.iterrows():
        x, pages = fenetre(w, e.pays, e.date)
        exclusions = list(cand[cand.c == e.pays].date_debut) + list(ep[ep.pays == e.pays].date)
        gouv = bl.gouvernement(e.pays, e.date.date())
        elec = [d.date() for d in ELECTIONS[e.pays]
                if e.date - pd.Timedelta(weeks=AVANT) < d < e.date + pd.Timedelta(weeks=APRES)]
        effets, pentes = {}, {}
        for col in bl.BLOCS:
            r = ecart(x, col)
            base = {"episode": e.episode, "pays": e.pays, "date": e.date.date(), "echantillon": e.echantillon,
                    "n_avant": int((x.t < 0).sum()), "n_apres": int((x.t >= 0).sum()),
                    "election_dans_fenetre": ", ".join(map(str, elec)), "series": pages}
            if r is None:
                continue
            effets[col], pentes[col] = r[2], r[3]
            pl2 = placebos(w, e.pays, exclusions, e.date)[col]
            pl, pln = pl2[:, 0], pl2[:, 1][~np.isnan(pl2[:, 1])]
            P[(e.episode, col)] = pl
            P[(e.episode, col, "sans_tendance")] = pln
            res = {**base, "ecart_0_6": r[0], "ecart_6_12": r[1], "pente_avant_par_semaine": r[3],
                   "n_placebos": len(pl), "ecart_type_placebo": pl.std() if len(pl) else np.nan,
                   "p_valeur": (np.abs(pl) >= abs(r[0])).mean() if len(pl) else np.nan,
                   "ecart_0_6_sans_tendance": r[4],
                   "p_valeur_sans_tendance": (np.abs(pln) >= abs(r[4])).mean() if len(pln) and not np.isnan(r[4])
                   else np.nan, "bloc_reel": col}
            lignes.append({**res, "bloc": col})
            if col == gouv:
                lignes.append({**res, "bloc": "gouvernement"})
        if not effets:
            lignes.append({"episode": e.episode, "pays": e.pays, "date": e.date.date(),
                           "echantillon": e.echantillon, "n_avant": int((x.t < 0).sum()),
                           "n_apres": int((x.t >= 0).sum()), "bloc": "(sondages insuffisants)"})
        else:
            figure(x, e.date.date(), effets, pentes, f"{e.nom} ({e.pays})", FIG / f"{e.episode}.png")
    R = pd.DataFrame(lignes)
    R.drop(columns="bloc_reel").to_csv(ICI / "resultats.csv", index=False, float_format="%.3f")
    G = regroupe(R[R.bloc != "(sondages insuffisants)"], P)
    synthese(R[R.bloc != "(sondages insuffisants)"], P, FIG / "synthese.png")
    G.to_csv(ICI / "resultats_regroupes.csv", index=False, float_format="%.3f")
    return R, G


if __name__ == "__main__":
    R, G = main(sys.argv[1] if len(sys.argv) > 1 else ICI / "episodes.csv")
    pd.set_option("display.width", 200)
    print(R[["episode", "bloc", "ecart_0_6", "ecart_6_12", "n_avant", "n_apres", "ecart_type_placebo",
             "p_valeur", "election_dans_fenetre"]].round(2).to_string())
    print(G.round(2).to_string())
