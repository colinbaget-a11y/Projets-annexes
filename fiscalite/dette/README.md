# À qui revient la dette publique ? Attribution entre État, collectivités et sécurité sociale

Projet lancé en octobre 2026. La question de départ : l'État porte environ 80 % de la dette alors
qu'il finance les collectivités et la sécurité sociale ; quelle part de la dette revient
réellement à chacun ? L'hypothèse de départ de l'utilisateur était d'environ 50 % pour le social.

## Livrable

- `note-dette.pdf` / `note-dette.tex` : note de 9 pages avec 5 figures et un tableau.
  - Plan : l'essentiel ; ce que disent les comptes ; attribuer suppose un contrefactuel (les règles
    M1 à M4) ; résultats ; poids de la dette de 1995 ; travaux existants (IPP 2026, Beaufret) ;
    limites ; annexe de méthode.
  - Compilation : depuis ce dossier, `pdflatex note-dette.tex` deux fois. La note utilise
    `../lvt/preambule.tex`.
- `tableau_attribution.tex` : tableau 1, généré par `attribution.py`.

## Résultats clés (fin 2025)

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
- Ordre d'exécution : `python dette/extract_dette.py && python dette/attribution.py &&
  FIG_NU=1 python dette/graphiques_dette.py`, depuis `fiscalite/`.

## Notes de lecture

- `notes/lectures.md` : IPP 2026 (lu), Beaufret 2023 (lu), Beaufret 2026 (non lu), Fipeco, points
  vérifiés et non vérifiés.

## Points en suspens

- Réattribuer le stock de 1995 : il faudrait les comptes par sous-secteur antérieurs (Insee, séries
  longues).
- Construire la variante cohérente de M3 : il faut les exonérations compensées, que donnent les
  annexes aux PLFSS.
- Isoler les contributions d'équilibre aux régimes de fonctionnaires (CAS pensions, CNRACL).
- Sylvain Catherine, cité par l'utilisateur : la recherche bibliographique était encore en cours
  quand la note a été écrite.
