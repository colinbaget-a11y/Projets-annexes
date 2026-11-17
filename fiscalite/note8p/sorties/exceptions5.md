# Les trois exceptions réexaminées (v5, 17/11/2026)

Script : `calculs/ircsg5_exceptions.py` (exécute `ircsg4_modele.py` jusqu'au barème final, sans réécrire ses sorties) ;
chiffres : `sorties/exceptions5.json`. Montants en Md€ 2025, recette statique de l'impôt du barème final v4
(financement externe 7,0 Md€), régime de croisière (λ = 1, soit 2030 avec la montée en charge de la fusion) ;
« + » = recette en plus par rapport au modèle v4. Ordre de grandeur de conversion : 1 point de baisse uniforme des taux
marginaux aux repères 0 à 3,5 Smic ≈ 13,6 Md€.

## 1. Frais professionnels des salariés

| Option (barème final v4) | Déduction | Déclarants frais réels | Recette vs v4 | Baisse uniforme (pt, 0-3,5 Smic) |
|---|---|---|---|---|
| v4 : forfait supprimé, frais réels gardés | 65,4 | 18,2 M | 0 | — |
| Aucune déduction | 0 | 0 | **+15,2** | 1,12 |
| Forfait de 300 € pour tout salarié, sans frais réels | 10,4 | 0 | +13,0 | 0,97 |
| **Forfait de 500 €, sans frais réels** | 17,3 | 0 | **+11,6** | **0,87** |
| Forfait de 1 000 €, sans frais réels | 34,6 | 0 | +8,0 | 0,61 |
| Abattement de 1,75 % (type CSG), plafond 4 PASS | 15,4 | 0 | +11,2 | 0,83 |
| Frais réels au-delà d'une franchise de 2 000 € | 31,2 | 9,1 M | +7,7 | 0,58 |
| Frais réels au-delà d'une franchise de 5 000 € | 8,2 | 3,7 M | +13,2 | 0,98 |
| Forfait de 500 € ou frais réels | 71,4 | 15,2 M | −1,0 | — |

Sensibilité [H] : si le recours aux frais réels est deux fois moins élastique (seuil de gain doublé), la v4 n'attire que
13,1 M de déclarants et la suppression totale rapporte 13,7 Md€ au lieu de 15,2. Taux marginal moyen apparent de la
déduction v4 : 23 %. 14 % des salariés ont, dans le modèle de frais [H], plus de 5 000 € de frais simulés (trajets
longs en voiture) : ce sont eux qui perdent à la suppression (pour 8 000 € de frais à 30 %, 2 400 € par an).

Droit vérifié :
- CSG : assise depuis 1991 sur le salaire brut avec une seule « réduction représentative de frais professionnels »
  forfaitaire (5 % à l'origine, 1,75 % aujourd'hui jusqu'à 4 PASS ; article du CSS cité par des sources secondaires,
  L. 136-1-1, non relu sur Légifrance). Le Conseil constitutionnel l'a admis (déc. n° 90-285 DC du 28/12/1990,
  cons. 32-35) : asseoir la contribution sur le brut, « moyennant » une déduction forfaitaire « représentative de frais
  professionnels », ne crée « pas de disparité manifeste » avec les indépendants imposés sur leur revenu net.
- Déc. n° 2012-662 DC du 29/12/2012, cons. 28-30 : plafonnement du barème kilométrique à 7 CV (art. 6 LF 2013) jugé
  conforme ; salariés et indépendants « ne se trouvent pas dans une situation identique » pour la détermination du
  revenu imposable.
- Aucune décision trouvée imposant la déduction des frais réels de l'impôt sur le revenu. La 90-285 DC s'appuie
  toutefois sur l'existence d'un forfait : un abattement forfaitaire, même petit, est la voie la plus sûre.

Recommandation : **supprimer les frais réels et instaurer un forfait de 500 € par salarié** (≈ l'abattement de 1,75 %
de la CSG au salaire médian), +11,6 Md€ par rapport à la v4 (+6,5 Md€ par rapport au maintien des frais réels au
niveau actuel), soit 0,87 point de baisse uniforme des taux.

## 2. Engagements d'investissement locatif en cours

Hors modèle (avantages gardés, retirés de la recette à tenir). Voies et moyens PLF 2026, coûts 2024/2025/2026 (M€) :
Pinel-Duflot 1 469/1 459/1 349 (fin du fait générateur 2024, fin d'incidence 2038) ; Scellier 34/30/38 et
Scellier intermédiaire 189/169/176 (incidence jusqu'en 2051) ; Scellier OM intermédiaire 41/37/37 ; Censi-Bouvard
39/35/37 (2035) ; Denormandie 5/5/7 (fait générateur jusqu'en 2027, incidence 2039). Stock métropolitain 2026 :
1,64 Md€. Calendrier de suppression [H : extinction linéaire, Pinel à 2038, Scellier à 2031] : 1,47 Md€ en 2027,
1,13 en 2029, 0,79 en 2031, 0,46 en 2034, ≈ 0 en 2038 ; cumul 2027-2038 ≈ 8 Md€. Pas de régime de croisière : la recette
est transitoire (≈ 0,1 point de barème en 2027). Girardin industriel (0,83 Md€) : déjà supprimé dans la v4 pour les
investissements futurs ; seuls les reports de réductions acquises s'imputent (profil 60/80/90/100 %).

Droit vérifié : déc. n° 2013-682 DC du 19/12/2013, cons. 14 : le législateur ne saurait, « sans motif d'intérêt général
suffisant, ni porter atteinte aux situations légalement acquises ni remettre en cause les effets qui peuvent
légitimement être attendus de telles situations » (art. 16 DDHC) ; cons. 17-18 : pour l'assurance-vie, un motif
« exclusivement financier » n'est pas un intérêt général suffisant (réserve d'interprétation). Déc. 2012-662 DC,
cons. 107-108 : aucune règle constitutionnelle n'impose le maintien d'avantages fiscaux pour l'avenir. La réduction
Pinel est la contrepartie d'un engagement de location de 6 ou 9 ans sous plafonds de loyer : son retrait en cours
d'engagement, pour un motif de recette, serait très exposé. Non trouvé : une décision sur le retrait d'une réduction
d'impôt étalée en cours d'engagement ; non vérifié : le statut des prorogations Pinel non encore exercées.

Recommandation : **garder les engagements en cours** (coût 1,5 Md€ en 2027, nul en 2038), mais fermer toute entrée
nouvelle dès l'annonce (Denormandie ouvert jusqu'à fin 2027 par le droit actuel) et ne pas ouvrir de prorogation
nouvelle.

## 3. Épargne retraite (PER)

Le modèle déduit 10,58 Md€ (2024) de cases 6NS à 6QU et 6OS ; seules 6NS-6NU (7,10 Md€, 1,7 M de déclarants) et
6RS-6RU (1,00 Md€) sont des versements individuels déduits du revenu global ; 6QS-6QU (régimes obligatoires d'entreprise,
1,55) et 6OS-6OU (cotisations déduites des revenus d'indépendants, 0,94) ne servent, à notre connaissance, qu'au calcul
du plafond [non vérifié sur la notice 2042 : à contrôler, car le modèle les déduit aussi]. La VM ne chiffre pas
l'art. 163 quatervicies (code 100112, sans fiche : modalité de calcul de l'impôt).

Suppression de la déduction des versements individuels (8,28 Md€ en 2025) : **+2,47 Md€** (taux marginal apparent
30 %), 0,19 point de baisse uniforme ; avec la suppression des frais : +17,8 Md€.

Droit et neutralité (service-public.gouv.fr, fiche F34982 vérifiée le 12/10/2026) : le PER connaît déjà les deux
régimes. Versements déduits : capital imposé au barème à la sortie (EET). Versements non déduits (renonciation
possible à chaque versement) : capital correspondant « exonéré d'impôt sur le revenu et de prélèvements sociaux »,
gains au prélèvement forfaitaire (TEE). Supprimer la déduction sans exonérer la sortie imposerait deux fois les mêmes
euros ; basculer les versements futurs en TEE n'impose qu'une fois. À taux marginal égal à l'entrée et à la sortie,
EET et TEE ont la même valeur actualisée : le gain de la bascule est un gain de trésorerie (2,5 Md€ par an au début,
qui s'érode à mesure que sortent, exonérés, les versements non déduits, sur 20 à 40 ans) ; dans le barème final, le
taux marginal à 30-60 k€ (24-35 %) est voisin du taux apparent des déposants (30 %), d'où un gain actualisé proche de
zéro [S]. L'argument de l'imposition à la sortie vaut donc pour la neutralité, pas pour la recette.

Recommandation : **PER en TEE pour les versements futurs** (régime actuel des versements non déduits), versements déjà
déduits imposés à la sortie comme prévu. Recette +2,5 Md€ par an au départ, décroissante, quasi nulle en valeur
actualisée ; gain de simplicité (plus de plafond à suivre ni de report de plafonds non utilisés). Variante neutre pour
le budget à long terme : garder la déduction (EET), cohérente avec l'imposition à la sortie.
