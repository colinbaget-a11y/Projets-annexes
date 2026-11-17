# Fiche 4 « Super taxe foncière » : ce qu'on peut chiffrer simplement (17/11/2026)

Script : `note8p/calculs/super_tf_rapide.py` (lancer depuis `fiscalite/`, n'écrit rien). Statuts : [E] publié et lu,
[S] calcul, [H] hypothèse. Aucun fichier existant modifié.

## Chiffres obtenus

| Item | Résultat | Statut |
|---|---|---|
| Base : immobilier bâti privé (sol bâti + logements + bâtiments non résidentiels ; S11, S12, S14, S15), fin 2025 | 12 651 Md€ | [E] Insee 8.200 |
| Taux neutre qui remplace la TFPB (43,1 Md€, REI 2025) | **0,34 %** | [S] |
| Taux neutre qui remplace TFPB + DMTO (16,1 Md€, taux permanent, ventes 2025) | **0,47 %** (0,41 % avec DMTO/2) | [S] |
| Coût d'un point de base (0,01 %) | 1,27 Md€ | [S] |
| Ménages seuls : TFPB « ménages » (26,3, clé DGCL 61 %) / 8 993 Md€ | 0,29 % | [S] |
| Modèle communal (logements des particuliers, métropole hors Alsace-Moselle, 6 762 Md€) | 0,36 % ; 0,54 % avec DMTO | [S] |
| Encours des crédits à l'habitat des ménages, déc. 2025 | 1 288 Md€ | [E] BCE |
| Taux moyen de l'encours, déc. 2025 | 1,94 % (2,04 % sept. 2026) | [E] BCE |
| Intérêts payés (encours × taux) | ≈ 25 Md€/an | [S] |
| Dette déduite de l'assiette : manque à gagner au taux de 0,34 % / 0,47 % | 4,4 / 6,0 Md€ | [S] |
| Taux neutre sur base nette de dette | 0,38 % / 0,52 % (+11 %) | [S] |
| Crédit d'impôt égal aux intérêts | 25 Md€, autant que toute la TFPB des ménages : impraticable sans plafond | [S] |

Répartition territoriale (modèle communal, taxe unique sur la valeur totale, recette constante) :
- remplace la TF : dixièmes de prix au m² 1 à 7 de −80 à −185 €/an (−9 à −33 %), 10e +825 € (+99 %) ; 40 % des
  logements en hausse, 15 % à plus de +300 € ; Paris +183 %, Hauts-de-Seine +114 %, Haute-Savoie +78 % ; Nièvre,
  Aisne, Allier −47 %.
- remplace TF + DMTO des logements : 80 % en hausse, 44 % à plus de +300 € ; Paris +327 %. Net de l'économie moyenne
  de droits : −160 € (1er dixième) à +730 € (10e).

Volatilité : de 2022 à 2025 la valeur des logements et du sol bâti des ménages a baissé d'environ 4 % (−3,9 % en 2023),
les DMTO sur les logements de 33 % (16,8 → 11,2 Md€). Écart-type annuel de la croissance de l'assiette 1979-2025 :
6,0 points (5,2 lissée sur 3 ans).

## Sources

- Insee, comptes de patrimoine 2025, tableau 8.200 : https://www.insee.fr/fr/statistiques/8988859 (dans `foncier/donnees/`).
- BCE Data Portal, encours : https://data.ecb.europa.eu/data/datasets/BSI/BSI.M.FR.N.A.A22.A.1.U2.2250.Z01.E ;
  taux de l'encours : https://data.ecb.europa.eu/data/datasets/MIR/MIR.M.FR.B.A22.A.R.A.2250.EUR.O (séries nationales
  transmises par la Banque de France ; Webstat inaccessible ce jour). Le périmètre « ménages » comprend les
  entrepreneurs individuels et inclut les prêts pour résidences secondaires et investissement locatif.
- TFPB, DMTO (OFGL, Compte du logement, comptabilité nationale) : `foncier/notes/inventaire.md` (textes lus).
- Insee Analyses n° 91 (valeur de marché par XGBoost sur Fidéli-Majic-DVF) : https://www.insee.fr/fr/statistiques/fichier/7735076/IA91.pdf
- CPO 2023 (recommandations 3 et 8 ; DGFiP réticente : rotation tous les 19 ans, volatilité) :
  https://www.vie-publique.fr/files/rapport/pdf/292676.pdf
- CAE Note n° 2 (2013), Trannoy-Wasmer, proposition 9 (valeur vénale nette, 0,5 %) : https://cae-eco.fr/static/pdf/cae-note002.pdf

## Limites

Bâti des sociétés au coût de remplacement (pas une valeur de marché) ; sol = résidu ; TFPB 2025 contre valeurs de fin 2025 ;
la déduction de dette ne vaut que pour les ménages (dette des sociétés non comptée) ; modèle : même taux TF/valeur pour
tous les logements d'une commune (dispersion intracommunale ignorée) ; recettes de 2025 non indexées.
