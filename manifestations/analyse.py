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
    s = pd.read_csv(ICI / "sondages.csv.gz", parse_dates=["date"])
    s["bloc"] = [bl.bloc(p, str(x)) for p, x in zip(s.pays, s.parti)]
    s = s[s.bloc.notna() & (s.bloc != "non classé")]
    w = (s.groupby(["pays", "page", "institut", "date", "bloc"]).part.sum()
         .unstack("bloc").fillna(0).reset_index())
    return w


def fenetre(w, pays, jour, page=None):
    jour = pd.Timestamp(jour)
    x = w[(w.pays == pays) & (w.date >= jour - pd.Timedelta(weeks=AVANT))
          & (w.date < jour + pd.Timedelta(weeks=APRES))]
    if page is None:
        if x.empty:
            return x, None
        page = x.page.value_counts().index[0]
    x = x[x.page == page].copy()
    avant = [d for d in ELECTIONS[pays] if d < jour]
    apres = [d for d in ELECTIONS[pays] if d >= jour]
    if avant:
        x = x[x.date > max(avant)]
    if apres:
        x = x[x.date < min(apres)]
    x["t"] = (x.date - jour).dt.days / 7
    return x, page


def ecart(x, col):
    """Écart à la tendance d'avant : (semaines 0-6, semaines 6-12, ajustement, pente)."""
    av, ap = x[x.t < 0], x[x.t >= 0]
    if len(av) < MIN_AVANT or len(ap) < MIN_APRES or col not in x or x[col].abs().sum() == 0:
        return None
    inst = sorted(av.institut.unique())
    X = np.column_stack([(np.asarray(av.institut, dtype=object)[:, None] == np.array(inst, dtype=object)).astype(float), av.t.values])
    coef, *_ = np.linalg.lstsq(X, av[col].values, rcond=None)
    effet, pente = dict(zip(inst, coef[:-1])), coef[-1]
    ap = ap[ap.institut.isin(inst)]
    if len(ap) < MIN_APRES:
        return None
    r = ap[col].values - (ap.institut.map(effet).values + pente * ap.t.values)
    e1 = r[ap.t.values < 6].mean() if (ap.t.values < 6).any() else np.nan
    e2 = r[ap.t.values >= 6].mean() if (ap.t.values >= 6).any() else np.nan
    return e1, e2, effet, pente


_CACHE = {}


def placebos(w, pays, page, dates_episodes, centre):
    """Écarts (semaines 0-6) à toutes les dates placebo de la série, pour chaque bloc."""
    cle = (pays, page, centre)
    if cle in _CACHE:
        return _CACHE[cle]
    serie = w[(w.pays == pays) & (w.page == page)]
    debut = max(serie.date.min() + pd.Timedelta(weeks=AVANT), centre - pd.DateOffset(years=PLACEBO_ANNEES))
    fin = min(serie.date.max() - pd.Timedelta(weeks=APRES), centre + pd.DateOffset(years=PLACEBO_ANNEES))
    out = {c: [] for c in bl.BLOCS}
    for jour in pd.date_range(debut, fin, freq="W-MON"):
        if any(abs((jour - d).days) < 7 * EXCLUSION_PLACEBO for d in dates_episodes):
            continue
        if any(jour - pd.Timedelta(weeks=AVANT) < d < jour + pd.Timedelta(weeks=APRES) for d in ELECTIONS[pays]):
            continue
        x, _ = fenetre(w, pays, jour, page)
        for c in bl.BLOCS:
            e = ecart(x, c)
            if e is not None and not np.isnan(e[0]):
                out[c].append(e[0])
    _CACHE[cle] = {c: np.array(v) for c, v in out.items()}
    return _CACHE[cle]


def figure(x, jour, effets, pentes, titre, fichier):
    cols = [c for c in bl.BLOCS if c in x and x[c].sum() > 0]
    fig, ax = plt.subplots(figsize=(9, 5))
    couleurs = dict(zip(bl.BLOCS, ["#5b3a8e", "#2a78d6", "#eda100", "#e34948", "#9b1c1c", "#898781"]))
    for c in cols:
        if c not in effets:
            continue
        aj = x[c] - x.institut.map(effets[c]).fillna(0) + np.mean(list(effets[c].values()))
        sem = aj.groupby(np.floor(x.t)).mean()
        ax.plot(sem.index, sem.values, color=couleurs[c], lw=1.8, label=c)
        base = np.mean(list(effets[c].values()))
        tt = np.array([-AVANT, APRES])
        ax.plot(tt, base + pentes[c] * tt, color=couleurs[c], lw=1, ls="--")
    ax.axvline(0, color="#52514e", lw=1)
    ax.set_xlabel(f"Semaines autour de l'émeute ({jour})")
    ax.set_ylabel("Intentions de vote (%), corrigées des effets institut")
    ax.set_title(titre, loc="left", fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, fontsize=8, ncol=3)
    fig.tight_layout()
    fig.savefig(fichier, dpi=140)
    plt.close(fig)


def main(fichier_episodes):
    w = charger()
    ep = pd.read_csv(fichier_episodes, parse_dates=["date"])
    FIG.mkdir(exist_ok=True)
    lignes = []
    for _, e in ep.iterrows():
        x, page = fenetre(w, e.pays, e.date)
        if page is None:
            continue
        gouv = bl.gouvernement(e.pays, e.date.date())
        effets, pentes = {}, {}
        for col in bl.BLOCS:
            r = ecart(x, col)
            if r is None:
                continue
            effets[col], pentes[col] = r[2], r[3]
            pl = placebos(w, e.pays, page, list(ep[ep.pays == e.pays].date), e.date)[col]
            elec = [d.date() for d in ELECTIONS[e.pays]
                    if e.date - pd.Timedelta(weeks=AVANT) < d < e.date + pd.Timedelta(weeks=APRES)]
            lignes.append({"episode": e.episode, "pays": e.pays, "date": e.date.date(), "page": page,
                           "election_dans_fenetre": ", ".join(map(str, elec)),
                           "bloc": col, "gouvernement": col == gouv,
                           "ecart_0_6": r[0], "ecart_6_12": r[1], "pente_avant": r[3],
                           "n_avant": int((x.t < 0).sum()), "n_apres": int((x.t >= 0).sum()),
                           "n_placebos": len(pl), "ecart_type_placebo": pl.std() if len(pl) else np.nan,
                           "p_valeur": (np.abs(pl) >= abs(r[0])).mean() if len(pl) else np.nan})
        if effets:
            figure(x, e.date.date(), effets, pentes, e.episode, FIG / f"{e.episode}.png")
    R = pd.DataFrame(lignes)
    R.to_csv(ICI / "resultats.csv", index=False, float_format="%.3f")
    return R


if __name__ == "__main__":
    print(main(sys.argv[1]).round(2).to_string())
