# Bloc « fiscalité du capital », v3 : neutralité entre vendre et transmettre

Chiffres : `note8p/calculs/pfu3_neutralite.py` → `sorties/pfu3.json` (table `annuel` 2027-2040) et
`sorties/pfu3_calculs.txt`. Ce script reprend le barème, les jeux d'hypothèses et le calendrier de
`pfu_transmission.py` (v2), qui n'est pas modifié. Le coût d'un point de PFU, la CEHR et la CDHR restent dans
`sorties/pfu.json`. Figure : `figures/g9_exemple_pv` (refaite). Annexe : `annexes/annexe_pfu.tex` (2 pages).
Unités : Md€ au niveau du PIB de 2025.

## 1. Ce qui est conservé [C]

- PFU à 31,4 %.
- Fin de l'effacement de la plus-value à la donation et au décès.
- Reprise du prix d'acquisition historique, sans impôt à la transmission : seule la vente est imposée.
- Option 1 (prix historique pour tous les titres), date d'effet au jour de l'annonce.
- Report d'apport-cession transmis sans s'effacer.
- CEHR et CDHR maintenues sur le capital.

## 2. La règle de neutralité : « correction à la marge » (recommandée) [C]

**Principe.** Le parent qui vend paie `tG + D(V − tG)`. L'héritier qui reçoit puis vend paie `D(V) + t(G − a)`.
Les deux charges sont égales si `t·a = D(V) − D(V − tG)`, c'est-à-dire si l'héritier récupère, quand il vend, les
droits payés sur l'impôt latent. L'idée se dit simplement : la part de l'héritage qui reviendra au fisc ne doit pas
payer de droits de succession.

**Règle.** Le prix repris est majoré de `[droits payés − droits recalculés sur la part diminuée de l'impôt latent] /
PFU`. Le notaire fait un second calcul de droits, et la déclaration porte de toute façon le prix historique. La
majoration suit les titres : ventes partielles au prorata, cumul en cas de nouvelle transmission. Économiquement, c'est
la règle (iv), un crédit à la vente des droits afférents à l'impôt latent, présenté comme un prix pour rester simple.
Elle se confond avec la règle (ii), le taux marginal des droits × la plus-value ajouté au prix, sauf quand le calcul
franchit une tranche.

**Pourquoi pas la règle v2 (taux moyen, § 1015(d)(6)) ?** Elle laisse une double imposition égale à `tG(m − τ̄)`.
L'écart vient de la progressivité et de l'abattement : 24 600 € (6 %) dans l'exemple, presque rien aux taux plats
(neveu, 55 %) ou au taux maximal.

| Charge totale (€), droit de 2026 | Vendre puis transmettre | Transmettre aujourd'hui | Écart avec la 1re colonne : (i) v2 | (iv) retenue | (iii) | (v) forfait 30 % |
|---|---|---|---|---|---|---|
| 100 k€ → 1 M€, un enfant | 410 782 | 212 962 | +24 597 | 0 | 0 | 0 |
| 250 k€ → 400 k€, un enfant | 95 874 | 58 194 | +2 568 | 0 | 0 | −4 710 |
| 2 M€ → 40 M€, deux enfants | 23 997 389 | 17 434 789 | +168 603 | 0 | 0 | +1 789 800 |
| 100 k€ → 1 M€, un frère | 595 818 | 440 388 | +2 716 | 0 | 0 | +42 390 |
| 100 k€ → 1 M€, un neveu | 672 788 | 545 618 | +1 238 | 0 | 0 | +70 650 |
| 100 k€ → 1 M€, conjoint (exonéré) | 282 600 | 0 | 0 | 0 | 0 | −84 780 |

**Les autres règles.**
- **(iii) Déduire l'impôt latent de l'assiette des droits.** La règle est neutre, mais elle coûte 0,8 à 1,1 Md€ par
  an dès 2027, avant toute recette. Elle baisse les droits des héritiers qui ne vendront jamais, au titre d'un impôt
  jamais payé.
- **(v) Forfait de 30 %.** Il n'est juste que par coïncidence (exemple, où m = 30 %). Il fait des cadeaux au conjoint
  et dans les petites successions, et taxe trop les neveux.
- **(vi) Réalisation au décès, avec l'impôt déduit des droits (modèle canadien).** Elle est neutre et rapporterait
  6,4 Md€ par an dès 2028 au centre, mais elle contredit l'imposition à la vente seule. Pour mémoire.

**Si l'héritier ne vend jamais.** Avec (iv), il paie les droits d'aujourd'hui, ni plus ni moins. L'impôt latent reste
attaché aux titres et passe à la génération suivante. Il n'y a ni perte de recette ni impôt nouveau tant qu'il n'y a
pas de vente.

**Taux combinés.** La neutralité ne crée aucun taux nouveau. L'héritier qui vend supporte sur la plus-value
`t + m(1 − t)`, comme tout patrimoine vendu avant le décès : 52 % à 1 M€ en ligne directe, 62 % au taux maximal, 69 %
pour un neveu [S]. Ces taux sont élevés, mais ils existent déjà pour toute succession en liquidités. Fermer
l'effacement les applique aux titres, sans les dépasser.

Titre-message proposé pour g9 : **« Avec la réforme, transmettre puis vendre coûte exactement ce que coûte vendre
puis transmettre ; aujourd'hui, deux fois moins »** (barres : 411 / 213 / 435 [variante au taux moyen] / 411 k€).

## 3. Pacte Dutreil : charge cumulée [S]

| Entreprise familiale transmise sous pacte, cédée par les héritiers après l'engagement | Aujourd'hui | Réforme (iv) | Le fondateur vend avant |
|---|---|---|---|
| 1 M€ (prix 100 k€), un enfant | 28 194 € (3 %) | 296 664 € (30 %) | 410 782 € (41 %) |
| 10 M€ (prix 0,5 M€), deux enfants | 0,63 M€ (6 %) | 3,34 M€ (33 %) | 5,58 M€ (56 %) |

- La correction porte sur les droits réellement payés, faibles sous pacte (m = 5 à 10 %).
- L'écart restant avec la vente avant transmission vient de l'exonération de 75 % elle-même, pas de l'interaction des
  deux impôts. Son sort relève d'une décision sur le pacte, qui n'est pas prise ici.
- Si les héritiers gardent l'entreprise, rien ne change.
- Pour les familles qui cèdent, la hausse est forte (de 3-6 % à 30-33 %) et assumée : le cumul « 75 % d'exonération +
  effacement » disparaît, pas le pacte.

## 4. Recettes, 2027-2040 (Md€) [S sur hypothèses H]

| | 27 | 28 | 29 | 30 | 31 | 32 | 33 | 34 | 35 | 36 | 37 | 38 | 39 | 40 | Cumul |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Bas | 0 | 0,19 | 0,44 | 0,49 | 0,54 | 0,58 | 0,63 | 0,67 | 0,72 | 0,76 | 0,80 | 0,85 | 0,89 | 0,93 | 8,5 |
| **Central** | 0 | 0,82 | 1,83 | 2,01 | 2,19 | 2,36 | 2,52 | 2,68 | 2,83 | 2,97 | 3,11 | 3,24 | 3,37 | 3,50 | 33,4 |
| Haut | 0 | 2,51 | 5,53 | 6,02 | 6,48 | 6,91 | 7,31 | 7,69 | 8,05 | 8,38 | 8,70 | 9,00 | 9,28 | 9,54 | 95,4 |
| **Prudent (bouclage)** | 0 | 0 | 0 | 0,19 | 0,44 | 0,49 | 0,54 | 0,58 | 0,63 | 0,67 | 0,72 | 0,76 | 0,80 | 0,85 | 6,7 |

- **Coût de la neutralité par rapport à la v2.** Il est de 1,6 Md€ cumulés au centre (0,6 à 2,1), soit environ
  0,3 Md€ par an en régime de croisière. Hypothèse : taux marginal effectif des droits m = 1,4 × le taux moyen τ̄ [H],
  rapport tiré des cas-types (1,0 à 1,8).
- **Scénario prudent.** C'est le jeu bas, encaissé deux ans plus tard : la recette est constatée en N+1 et réutilisée
  en N+2. Ces recettes ne servent qu'une fois constatées (CADRE). Pour le bouclage, ligne `fin_effacement_prudent`.
  La clé `fin_effacement_central` de pfu3.json remplace celle de pfu.json : 3,50 au lieu de 3,66 en 2040.

## 5. Localisation des très grands patrimoines : prudence qualitative

**Littérature vérifiée [E].**
- **Jakobsen, Kleven, Kolsrud, Landais et Muñoz** (NBER WP 32153 ; *AER* 116(10), 2026, d'après la page NBER) : un
  point d'impôt sur la fortune en plus réduit d'environ 2 % le nombre de contribuables fortunés (Suède, Danemark). Les
  effets agrégés sont faibles (valeur ajoutée −0,1 % au plus). Une version du papier indique 0,22 $ perdus par dollar
  levé (chiffre lu sur un résumé, à confirmer selon la version).
- **Agrawal, Foremny et Martínez-Toledano** (*AEJ: Applied* 17(1), 2025) : Madrid, seule région espagnole sans impôt
  sur la fortune après 2011, gagne 7,5 % de contribuables fortunés en six ans. L'élasticité est de 0,36 par rapport au
  taux net d’impôt sur les revenus du capital (chiffres du document de travail CESifo 11048, 2024).
- **Moretti et Wilson** (*AEJ: Policy* 15(2), 2023) : 35 % des milliardaires du Forbes 400 quittent les États qui
  gardent un impôt successoral après 2001. L'impôt reste pourtant rentable pour la plupart des États.
- **Agrawal et Foremny** (Spanish top income tax rates ; document de travail lu) : élasticité de 0,85 du nombre de
  hauts revenus au taux net.
- **Kleven, Landais, Saez et Schultz** (*QJE* 129(1), 2014) : 1,5 à 2 pour les étrangers très bien payés au Danemark.
  Ce groupe est bien plus mobile que les nationaux.
- **France.**
  - CAE, Focus n° 118 (2025) : 0,02 à 0,23 % du dernier centile part en plus par point d'imposition effective.
  - France Stratégie (2023) : depuis 2018, les retours de redevables de l'IFI dépassent les départs (380 contre 260
    par an). Sous l'ISF, on comptait 950 départs par an.
  - Rien ne mesure le dernier dix-millième, qui détient l'essentiel de l'impôt latent.

**Transposabilité : faible.** Ces élasticités portent sur des impôts annuels sur le stock ou le revenu. Ici, l'impôt
est payé une fois par génération, à la vente, et il est évitable en ne vendant pas. Leur message commun est que la
mobilité est réelle au sommet, mais qu'elle n'annule pas la recette. **Aucune élasticité n'est appliquée** :
parcimonie, aucun calibrage transposable. La prudence passe par le scénario prudent ci-dessus et par deux gardes [C].
- **Exit tax (art. 167 bis).** Porter le délai de dégrèvement à 15 ans pour les participations de plus de 2,57 M€
  (aujourd'hui 2 ans, 5 au-delà de ce seuil [S : sources secondaires, texte non relu] ; 15 ans de 2014 à 2018,
  secondaire). La plus-value reprise entre dans sa base.
- **Bénéficiaires non résidents.** Imposer, dans les limites des conventions (non vérifiées), la plus-value transmise
  à un bénéficiaire non résident. À expertiser.

## 6. Hypothèses retirées ou non utilisées (parcimonie)

- Pas de modèle de migration, pas d'élasticité de départ appliquée aux recettes, pas de « taux de fuite ».
- Pas de sensibilité sur des comportements non établis : avancement des donations, report vers l'assurance-vie.
  Ils sont cités comme risques et ne sont pas chiffrés.
- Une seule hypothèse nouvelle : m = 1,4 τ̄. Elle ne fait varier la recette que de 0,3 Md€ par an.

## 7. Limites

- La recette dépend de cinq hypothèses non mesurées (fourchette de 0,9 à 9,5 Md€ en 2040).
- Les seuils du barème des droits et les paramètres Dutreil (LF 2026) et de l'exit tax proviennent de sources
  secondaires.
- La constitutionnalité de l'option 1 n'a pas été expertisée.
- La majoration est calculée avec le PFU en vigueur à la transmission. Si le PFU change, en particulier à la fin de la
  CRDS en 2033, la neutralité n'est qu'approchée.
- La règle neutralise les deux chemins à valeur constante. Le report de l'impôt pendant la détention reste un
  avantage, comme pour tout détenteur.
