# Fiche 5 : « impôt de 25 % sur les plus-values et les revenus non réinvestis des holdings ». Chiffrage rapide

*17/11/2026. Statuts : [V] texte lu ; [D] chiffre du dépôt déjà vérifié (`pfu/notes/pfu_recherche.md`,
`pfu/sorties/calculs_pfu.json`, `sorties/pfu*.md`) ; [S] source secondaire ; [C] calcul ; [H] hypothèse. Unités : Md€ par an,
revenus de 2025 sauf mention.*

## 1. Ce que « 25 % » change par rapport au droit de 2026

- **Particuliers.** Plus-values de valeurs mobilières au PFU de **31,4 %** : 12,8 % d'IR (art. 200 A) + 18,6 % de
  prélèvements sociaux (LFSS 2026, art. 12) [D, texte lu dans une session antérieure]. Plus CEHR (3-4 %) et CDHR en haut.
  « 25 % » est donc **une baisse** s'il s'agit du taux global, **une hausse** (25 + 18,6 = 43,6 %) s'il remplace la seule
  part d'IR.
- **Sociétés (holdings comprises).** Plus-values nettes à long terme de cession de titres de participation **imposées à
  0 %**, sous réserve d'une **quote-part de frais et charges de 12 %** du montant brut des plus-values, réintégrée au
  taux normal [V, BOI-IS-BASE-20-20-10-20 du 03/04/2024], soit **3 %** effectifs au taux de 25 % [C]. La durée de
  détention de 2 ans n'est pas relue sur le texte. Dividendes mère-fille : quote-part de 5 %, soit 1,25 % [D, rapport AN
  n° 3056]. Pour les holdings, 25 % serait donc une hausse de 22 points sur les plus-values et de 23,75 points sur les
  dividendes conservés.

## 2. Plus-values des ménages : assiette, recette actuelle, variantes

- **Assiette** [D] : case 3VG (revenus 2024) 18,78 Md€ (200 368 foyers), plus 0,37 d'actifs numériques, moins 1,44 de
  moins-values (3VH), soit **17,7 Md€** nets. Pour les revenus de 2025, **13,0 Md€** estimés (3VG de 2024 évoluée comme
  les « revenus divers » de DGFiP Statistiques n° 53, −26 %, données provisoires). À cela s'ajoutent 22,2 Md€ placés en
  report d'apport-cession (3WH, 9 571 foyers), qui ne paient rien aujourd'hui. Concentration : 0,01 % des foyers déclare
  70 % des plus-values de droit commun (France Stratégie, 2023) [D].
- **Recette actuelle sur les plus-values** [C] : 31,4 % × 13,0 = **4,1 Md€** (1,7 d'IR, 2,4 de prélèvements sociaux) ;
  5,6 sur l'assiette de 2024. Majorant : les foyers qui optent pour le barème ne sont pas isolés.
- **Élasticité des réalisations** [S, résumé lu] : Agersnap et Zidar (*AER: Insights* 3(4), 2021), élasticité de long
  terme des réalisations au taux de −0,3 à −0,5 (États-Unis) ; taux maximisant la recette de 38 à 47 %. L'effet d'annonce
  de court terme est plus fort (ventes avancées avant une hausse, différées avant une baisse). Aucune estimation française
  sur les plus-values n'a été retrouvée ; l'IPP (note 46) ne trouve pas d'effet de la réforme de 2013 sur les plus-values
  [D]. Transposition à la France : hypothèse [H].

| Variante (plus-values seules ; e = −0,3 / −0,5) | Statique | Après réaction des réalisations |
|---|---|---|
| A. 25 % **remplace** le PFU (IR ramené à 6,4 %) | −0,8 (−1,1 sur 2024) | **−0,4 à −0,6** (−0,6 à −0,8) |
| B. 25 % d'IR **+ 18,6 %** de prélèvements sociaux = 43,6 % | +1,6 (+2,2) | **+0,7 à +1,1** (+1,0 à +1,4) |

[C : recette = t × B × (t / 31,4 %)^(−e) − 4,1.] La variante B casse le taux unique du PFU (dividendes et intérêts restant
à 31,4 %), porte le taux du haut à 47,6 % avec la CEHR, et renforce le verrouillage tant que l'effacement au décès existe.

## 3. Holdings : ordres de grandeur

- **Nombre** : environ 62 000 holdings fin 2018 (76 % de 82 000 sociétés financières appartenant à des groupes) [V,
  Insee, *Les entreprises en France* 2020, fiche 1 ; C pour le produit]. Les holdings patrimoniales ne sont pas isolées.
  Le Gouvernement estimait à **environ 4 000 foyers** les utilisateurs des montages visés par la taxe initiale de 2 %
  (rendement attendu 1 Md€ ; 100 M€ après recentrage sur les biens somptuaires, art. 235 ter C) [S, LégiFiscal 16/10/2025 ;
  D, PLF 2027 état A].
- **Dividendes remontés** : la quote-part rapporterait 1,5 Md€ pour le régime mère-fille [D, AN n° 3056], ce qui suppose
  environ 120 Md€ de dividendes exonérés [C : 1,5 / 1,25 %], **tous groupes confondus**, opérationnels compris. La part
  conservée dans des holdings patrimoniales et la **trésorerie non distribuée** ne sont pas publiées : aucune statistique
  DGFiP, Banque de France ou FARE (Ésane) isolant les holdings patrimoniales n'a été trouvée [non vérifié plus avant].
- **Report d'apport-cession** [D, AN n° 3056] : 33,6 Md€ mis en report en 2023, 22,2 en 2024 ; **stock de 153 Md€** ; 84
  foyers concentrent 23,5 Md€ (2023) ; reports expirés 0,4 à 1,5 Md€ par an. Point clé : la holding reçoit les titres à
  leur valeur d'apport, si bien qu'un impôt de 25 % sur **ses** plus-values **ne touche pas** ce stock latent, qui est
  personnel et s'efface au décès. Le levier est l'expiration du report à la transmission (PLF 2027, art. 5, rendement
  annoncé de 0,5 Md€ en 2027 [S], première partie rejetée le 04/11/2026 [D]) ou la fin de l'effacement (bloc PFU v3).
- **Rendement d'une hausse à 25 % des plus-values des holdings** : non chiffrable faute d'assiette. Repère [C] : +2,2 Md€
  statiques par tranche de 10 Md€ de plus-values imposées (22 points), avant toute réaction. Or c'est l'impôt le plus
  facile à éviter : il suffit de ne pas vendre.

## 4. Paramètres et points d'attention

- **Secteurs « stratégiques »** : une liste sectorielle serait arbitraire et exposée au droit de l'Union (liberté
  d'établissement, aides d'État) [non expertisé]. Repère existant : les activités de l'art. 199 terdecies-0 A, déjà
  retenues par la LF 2026 pour le réinvestissement de 70 % en 3 ans de l'apport-cession [D, S]. Seuil de champ possible :
  5 M€ d'actifs et revenus passifs majoritaires, comme l'art. 235 ter C [S] ; délai de distribution de 18 mois sur le
  modèle irlandais [S, non relu].
- **Double imposition** [C] : bénéfice de la filiale à l'IS (25 %), puis 25 % dans la holding, puis PFU à la
  distribution : 1 − 0,75 × 0,75 × 0,686 = **61,4 %**, contre 48,6 % pour un dividende versé directement. Il faut un
  crédit ou une exonération à la distribution (impôt-acompte), sinon la mesure pousse à ne jamais distribuer.
- **Mère-fille** : la directive 2011/96/UE plafonne la quote-part à 5 % ; une taxe sur les flux remontés s'y heurte, une
  taxe sur la personne morale ou ses actifs passifs non (DLF, rapportée par AN n° 3056) [D]. L'imposition des bénéfices non
  distribués chez l'associé est fermée par la jurisprudence de 2012 [D].
- **Effacement au décès** : tant qu'il existe, toute hausse du taux à la vente accroît la prime à garder les titres
  jusqu'au décès ; la fin de l'effacement (bloc PFU v3) doit précéder toute hausse.
- **Relocalisation et blocage des cessions** : départ de la holding ou de l'associé (exit tax : 2 ans, 5 ans au-delà de
  2,57 M€, sursis dans l'UE [S]) ; verrouillage des participations (vendre devient plus cher que garder). Aucune
  élasticité française n'est disponible pour les holdings.

## 5. Recommandation

Ne pas retenir l'instrument tel quel. Côté ménages, 25 % en remplacement du PFU coûte 0,4 à 0,8 Md€ ; 25 % en plus des
prélèvements sociaux rapporte 0,7 à 1,4 Md€ mais rompt le taux unique et contredit la contrainte de mobilité. Côté
holdings, l'assiette est inconnue et l'impôt est évitable en ne vendant pas. L'objectif visé, le circuit des holdings,
passe mieux par (1) la fin de l'effacement et l'expiration du report d'apport-cession à la transmission, déjà dans la
note, et (2) un prélèvement modéré sur la **trésorerie passive** des holdings patrimoniales contrôlées (AN n° 3056,
rec. 19), imputable sur l'impôt dû à la distribution. Chiffrer (2) demande des données DGFiP (liasses des holdings
patrimoniales) qui ne sont pas publiques.

## Sources

- BOFiP, BOI-IS-BASE-20-20-10-20 (03/04/2024) : https://bofip.impots.gouv.fr/bofip/4948-PGP.html [V]
- Insee, *Les entreprises en France* 2020, fiche 1 (groupes) : https://www.insee.fr/fr/statistiques/fichier/4986677/ENTFRA20-F1.pdf [V]
- Assemblée nationale, rapport n° 3056 (8/7/2026) : https://www.assemblee-nationale.fr/dyn/17/rapports/cepat/l17b3056-t1_rapport-enquete.pdf [D]
- Agersnap et Zidar (2021), NBER WP 27705 : https://www.nber.org/papers/w27705 [S, résumé]
- LégiFiscal, 16/10/2025 (taxe holdings, PLF 2026) : https://www.legifiscal.fr/actualites-fiscales/4275-plf-2026-instauration-taxe-patrimoine-financier-holdings-patrimoniales.html [S]
- DGFiP, totaux des cases 2042 (revenus 2024) et Statistiques n° 53 (revenus 2025) ; France Stratégie (2023) ; IPP note 46 :
  via `pfu/donnees/pfu_chiffres.csv` [D].
