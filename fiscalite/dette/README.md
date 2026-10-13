# À qui revient la dette publique ? Attribution entre État, collectivités et sécurité sociale

Projet lancé en octobre 2026. La question de départ : l'État porte environ 80 % de la dette alors
qu'il finance les collectivités et la sécurité sociale ; quelle part de la dette revient
réellement à chacun ? L'hypothèse de départ de l'utilisateur était d'environ 50 % pour le social.

## Livrable

- `note-dette.pdf` / `note-dette.tex` : « À quoi a servi la dette publique ? », 12 pages avec 7
  figures et un tableau.
  - Plan : chiffre officiel ; méthode fongible ; résultat par fonction ; dérive de la dépense ;
    règles non fongibles ; travaux existants ; limites ; annexe.
  - Plan : l'essentiel ; ce que disent les comptes ; attribuer suppose un contrefactuel (les règles
    M1 à M4) ; résultats ; poids de la dette de 1995 ; travaux existants (IPP 2026, Beaufret) ;
    limites ; annexe de méthode.
  - Compilation : depuis ce dossier, `pdflatex note-dette.tex` deux fois. La note utilise
    `../lvt/preambule.tex`.
- `tableau_attribution.tex` : tableau 1, généré par `attribution.py`.

## Résultat principal : la méthode simple (dépenses fongibles, `fongible.py`)

- Principe : chaque année, la dette hors intérêts est répartie au prorata de la dépense par fonction
  (COFOG, hors intérêts). Chaque fonction porte les intérêts de sa dette. Le stock de 1995 est
  réparti selon la dépense de 1995.
- Dette attribuée fin 2025, sur 3 460 Md€ :

  | Fonction | Part de la dette | Montant |
  |---|---|---|
  | Santé et protection sociale | 57 % | 1 959 Md€ |
  | dont vieillesse | 22 % | 766 Md€ |
  | dont autre protection sociale | 20 % | 705 Md€ |
  | dont santé | 14 % | 488 Md€ |
  | Affaires économiques | 12 % | |
  | Enseignement | 10 % | |
  | Défense | 4 % | |
  | Police et justice | 3 % | |

  Sur la seule dette créée depuis 1995, la part sociale est de 59 %.
- Variation 1995-2024, en points de PIB :
  - dépense hors intérêts : +2,3 ;
  - recettes : +0,3 ;
  - vieillesse : +2,4 ; santé : +2,0 ; toutes les autres fonctions : −2,1 ;
  - intérêts : −1,4.
- Sylvain Catherine :
  - il ne fait pas de prorata ; il compare à l'Allemagne (dette de 58 % du PIB avec les retraites
    allemandes) ;
  - il affirme que les retraites sont « la cause de la moitié de l'endettement public » (X, avril
    2026, contesté par Sterdyniak) ;
  - ses tweets ne sont pas lisibles directement (HTTP 402) et ne sont connus que par des extraits.

## Comparaison des règles par administration (`attribution.py`, résultats fin 2025)

- Dette par émetteur (Insee) : État et ODAC 83,6 %, APUL 8,0 %, ASSO 8,5 %, sur 3 460 Md€.
- Décomposition de la dette au taux apparent des APU :
  - stock 1995 et ses intérêts : 1 928 Md€ (56 %) ;
  - déficits primaires 1996-2025 et leurs intérêts : 1 355 Md€ ;
  - ajustements stock-flux : 177 Md€.
- Part de la sécurité sociale, puis du social selon la règle (dette créée depuis 1995 / dette
  totale) :

  | Règle | Dette créée depuis 1995 | Dette totale |
  |---|---|---|
  | M0 émetteur | ≈ 0 % | 9 % |
  | M2 transferts explicites | 3 % | 10 % |
  | M3 TVA affectée traitée comme transfert | 42 % | 26 % |
  | M3+ tous impôts indirects affectés | 131 % | 61 % |
  | M1 prorata de la dépense primaire finale | 46 % | 27 % |
  | M4 prorata par fonction (santé + protection sociale) | 59 % | 32 % |

  La vieillesse au prorata de la dépense : 24 % des déficits primaires cumulés.
- Flux de l'État en 2025 :
  - transferts D7 et D9 vers les APUL 55 Md€, vers les ASSO 23 Md€ ;
  - TVA affectée en 2024 : ASSO 58 Md€, APUL 52 Md€ ;
  - autres impôts sur la production des ASSO : 63 Md€.
- ASSO, 1995-2025 : déficits cumulés 118 Md€, mais hausse de la dette de 259 Md€ (réserves des
  régimes complémentaires et du FRR : la dette brute surestime la dette nette).
- Conclusion de méthode :
  - La règle la plus défendable comme convention est le prorata de la dépense (M1, M4).
  - Les règles de « ressources propres » dépendent du statut des impôts affectés, fixé par le
    Parlement : le CICE en 2019 déplace environ 35 Md€ par an.
  - Une règle de ressources propres cohérente (TVA rendue à l'État, exonérations rendues à la
    sécurité sociale) donnerait un résultat proche de M2.

## Scripts et données (`donnees/`)

- `fongible.py` : méthode simple par fonction ; écrit `fonctions_2025.csv` et
  `fonctions_evolution.csv`.
- `extract_dette.py` télécharge les données Eurostat et Insee et écrit dans `donnees/` :
  - `comptes.csv` : `gov_10a_main`, dont les transferts par sous-secteur destinataire ;
  - `impots.csv` : `gov_10a_taxag` ;
  - `cofog.csv` : `gov_10a_exp`, avec GF1002 ;
  - `pib.csv` ;
  - `dette.csv` : Eurostat, seulement 2024-2025 par sous-secteur ;
  - `dette_insee.csv` : flux BDM `DETTE-TRIM-APU-2020`, 1995-2025.
- `attribution.py` calcule les règles M0 à M4 et écrit `attribution_annuelle.csv`,
  `attribution_deficits.csv`, `attribution_2025.csv` et `tableau_attribution.tex`.
- `graphiques_dette.py` produit les figures `dette_*`. Avec `FIG_NU=1`, il produit les versions de la
  note dans `../figures/nu/`.
- Ordre d'exécution : `python dette/extract_dette.py && python dette/fongible.py && python dette/attribution.py &&
  FIG_NU=1 python dette/graphiques_dette.py`, depuis `fiscalite/`.

## Notes de lecture

- `notes/lectures.md` : IPP 2026 (lu), Beaufret 2023 (lu), Beaufret 2026 (non lu), Fipeco, points
  vérifiés et non vérifiés.
- `notes/revue_attribution_par_fonction.md` : qui a déjà attribué la dette par fonction.
  - Pébereau 2005 juge cette attribution « impossible » : « un seul déficit ».
  - Champsaur-Cotis 2010 : contrefactuel côté recettes, environ −20 points de PIB de dette.
  - Fipeco 2023 : variations de dépense par fonction, 1995-2021.
  - Auerbach 1994, OBR 2024 : cadre des décompositions de variations.
  - États-Unis : lectures opposées de Riedl et de Kogan.
  - Beaufret, HCP, COR ; Dufourcq (méthode non publiée) ; CAE Focus 121 (cotisations fictives de
    l'État).
  - Conclusion : aucune attribution documentée du stock par fonction.
- `notes/revue_litterature_agent.md` : revue détaillée (Catherine, Dufourcq, Ecalle, reprises de dette
  1993-2026, SEC 2010 §1.78 et pratiques européennes, impôts affectés CPO 2024), avec statut de
  vérification de chaque fait.

## Points en suspens

- Réattribuer le stock de 1995 : il faudrait les comptes par sous-secteur antérieurs (Insee, séries
  longues).
- Construire la variante cohérente de M3 : il faut les exonérations compensées, que donnent les
  annexes aux PLFSS.
- Isoler les contributions d'équilibre aux régimes de fonctionnaires (CAS pensions, CNRACL).
- Sylvain Catherine : ses textes originaux (fils sur X) n'ont pas été lus ; seule une reprise de presse
  l'a été.
- Texte Insee justifiant l'enregistrement des fractions de TVA comme impôts de l'affectataire : non
  trouvé.
