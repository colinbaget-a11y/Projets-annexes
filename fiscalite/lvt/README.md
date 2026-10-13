# Taxe sur la valeur foncière (LVT) : note et matériaux

Travail réalisé en octobre 2026 pour le rapport « Un système fiscal pour la France au XXIe siècle »
(think tank Robert de Sorbon), à la demande des commanditaires qui pensaient à une forme de LVT
pour réformer la taxe foncière.

## Livrable

- `lvt-brief.pdf` / `lvt-brief.tex` : note unique « Taxer le terrain » (20 pages, 12 figures).
  Plan : l'essentiel ; définition et pays ; théorie (et encadré des économistes) ; la France
  (valeur du sol, ce que mesure ce chiffre, géographie, taxe foncière de 1970, ordres de grandeur) ;
  études transposées à la France par règles de trois ; difficultés pratiques (évaluation, revenus,
  communes, zonage) ; mise en place progressive ; options ; annexe de méthode ; références.
- `preambule.tex` : mise en page commune (même charte que `cours/refaire-l-impot.tex`).
- Compilation : `pdflatex lvt-brief.tex` deux fois, depuis ce dossier.

## Chiffres clés (à réutiliser)

- Terrains sous les bâtiments : 6 729 Md€ fin 2024 (229 % du PIB, 53 % en 1998) ; ménages 4 043 Md€.
  C'est un résidu (valeur de marché − bâti à l'inventaire permanent), sans marge d'incertitude
  publiée ; niveau 2023 révisé de 9 % entre deux publications Insee.
- Prix des logements anciens ×3,0 de 1998 à 2025, coût de construction ×2,0, loyers ×1,5.
- Taxe foncière bâtie : 42 Md€ (2024) ; elle pèse 0,54 % de la valeur des logements dans les 5 %
  de communes les moins chères contre 0,20 % dans les plus chères (Insee IA 91 × DVF 2024).
- Taux neutre d'une LVT : 0,72 % de la valeur des terrains (remplace la TFPB), environ 1 % avec
  les DMTO ; 0,57 % sur le seul périmètre des ménages (2017).
- Biens types (bascule à recette constante, taux 0,57 %) : maison Corrèze 1 040 € → 70 € ;
  Haute-Savoie 930 € → 1 700 € ; appartement parisien (hypothèse 75 % de terrain) 730 € → 2 130 €.
- Mise en place progressive (capitalisation, r = 3 %) : part de la perte supportée à l'annonce
  88 % (10 ans), 82 % (15 ans), 77 % (20 ans), 67 % (30 ans).
- Karlsruhe 2025 (Bade-Wurtemberg, terrain seul, recette constante) : maisons individuelles +76 %,
  commerces −40 %, copropriétés −20 %, terrains nus +265 %, 24 % de réclamations.

## Scripts et données

- `extract_lvt.py BRUT` : comptes de patrimoine Insee, PIB, DVF 2024, données de l'Insee Analyses
  n° 91 → `donnees/patrimoine.csv`, `dep2024.csv`, `tf_vs_prix.csv`, `tf_vs_prix_bins.csv`.
- `extract_complements.py BRUT` : indices de prix, de coût et de loyers, logements commencés,
  parc, gradient francilien, ventes DVF → `donnees/indices.csv`, `gradient_idf.csv`, `volumes.csv`.
- `graphiques_lvt.py` : les 12 figures (`FIG_NU=1` pour les versions sans titre utilisées dans la
  note), écrites dans `../figures/` et `../figures/nu/` sous le préfixe `lvt_`.
- Les fichiers bruts (DVF 2024 : 90 Mo) ne sont pas versionnés ; leurs URL sont en tête des scripts.

## Notes de lecture (`notes/`)

Notes de vérification bibliographique, avec statut de lecture de chaque source (texte intégral,
résumé, secondaire, NON VÉRIFIÉ). Les PDF téléchargés n'ont pas été conservés.

- `theorie_et_split_rate.md` : George, Arnott-Stiglitz, Feldstein, neutralité, Pittsburgh,
  Pennsylvanie, Mirrlees, OCDE 2022, pays.
- `etudes_recentes.md` : Danemark (Høj ; Nielsson et al.), Löffler-Siegloch, Koster-Pinchbeck,
  droits de mutation, Allemagne (Grundsteuer, BFH), Kumhof.
- `france_institutions_chiffres.md` : TFPB, DMTO, valeurs locatives, révisions, CPO, IPP, CAE,
  comptes de patrimoine, détention du patrimoine.
- `etudes_francaises.md` : Segú, Bérard-Trannoy, suppression de la TH (IPP 2023), Fack-Grenet,
  Combes-Duranton-Gobillon, LTV des primo-accédants.
- `valeur_des_terrains_statistique.md` : méthode Insee, guide Eurostat-OCDE, résidu vs terrain nu,
  Bodenrichtwerte, comparaisons internationales.
- `transitions_et_saillance.md` : Bradley, Elinder-Persson, Proposition 13, reports de paiement,
  Danemark 2024, ACT, Pittsburgh, Nouvelle-Zélande.
- `sources_video_et_rapports_officiels.md` : sources de la vidéo Money & Macro, pays de Galles 2020
  et 2026, Irlande, Écosse, Karlsruhe, Danemark (audits), Detroit, Cincinnati.
- `citations_economistes.md` : citations vérifiées (Smith, Ricardo, Mill, Walras, George,
  Vickrey, Mirrlees, panel de Chicago 2023, critiques) et non vérifiées (Friedman, Samuelson…).

## Points en suspens

- La citation de Friedman (1978) n'est vérifiée que par des sources secondaires (Nielsson et al.).
- Si l'on veut revenir à −10 % de longueur : retirer la critique autrichienne de l'encadré, la
  comparaison internationale du stock de terrains (3.2), Segú (2.2) et Berlin (5.1).
