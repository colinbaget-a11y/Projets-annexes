# Charte éditoriale de la note « Taxer mieux plutôt que davantage » (refonte du 16/11/2026)

Lecteur visé : un décideur politique intelligent, intéressé par l'économie, qui ne connaît pas bien la fiscalité
française. On l'amène progressivement à comprendre le problème puis la solution ; on ne lui assène pas les
résultats des modèles. Le travail économique est fait : il s'agit de le présenter comme une démonstration
économique et politique, pas comme un compte rendu de simulations. Ne jamais modifier un résultat de simulation
pour servir le récit ; si un chiffre manque, le calculer (et le dire) ; si une proposition est fragile, le dire.

## Architecture commune des quatre parties (IR-CSG, immobilier, IS, PFU)

Chaque partie est un `\section` (déjà posé dans note-reforme-fiscale.tex) découpé en six `\subsection`. Les titres
racontent l'histoire : un lecteur qui ne lit que les titres et les figures comprend le raisonnement. Titres
affirmatifs, courts, pas « Situation actuelle » mais par exemple « Trois impôts empilés, qui ne se parlent pas ».

1. **La situation actuelle : comprendre avant de réformer.** Très pédagogique. Combien l'impôt rapporte, sur quelle
   assiette, à quels taux, qui le paie réellement, ses particularités françaises, la comparaison internationale
   quand elle est pertinente. Largement illustrée de graphiques simples. Aucune proposition ici.
2. **Quel est le problème économique ?** Ce que la théorie reproche à l'impôt, et dans quelle mesure les études le
   confirment. Pas de revue de littérature autonome : deux à quatre résultats empiriques convaincants, chacun au
   moment où il sert le raisonnement (ce que l'étude mesure, sur qui, l'ordre de grandeur). Expliquer aussi pourquoi
   les dispositifs existants ont été créés (justification d'origine), et ce qui pose problème aujourd'hui
   (accumulation, coût, justification disparue).
3. **Que donnerait une réforme naïve ?** La réforme qui viendrait spontanément à un économiste. IR-CSG : harmoniser
   brutalement assiettes et règles en gardant les barèmes. Immobilier : baisser les droits de mutation et relever
   uniformément la taxe foncière. IS : une baisse générale du taux. PFU : changer son taux ou revenir au barème.
   Montrer concrètement ce que cela donne (graphique, ordres de grandeur), puis pourquoi cela ne suffit pas.
4. **Construire une réforme plus intelligente.** Le cœur. Partir des limites de la réforme naïve ; mobiliser les
   enseignements de la littérature ; mécanismes ambitieux mais conventionnels, si possible inspirés d'expériences
   étrangères documentées (vérifiées). L'optimisation indique une direction, elle ne décide pas. Présenter le système
   auquel on aboutit, avec des graphiques comparant directement aujourd'hui et la proposition.
5. **Les vrais arbitrages politiques.** Trois à cinq paramètres sur lesquels un décideur peut hésiter. Pour chacun :
   ce qu'on gagne économiquement à aller plus loin ; ce que cela coûte et comment on le finance ; qui le supporte ;
   les pertes particulièrement fortes ; si une variante prudente garde l'essentiel du bénéfice. Cas types concrets
   auxquels on peut s'identifier (un retraité modeste, un couple avec trois enfants, un couple à un seul revenu, un
   jeune ménage qui achète…), pas seulement des moyennes par décile.
6. **Comment passer de l'ancien au nouveau système.** Rythme de montée en charge (trois, cinq, dix ans), hausse
   annuelle que doivent absorber les principaux perdants, trésorerie, endettement transitoire, collecte,
   constitutionnalité, faisabilité administrative. Distinguer très clairement le coût de transition du coût permanent.

Annexe de chaque partie (`parties/annexe_<partie>.tex`, compilée en fin de note) : calibrage, hypothèses
techniques, variantes secondaires, tableaux complets, figures chargées (toutes les variantes), précautions de
méthode. Rien ne se perd : ce qui sort du corps va en annexe. Le corps garde les incertitudes qui peuvent changer
la conclusion.

## Style

- Texte engageant, éditorialisé, presque politique dans la manière de poser les questions ; rigoureux dans les
  réponses. De vrais paragraphes qui développent un raisonnement. Listes à puces seulement pour une énumération
  réellement parallèle (options, cas types), jamais pour transformer un raisonnement en fragments.
- Français précis ; pas de tics de rédaction IA (« il est important de noter », « souligne », « met en lumière »,
  triades artificielles, conclusions récapitulatives, transitions scolaires). Concret avant abstrait.
- Expliquer le mécanisme (qui fait quoi, ce qui change pour lui, pourquoi il change sa décision), pas son nom.
- **Hypothèses et chiffres non vérifiés : toujours signalés.** Dans le texte, une hypothèse forte est dite comme
  telle (« nous supposons que… ; aucune donnée publiée ne permet de le vérifier »). Un chiffre non vérifié sur une
  source primaire est signalé (« chiffre non vérifié », ou renvoi à l'annexe). Chaque partie a, dans son annexe, un
  tableau « Hypothèses fortes et chiffres non vérifiés » (hypothèse ; où elle joue ; ce qu'elle change si elle est
  fausse). Les registres `revue/hypotheses_<partie>.md` en sont la source.
- Distinguer : mécanisme théorique / fait mesuré / effet causal établi / ordre de grandeur.

## Graphiques

- Davantage de graphiques simples, pas de graphiques compliqués. Un graphique démontre une idée précise. Privilégier :
  histogrammes, courbes de taux moyen et marginal, avant/après, décompositions de recettes, gagnants/perdants.
- Le titre (2e argument de `\figbloc`) énonce le résultat : « Un retraité modeste paierait 1 300 € de plus », pas
  « Variation de la charge ».
- Couleurs identiques dans toute la note (module `synthese/style_note.py`) : aujourd'hui = encre grise foncée
  `#3d3d3d` ; réforme naïve = brique `#993333` ; proposition = bleu `#1d4ba6` ; variante ou arbitrage = ocre
  `#c79100` ; gris clair `#b8b8b8` pour un élément secondaire. Composantes d'une décomposition : nuances d'une même
  teinte (module : `NUANCES_BLEU`). Ne pas superposer plus de trois séries ; les figures à toutes les variantes vont
  en annexe.
- Charte technique : scripts de figure qui importent `graphiques` (fonctions `fin`, mode `FIG_NU=1`) et
  `synthese/style_note.py`. En mode nu, `graphiques` réduit le format à 62 % et les polices à 78 % : dessiner à
  environ 9 pouces de large (→ 14 cm imprimés) et moins de 4,3 pouces de haut ; ce que `graphiques` ne met pas à
  l'échelle (`tick_params(labelsize=…)`, `fig.legend`, `set_yticklabels(fontsize=…)`) se multiplie par `ECH_TXT`.
  Sources et note de lecture passées à `fin()` (écrites dans `figures/nu/<nom>_note.tex`), jamais dans l'image.
  Générer les deux modes : `python3 <script>` puis `FIG_NU=1 python3 <script>`. Regarder chaque PNG avant de finir.
- Noms : `<partie>_n<NN>_<sujet>` (ex. `ircsg_n01_recettes`), pour ne pas écraser les figures existantes.

## Fichiers et compilation

- Corps : `synthese/parties/<partie>.tex` (ircsg, foncier, is, pfu) ; annexe : `synthese/parties/annexe_<partie>.tex`.
- Le document maître `synthese/note-reforme-fiscale.tex` est modifié par l'orchestrateur seulement.
- Pour tester, compiler une COPIE dans le scratchpad (pas dans synthese/, d'autres agents compilent en parallèle) :
  copier note-reforme-fiscale.tex et ne garder que sa partie, ou utiliser `\includeonly`-like en dupliquant.
- Références : citer « Auteur (année) » dans le texte ; signaler à l'orchestrateur toute entrée à ajouter à
  `parties/references.tex` (ne pas l'éditer).
