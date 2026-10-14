# À quoi a servi la dette publique ? Attribution de la dette française

Projet lancé en octobre 2026. Point de départ de l'utilisateur : l'État porte environ 80 % de la
dette alors qu'il finance les collectivités et la sécurité sociale. Quelle part revient réellement
à chacun, et à quelles dépenses ? L'hypothèse de départ était d'environ 50 % pour le social.

## Livrable

- `note-dette.pdf` / `note-dette.tex` : « À quoi a servi la dette publique ? », 7 figures et un
  tableau. C'est la version raccourcie d'environ 40 % de la note d'octobre.
  - Plan : chiffre officiel ; pourquoi la dette a monté (dynamique standard, 1978-2025) ; méthode
    fongible par fonction ; ce qui a fait monter la dépense (dérive) ; règles non fongibles ;
    travaux existants ; limites ; annexe de méthode.
  - Compilation : depuis ce dossier, `pdflatex note-dette.tex` deux fois. La note utilise
    `../lvt/preambule.tex`.

## Programme unique : `dette.py`

Depuis `fiscalite/` :

- `python dette/dette.py --telecharger` : télécharge les données Eurostat et Insee dans `donnees/`,
  puis calcule.
- `python dette/dette.py` : calculs, résumé imprimé, `tableau_attribution.tex`, figures PNG avec
  titre dans `../figures/`.
- `FIG_NU=1 python dette/dette.py` : figures sans titre pour la note, dans `../figures/nu/`.

Le programme enchaîne cinq étapes, puis les figures :

1. données ;
2. dynamique de la dette (FMI et Commission) ;
3. méthode fongible par fonction ;
4. dérive (méthode d'Auerbach) ;
5. règles par administration (M0 à M4).

Les figures, préfixe `dette_` : `emetteur`, `financement`, `dynamique`, `fonctions`,
`fonctions_evolution`, `derive`, `prestations`.

Données (`donnees/`) :

- `comptes.csv` : Eurostat `gov_10a_main`, dont les transferts D7 et D9 par sous-secteur
  destinataire ;
- `cofog.csv` : `gov_10a_exp`, dépense par fonction, avec la vieillesse GF1002, 1995-2024 ;
- `impots.csv` : `gov_10a_taxag`, D2 et D211 (TVA) ;
- `pib.csv` ;
- `dette_insee.csv` : dette par sous-secteur, Insee base 2020 ;
- `insee_long.csv` : Insee base 2014, séries arrêtées, en Md€ ; dette depuis 1978, déficit,
  intérêts, prestations D62 + D632 et PIB depuis 1949.

Sorties : `dynamique_longue.csv`, `fonctions_2025.csv`, `attribution_2025.csv`.

## Résultats clés (fin 2025)

- **Émetteur** : État et ODAC 83,6 %, APUL 8,0 %, ASSO 8,5 % de 3 460 Md€.
- **Dynamique**, en points de PIB :
  - 1995-2025 : de 57,5 % à 115,7 % du PIB. Déficits primaires +50,5 (dont 22 pour 2009-2010 et
    2020-2021), intérêts +73,9, croissance −72,3, ajustements stock-flux +6,0.
  - 1978-1995 : de 21,2 % à 56,1 %. Déficits primaires +8,8, intérêts +41,9, croissance −33,4,
    ajustements stock-flux +17,6, inexpliqués et concentrés en 1979-1984.
  - Changement de base en 1995 : +1,4 point.
- **Méthode fongible** (prorata de la dépense par fonction, intérêts qui suivent la dette, stock
  de 1995 réparti selon la dépense de 1995) :
  - santé et protection sociale : 1 959 Md€, soit 57 %, dont vieillesse 22 %, autres prestations
    sociales 20 %, santé 14 % ;
  - autres fonctions : affaires économiques 12 %, enseignement 10 %, défense 4 %, police et
    justice 3 % ;
  - 59 % de la dette créée depuis 1995, et 29,7 points sur les 50,5 points de déficits primaires.
  - Par administration (M1) : ASSO 45 %, APUL 18 %, État 37 %.
- **Dérive**, 1995-2024, en points de PIB :
  - dépense hors intérêts +2,3 et recettes +0,3 ;
  - vieillesse +2,4 et santé +2,0 ; les autres fonctions −2,1.
  - Avec la méthode d'Auerbach et 1997 comme référence : vieillesse +42 et santé +32 points
    cumulés, autres fonctions −23. Quelle que soit la référence : vieillesse +42 à +55, santé
    +32.
- **Prestations sociales** (D62 + D632) : 11,3 % du PIB en 1960, 17,9 % en 1978, 25,8 % en 2025.
- **Règles non fongibles**, part de l'ASSO dans la dette créée depuis 1995 : M2 3 %, M3 (TVA
  traitée comme transfert) 42 %, M3+ 131 %. Ces règles sont fragiles : la bascule du CICE en
  2019 déplace environ 35 Md€ par an.
- **Littérature** : aucune attribution documentée du stock de dette par fonction.
  - Le rapport Pébereau (2005) la juge « impossible ».
  - Champsaur-Cotis (2010) : contrefactuel côté recettes, environ −20 points de dette.
  - Catherine : contrefactuel des retraites allemandes, dette de 58 % du PIB.
  - Riedl et Kogan : lectures opposées des mêmes données aux États-Unis.

## Notes de lecture (`notes/`)

- `lectures.md` : IPP 2026, Beaufret 2023, Fipeco, tweets de Sylvain Catherine (extraits), points
  vérifiés et non vérifiés.
- `revue_attribution_par_fonction.md` : Pébereau, Champsaur-Cotis, Fipeco, Auerbach, OBR, Riedl et
  Kogan, HCP, COR, Dufourcq, CAE Focus 121.
- `revue_litterature_agent.md` : attribution par sous-secteur ; chronologie des reprises de dette
  (CADES, SNCF Réseau, 1993) ; SEC 2010 §1.78.

## Points en suspens

- Expliquer les ajustements stock-flux de 1979-1984 : prêts ou dotations aux entreprises
  publiques, ou défauts de la rétropolation.
- Corriger le double compte des pensions des fonctionnaires de l'État (CAE Focus 121) dans la
  dépense par fonction.
- Une règle de ressources propres cohérente demanderait les exonérations compensées, que donnent
  les annexes aux PLFSS.
- Les textes originaux de Sylvain Catherine sur X n'ont pas été lus (HTTP 402).
