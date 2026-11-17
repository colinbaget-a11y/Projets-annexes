# Bloc « fiscalité immobilière », v4 : ce qui change (scénario central B_E10)

*Scripts : `calculs/foncier4_calculs.py` (→ `foncier4.json`, `foncier4_journal.txt`, `foncier4_taux_loyers.csv`),
`foncier4_figures.py` (g10b), `foncier4_annexe.py` (→ `annexes/annexe_foncier.tex`). Les autres chiffres restent ceux
de `foncier3.json`, clé `B_E10`. Données ajoutées : `calculs/donnees_oat10_bce.csv` (BCE, taux long France).
`foncier3_figures.py` a maintenant `--rec B_E10` par défaut (g4, g5, g6 étaient déjà en B_E10).*

## 1. Cohérence avec B_E10

- **Note** : tous les chiffres foncier sont en B_E10 (190 € en moyenne, 135 € médiane, Massy +350 €, taux 0,16 %,
  854 € pour construire contre 1 040 en base unique, 1 450 € pour un terrain nu, g5 « 200 à 500 € », table de
  trajectoire). **Une seule phrase à corriger** : « la valeur des logements des ménages pourrait baisser de l'ordre de
  1 à 2,3 % » reposait sur κ = 50 % et κ = 0 ; voir § 2.
- **Annexe** : elle était centrée sur B_E12 (tableaux, cas-types, dispersion, consommation). Elle est régénérée
  entièrement sur B_E10. Les autres enveloppes (B 9, 12, 15, 18) et l'architecture A sont dans un seul tableau de variantes.

## 2. Capitalisation [S sur hypothèses H]

- **Taxe sur le sol** : perte −E/r pour le propriétaire en place à l'annonce ; l'acheteur suivant paie moins cher et
  n'y perd rien. Logements des ménages : −207 Md€ (−2,3 % ; −155 si r = 4 %).
- **Droits** : payés à la vente seulement. Un bien vendu au taux ρ par an vaut Δτ·P·ρ/r de plus si les prix intègrent
  toutes les ventes futures. Il y a donc capitalisation « euro pour euro » *en moyenne*, mais proportionnelle à la
  rotation de chaque bien, pas à sa valeur. **Point mort** : un propriétaire gagne si son bien change de main plus
  souvent que tous les H* = Δτ·P/ΔTF ans (indépendant de r). Massy 22 ans, Ste-Geneviève 27 ; médiane du parc 43 ans.
- **Rotation** [S, DVF 2025] : 3,1 % de la valeur du parc vendue par an, soit un changement de main tous les 32 ans
  (communes P10-P90 : 1,7-4,5 %). Les biens revendus avaient été détenus 13,7 ans (appartements) et 15,8 ans (maisons)
  en Île-de-France en 2024 [E, Notaires du Grand Paris ; pas de série nationale trouvée]. L'écart vient des logements
  gardés jusqu'au décès. Appliquer 10-15 ans à tout le parc surestimerait le gain d'un facteur 3 à 4.
- **Trois hypothèses d'incidence** (logements des ménages, r = 3 %) :

| | Droits | Net | % valeur | Logements gagnants |
|---|---|---|---|---|
| (a) prix rigides (France 2014 : l'acheteur a tout supporté, Bachelet-Poulhès) | 0 | −207 | −2,3 % | 10 % |
| **(b) le vendeur capte l'économie de son seul acheteur (central)** | +100 | **−107** | **−1,2 %** | 30 % |
| (c) toutes les ventes futures capitalisées (ordre de grandeur de Dolls et al., 2025) | +219 | +11 | +0,1 % | 56 % |

  (c) est l'ancien κ = 100 %, qui devient la borne haute. La répartition change : les communes bon marché gagnent
  (+0,2 à +0,8 % dans les trois premiers dixièmes en (b)), les dixièmes chers perdent 2 à 2,6 %. Consommation (0,7 à 1,4
  centime par euro) : −0,7 à −1,5 Md€ par an en (b), avant recyclage.

**Phrase proposée pour la note** (remplace « baisser de l'ordre de 1 à 2,3 % … ») : « À l'annonce, la valeur des
logements des ménages baisserait de l'ordre de 1 % : 2,3 % pour la seule taxe, compensés en partie par la baisse des
droits, qui profite d'autant plus à un bien qu'il est souvent revendu. Les propriétaires des communes bon marché y
gagnent ; ceux qui ne vendent presque jamais là où le sol est cher perdent jusqu'à 2 à 3 %. »

## 3. Valeur du sol : rentes ou taux ? (figure g10b, annexe)

De 1998 à 2025, prix des logements anciens ×3,0, loyers (IPC) ×1,5 : le rapport loyers/prix est divisé par deux.
L'OAT à 10 ans passe de 4,6 % à −0,1 % (2020) puis 3,4 % (2025) [E]. **Phrases proposées** (remplacent « La rente
foncière, elle, a explosé ») : « **La valeur du sol bâti a quadruplé rapportée au PIB (figure g10).** Ce n'est pas que la
rente annuelle a explosé : les loyers n'ont progressé que de moitié quand les prix triplaient ; la baisse des taux
d'intérêt et l'anticipation de loyers futurs ont gonflé la valeur de rentes qui, elles, ont crû lentement, et la
remontée des taux depuis 2022 en a effacé une partie. » La part propre des rentes courantes ne peut pas être isolée
avec ces séries (indice de loyers à qualité constante, qui sous-estime les relocations).

## 4. IFI

2,2 Md€ en 2024 (186 000 foyers, patrimoine net taxable 467 Md€, taux moyen 0,47 %) ; 2,3 Md€ en 2025 (193 600 foyers)
[E, DGFiP, lu dans des sources secondaires]. À recette égale, le remplacer demanderait environ +0,04 point sur le sol.
**Deux phrases pour la note** : « L'IFI taxe le bâti comme le sol, net des dettes, et ne touche qu'une fraction des
propriétaires : une taxe sur la valeur du sol remplit mieux sa fonction. À terme, une fois les nouvelles valeurs
fiables, elle pourrait s'y substituer ; ce choix, qui répartit la charge sur tous les propriétaires, n'est pas compté
dans notre financement. »

## 5. Sources ajoutées

- Notaires du Grand Paris (2024), durée de détention des biens revendus (via paris.notaires.fr, focus immobilier).
- BCE, Data Portal, série IRS.M.FR.L.L40.CI.0000.EUR.N.Z (téléchargée).
- Insee, indices Notaires-Insee et IPC loyers (`lvt/donnees/indices.csv`, déjà dans le dépôt).
- DGFiP, IFI 2024 et 2025 (vie-publique.fr, Previssima 21/4/2026) : chiffres secondaires, publication DGFiP non relue.
- Bachelet et Poulhès (2017) ; Dolls, Fuest, Krolage et Neumeier (2025, *JUE* 145) : `foncier/notes/droits_mutation.md`.
