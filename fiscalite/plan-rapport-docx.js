// Proposition de plan au format Word.
// Régénération : npm install docx, puis node plan-rapport-docx.js (écrit plan-rapport.docx).
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Header, Footer, AlignmentType,
  HeadingLevel, LevelFormat, BorderStyle, PageNumber, ShadingType, LineRuleType,
} = require("docx");

const POLICE = "Cambria";
const BLEU = "003399";        // titres
const OCRE = "C79100";        // repères (numéros, étiquettes de partie)
const ENCRE = "1A1A19";       // texte courant
const GRIS = "5F6368";        // textes de cadrage
const BLEU_PALE = "C9D3EA";   // filets
const FOND = "EEF2FA";        // encadré de la thèse
const FR = { value: "fr-FR" };

// Typographie française : espaces insécables avant la ponctuation haute, dans les guillemets,
// entre un nombre et son unité.
const NBSP = String.fromCharCode(0xA0);    // espace insécable
const NNBSP = String.fromCharCode(0x202F);  // espace fine insécable
const fr = (s) => s
  .replace(/'/g, String.fromCharCode(0x2019))
  .replace(/ :/g, NBSP + ":")
  .replace(/ ([;?!])/g, NNBSP + "$1")
  .replace(/\u00AB /g, "\u00AB" + NBSP).replace(/ \u00BB/g, NBSP + "\u00BB")
  .replace(/(\d) %/g, "$1" + NBSP + "%")
  .replace(/(\d) (\d{3})(?!\d)/g, "$1" + NNBSP + "$2")
  .replace(/ \u20AC/g, NBSP + "\u20AC")
  .replace(/(\d) (milliards|points|ans)/g, "$1" + NBSP + "$2");

const run = (texte, opts = {}) => new TextRun({ text: fr(texte), language: FR, ...opts });

// Titre de partie : étiquette en ocre, puis le titre en bleu à la ligne.
const partie = (etiquette, titre) => new Paragraph({
  heading: HeadingLevel.HEADING_1,
  children: [
    run(etiquette.toUpperCase(), { color: OCRE, size: 17, characterSpacing: 30 }),
    run(titre, { break: 1 }),
  ],
});

// Titre de chapitre : numéro en ocre, titre en bleu.
const chapitre = (num, titre) => new Paragraph({
  heading: HeadingLevel.HEADING_2,
  children: [run(num + ".", { color: OCRE }), run("  " + titre)],
});

// Ce que le chapitre établit.
const cadre = (texte) => new Paragraph({
  keepNext: true,
  spacing: { after: 100 },
  children: [run(texte, { italics: true, color: GRIS })],
});

// Un argument : l'affirmation en gras, puis son développement.
const arg = (affirmation, suite) => new Paragraph({
  numbering: { reference: "puces", level: 0 },
  children: [run(affirmation, { bold: true }), run(" " + suite)],
});

// Transition entre deux parties.
const transition = (texte) => new Paragraph({
  spacing: { before: 200, after: 80 },
  indent: { left: 120 },
  border: { left: { style: BorderStyle.SINGLE, size: 18, color: OCRE, space: 10 } },
  children: [run("Transition : ", { bold: true, color: OCRE }), run(texte, { italics: true, color: BLEU })],
});

const siecle = (opts = {}) => [run("XXI", opts), run("e", { ...opts, superScript: true }), run(" siècle", opts)];

const contenu = [
  new Paragraph({
    spacing: { after: 60 },
    children: [run("PROPOSITION DE PLAN", { bold: true, size: 17, color: OCRE, characterSpacing: 40 })],
  }),
  new Paragraph({
    spacing: { after: 240, line: 252, lineRule: LineRuleType.AUTO },
    border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: OCRE, space: 8 } },
    children: [run("Un système fiscal pour la France", { bold: true, size: 40, color: BLEU }),
               run("au ", { bold: true, size: 40, color: BLEU, break: 1 }),
               ...siecle({ bold: true, size: 40, color: BLEU })],
  }),
  new Paragraph({
    spacing: { before: 120, after: 200, line: 288, lineRule: LineRuleType.AUTO },
    indent: { left: 120, right: 120 },
    shading: { type: ShadingType.CLEAR, color: "auto", fill: FOND },
    border: { left: { style: BorderStyle.SINGLE, size: 24, color: BLEU, space: 10 } },
    children: [
      run("La thèse. ", { bold: true, color: BLEU }),
      run("À niveau de recettes et de redistribution donnés, toutes les architectures fiscales ne se "
        + "valent pas. Il est possible de concevoir un système plus simple, plus neutre et moins "
        + "destructeur d'activité sans renoncer à ses objectifs de justice ou de financement."),
    ],
  }),

  // ---------------------------------------------------------------- Première partie
  partie("Première partie", "Qu'est-ce qu'un bon impôt ?"),

  chapitre("1", "Le pacte fiscal : les principes qui fondent l'impôt"),
  arg("Un socle commun : la Déclaration de 1789.", "La contribution commune est « indispensable », "
    + "répartie entre les citoyens « en raison de leurs facultés » ; les citoyens doivent pouvoir en "
    + "« constater la nécessité », la « consentir librement » et en « suivre l'emploi ». Ces principes "
    + "peuvent servir de point de départ théoriquement accepté par tous avant tout débat sur le niveau "
    + "ou la structure de l'impôt."),
  arg("Nécessité : lever ce dont la collectivité a besoin, sans coût inutile.", "En langage "
    + "économique, l'impôt doit financer les dépenses jugées nécessaires, mais une recette donnée doit "
    + "être levée en détruisant le moins possible d'activité et de valeur."),
  arg("Facultés : répartir l'effort selon la capacité contributive.", "Le système fiscal doit tenir "
    + "compte des différences de revenus et de ressources, sans jamais revêtir de caractère confiscatoire "
    + "selon la jurisprudence du Conseil constitutionnel. Le degré exact de redistribution relève du "
    + "choix collectif ; l'économie peut ensuite chercher la manière la moins coûteuse de l'obtenir."),
  arg("Consentement : un prélèvement lisible, prévisible et proportionné.", "Le contribuable doit "
    + "pouvoir comprendre ce qu'il paie et selon quelles règles. Cela conduit à rechercher des barèmes "
    + "lisibles, à limiter les taux marginaux excessifs et à éviter qu'un prélèvement devienne "
    + "disproportionné par rapport à son assiette."),
  arg("Contrôle de l'emploi : savoir ce que l'impôt finance.", "Le consentement suppose aussi de pouvoir "
    + "relier prélèvements et dépenses publiques. Transparence des recettes, affectations "
    + "compréhensibles et responsabilité dans l'usage de l'argent public participent donc à la qualité "
    + "du système fiscal, ce qui suppose que l'État, la Sécurité sociale et les collectivités disposent "
    + "chacun de ressources propres et identifiables."),

  chapitre("2", "Financer, orienter, corriger : le triangle de l'impôt"),
  cadre("Présenter les trois grandes fonctions du système fiscal à partir d'exemples concrets, puis "
    + "montrer pourquoi chaque impôt peut difficilement valider les trois côtés du triangle, d'où la "
    + "nécessité d'évaluer le système dans son entièreté."),
  arg("Financer l'action publique :", "lever les recettes nécessaires aux dépenses collectives, en "
    + "limitant autant que possible le coût économique du prélèvement."),
  arg("Orienter les comportements :", "encourager ou décourager certains comportements, notamment "
    + "lorsqu'ils produisent des externalités — pollution, tabac. On prépare le terrain pour la taxe "
    + "carbone."),
  arg("Corriger les inégalités :", "répartir l'effort selon les facultés contributives et assurer le "
    + "degré de redistribution souhaité collectivement, ce qui pose la question du meilleur instrument : "
    + "la progressivité et les dispositifs fiscaux, ou les dépenses publiques et les transferts sociaux ? "
    + "Ici, encadré possible pour expliciter ce point souvent oublié."),
  arg("Ces objectifs entrent en tension (Tinbergen) :", "plusieurs objectifs nécessitent généralement "
    + "plusieurs instruments."),
  arg("On ne doit donc pas demander à chaque impôt d'être à la fois efficace, redistributif et "
    + "incitatif.", "C'est l'ensemble du système fiscal et social qui doit tenir les trois sommets du "
    + "triangle (Musgrave ; Mirrlees Review)."),

  chapitre("3", "Prélever mieux : ce que nous apprend l'économie de l'impôt"),
  cadre("Présenter de manière pédagogique, à partir d'exemples concrets, quatre grands enseignements de "
    + "la littérature sur la taxation optimale."),
  arg("Tout impôt a un coût économique.", "Expliquer la perte sèche à partir d'un échange rendu "
    + "impossible par l'impôt (exemple : un propriétaire d'appartement prêt à vendre à 200 000 €, un "
    + "acheteur prêt à payer 210 000 ; l'État arrive et impose 8 % de droits de mutation entre les deux : "
    + "la vente n'a pas lieu, personne ne paie l'impôt et le gain de l'échange est perdu pour tous). Puis "
    + "introduire les taux marginaux, les réactions comportementales, les élasticités et l'intuition de "
    + "la courbe de Laffer : taxer davantage une activité peut réduire l'assiette au point de faire "
    + "baisser la recette."),
  arg("Tous les impôts ne sont pas également efficaces.", "Pourquoi privilégier des assiettes larges et "
    + "des taux bas ? Intuition du coût quadratique (sans le mentionner, bien sûr). Pourquoi rechercher la neutralité "
    + "fiscale, éviter de taxer les intrants et privilégier les assiettes peu élastiques ? Introduire la "
    + "fiscalité pigouvienne, et le classement des impôts selon leurs effets sur la croissance établi "
    + "par l'OCDE."),
  arg("Celui qui paie l'impôt n'est pas toujours celui qu'on croit.", "Introduire l'incidence fiscale : "
    + "une taxe sur les entreprises peut être supportée par les salariés, les consommateurs ou les "
    + "actionnaires, la charge retombant sur celui qui peut le moins s'y soustraire. Ici, on explique "
    + "pourquoi monter des impôts en apparence « sur les riches » ou « sur les entreprises » touche en "
    + "réalité Monsieur et Madame Tout-le-Monde."),
  arg("La justice fiscale se juge à l'échelle du système.", "Un impôt isolément régressif peut "
    + "s'inscrire dans un système globalement redistributif. Expliquer pourquoi une TVA uniforme "
    + "accompagnée de transferts ciblés peut être plus efficace et tout aussi redistributive qu'une TVA "
    + "à taux réduits."),
  transition("si ces principes sont relativement simples, comment la France s'en est-elle à ce point "
    + "éloignée ?"),

  // ---------------------------------------------------------------- Deuxième partie
  partie("Deuxième partie", "La France a progressivement perdu le fil de sa fiscalité"),

  chapitre("4", "Un système sans grand dessein, construit par accumulation"),
  arg("À chaque besoin nouveau, la solution la plus simple est d'ajouter un prélèvement.", "L'État "
    + "social grandit, de nouvelles dépenses apparaissent — chômage de masse et vieillissement depuis les "
    + "années 1970 — et les prélèvements suivent sans jamais rattraper la dépense : de 30 % du PIB en 1960 "
    + "à 45 % en 2022 (Insee). Le système fiscal s'adapte par couches plutôt que par refonte : "
    + "cotisations pour financer la protection sociale, puis CSG pour élargir son financement — créée en "
    + "1991 à 1,1 %, elle est devenue un second impôt sur le revenu —, puis CRDS pour financer la dette "
    + "sociale, créée en 1996 pour treize ans et toujours là."),
  arg("On taxe d'abord les assiettes les plus faciles à saisir.", "Les choix fiscaux sont aussi dictés "
    + "par les possibilités administratives : portes et fenêtres autrefois, salaires prélevés à la "
    + "source ou consommation aujourd'hui. La facilité de collecte peut donc peser autant que "
    + "l'efficacité économique dans la naissance d'un impôt."),
  arg("Les défauts d'un impôt appellent ensuite des correctifs plutôt que sa suppression.", "Le coût "
    + "élevé du travail conduit aux allègements de cotisations puis au CICE ; les taux élevés ou mal "
    + "ciblés conduisent aux niches, exonérations et taux réduits — près de 470 niches aujourd'hui. À "
    + "force de corriger les conséquences "
    + "des prélèvements existants, on complexifie encore leur architecture."),
  arg("L'économie politique favorise cette accumulation.", "Il est souvent plus facile de créer une "
    + "taxe sur une base peu visible ou sur un payeur politiquement commode que de remettre à plat "
    + "l'ensemble. Les cotisations dites « patronales » illustrent l'écart possible entre celui que la "
    + "loi désigne comme payeur et celui qui supporte économiquement le prélèvement."),

  chapitre("5", "Beaucoup prélever, mais surtout mal prélever"),
  cadre("Montrer, à partir de quelques prélèvements emblématiques, où la fiscalité française s'écarte "
    + "le plus clairement des principes de la première partie."),
  arg("Beaucoup prélever, parce qu'on dépense beaucoup.", "La France est au premier rang de la zone "
    + "euro pour la dépense publique en 2023, avec un écart qui s'est creusé depuis 2001 ; cet écart "
    + "finance pour deux tiers la protection sociale, d'abord les retraites et la santé (Cochard et "
    + "Deredec, Bulletin de la Banque de France n° 259/4)."),
  arg("Cotisations et allègements : des taux marginaux très élevés sur les bas salaires.", "La sortie "
    + "progressive des allègements de cotisations fait fortement augmenter le prélèvement sur l'euro "
    + "supplémentaire gagné : autour de certains niveaux de salaire, progresser salarialement est "
    + "davantage taxé qu'au salaire moyen. Trente ans d'exonérations ciblées ont épuisé le levier et tassé "
    + "l'échelle des salaires (Bozio et Wasmer, 2024) ; sur 100 euros gagnés en travaillant, un salarié "
    + "en garde 54, contre 60 dans les années 1990 (Foucher)."),
  arg("C3S : taxer le chiffre d'affaires plutôt que le bénéfice.", "La contribution sociale de "
    + "solidarité des sociétés est due sur les ventes indépendamment de la rentabilité et peut se "
    + "cumuler le long des chaînes de production : l'exemple le plus clair d'un impôt qui frappe avant "
    + "même que le profit existe."),
  arg("Droits de mutation : taxer le fait de déménager plutôt que le foncier.", "Les droits de "
    + "mutation à titre onéreux renchérissent directement les transactions immobilières et donc la "
    + "mobilité, alors que le sol constitue une assiette immobile beaucoup moins sensible aux "
    + "comportements."),
  arg("Fiscalité de l'épargne : taxer différemment un même rendement selon son enveloppe.", "PEA, "
    + "assurance-vie, compte-titres, livrets ou immobilier supportent des fiscalités très différentes : "
    + "le choix du placement dépend alors en partie de son statut fiscal plutôt que de son rendement "
    + "économique."),

  chapitre("6", "Quand la complexité finit par miner l'efficacité et la justice"),
  cadre("Montrer qu'à force de corriger des taux élevés par des exceptions, le système devient plus "
    + "coûteux économiquement, moins neutre et moins lisible."),
  arg("Des taux élevés, puis des exceptions pour en atténuer les effets.", "IR et niches fiscales ; "
    + "cotisations élevées et allègements de charges ; TVA et taux réduits. Une autre logique serait "
    + "celle d'assiettes beaucoup plus larges avec des taux plus faibles."),
  arg("Chaque exception détruit un peu la neutralité de l'impôt.", "Deux revenus, deux entreprises ou "
    + "deux consommations comparables ne sont plus taxés de la même manière. Les décisions sont alors "
    + "orientées par la fiscalité : choix d'un statut, d'un placement, d'un niveau de salaire ou d'un "
    + "secteur favorisé plutôt que par leur intérêt économique propre."),
  arg("L'exonération des uns est payée par les autres.", "À recettes données, toute niche ou allègement "
    + "oblige à taxer davantage le reste de l'assiette. Le débat fiscal devient alors une lutte "
    + "permanente pour obtenir ou conserver son régime particulier plutôt qu'une discussion sur le bon "
    + "niveau du taux commun."),
  arg("Le système devient illisible politiquement.", "Les allègements de cotisations sont qualifiés "
    + "d'« aides aux entreprises », les niches tantôt de privilèges, tantôt de politiques publiques : à "
    + "force de taxer puis de rendre, il devient difficile de savoir qui paie réellement quoi. Taxes "
    + "affectées et fractions de TVA réparties entre l'État, la Sécurité sociale et les collectivités "
    + "achèvent de brouiller le lien entre l'impôt et ce qu'il finance."),
  arg("Au total, un triangle brisé.", "Le rendement s'obtient par des taux élevés sur des assiettes "
    + "mitées ; les incitations se contredisent ; la redistribution passe par une complexité que nul ne "
    + "maîtrise. Le système pèse trop sur le travail et la production, trop peu sur la consommation, et "
    + "perd le consentement de ceux qui le paient."),

  // ---------------------------------------------------------------- Troisième partie
  partie("Troisième partie", "Quel système fiscal pour la France ?"),
  cadre("Le mouvement est le suivant : voilà le système qu'on peut construire, voilà les choix qui "
    + "restent ouverts à l'intérieur de ce système, voilà pourquoi il est difficile d'y arriver. Une "
    + "règle la traverse — assiettes larges, taux bas, le moins de niches possible, et pas d'aide là où "
    + "baisser un impôt suffit — et chaque proposition suit le même mode d'emploi : le principe, ce qu'on "
    + "en attend, ce que font nos voisins, qui gagne et qui perd, comment y aller, et la réponse aux "
    + "objections."),

  chapitre("7", "À quoi ressemblerait concrètement un système fiscal plus simple et plus efficace ?"),
  cadre("Passer des principes aux instruments et montrer qu'une autre architecture est possible."),
  arg("Travail et consommation : des cotisations plus faibles, une TVA plus large.", "Réduire fortement "
    + "les taux réduits de TVA ; lorsque leur suppression pénalise les ménages modestes, restituer "
    + "directement le gain du côté des prestations sociales plutôt que par un taux réduit bénéficiant à "
    + "tous. Utiliser ensuite une hausse de la TVA — la TVA dite « sociale » — pour financer une baisse "
    + "des cotisations et réduire la taxation du travail."),
  arg("Revenus : des assiettes larges et des taux plus faibles.", "À revenu égal, effort égal : qu'il vienne du "
    + "travail, d'une pension ou d'un patrimoine, un même revenu doit contribuer de la même façon, d'où "
    + "une CSG beaucoup plus uniforme entre revenus et statuts ; un IR débarrassé de l'essentiel de ses niches et abattements, permettant en "
    + "contrepartie d'abaisser les taux."),
  arg("Entreprises : cesser de taxer avant le bénéfice.", "Supprimer la C3S ; refondre la CVAE pour "
    + "qu'elle ne dépende plus du chiffre d'affaires, voire la rapprocher de l'IS ; réduire parallèlement "
    + "les aides qui compensent ces prélèvements — le troc « zéro aide contre zéro impôt de production », "
    + "crédits d'impôt et subventions sectorielles finançant la suppression. Resserrer l'assiette de l'IS "
    + "pour que les grands groupes paient le taux affiché."),
  arg("Capital : rechercher la neutralité.", "Rapprocher le traitement fiscal de placements comparables "
    + "et limiter les avantages liés au choix d'une enveloppe plutôt qu'à la nature économique du "
    + "revenu."),
  arg("Externalités : assumer les taxes qui corrigent réellement un coût collectif.", "À commencer par "
    + "la fiscalité carbone."),
  arg("Boucler les comptes.", "Présenter pour chaque réforme ce qui est supprimé, ce qui est abaissé ou "
    + "augmenté, son rendement et ses effets distributifs ; et pour l'ensemble, ce que paient le travail, "
    + "la consommation, les entreprises et les transmissions avant et après, avec les gagnants et les "
    + "perdants par niveau de vie et par âge."),

  chapitre("8", "Les grands arbitrages : jusqu'où déplacer la charge ?"),
  cadre("Les principes économiques donnent une direction, mais ne tranchent pas tous les choix "
    + "collectifs."),
  arg("Jusqu'où déplacer la taxation du travail vers la consommation ?", "Discuter l'ampleur souhaitable "
    + "de la TVA dite sociale et de la baisse correspondante des cotisations. Ce qu'on en attend : un "
    + "travail moins taxé, des exportations favorisées, des importations et des retraités mis à "
    + "contribution. Les précédents : le Danemark à la fin des années 1980, l'Allemagne en 2007, la "
    + "tentative française de 2012, abrogée. Les objections : l'inflation, un choc ponctuel plutôt "
    + "qu'une spirale ; les retraités modestes, protégés par les minima ; la fraude, réduite par la "
    + "facturation électronique."),
  arg("Quelle place donner aux transmissions ?", "Mettre face à face les arguments en faveur d'une "
    + "taxation accrue des héritages et ceux qui plaident pour la modération. D'un côté, la naissance "
    + "pèse de nouveau plus que le travail dans la constitution des patrimoines (CAE, « Repenser "
    + "l'héritage », 2021) ; de l'autre, l'impôt le plus rejeté, sur une épargne déjà imposée, dont le "
    + "rendement dépend de la capacité à retenir des assiettes mobiles."),
  arg("Comment taxer le capital sans décourager l'épargne et le risque ?", "Distinguer rendement "
    + "normal, rente, plus-value et prise de risque ; arbitrer le degré de neutralité souhaitable entre "
    + "supports, avec un objectif : orienter l'épargne longue vers les fonds propres des entreprises "
    + "plutôt que soutenir l'investissement par le guichet (rapport Draghi)."),

  chapitre("9", "Passer du système actuel au système cible"),
  arg("Réformer par paquets cohérents.", "Une suppression de niche doit être accompagnée de la baisse de "
    + "taux qu'elle finance ; une hausse de TVA, de la baisse de cotisations correspondante."),
  arg("Préserver le rendement et limiter les ruptures distributives.", "Compenser directement les "
    + "ménages réellement perdants plutôt que recréer des exceptions fiscales."),
  arg("Décider immédiatement la cible, mais étaler certaines transitions.", "Les droits acquis et les "
    + "situations constituées peuvent nécessiter une extinction progressive."),
  arg("Rendre la réforme crédible.", "Hausses, baisses et compensations doivent être votées ensemble "
    + "pour éviter que seules les premières soient effectivement mises en œuvre : une réforme d'ensemble, "
    + "aux éléments indissociables, qui appelle un mandat clair."),
  arg("Un calendrier en plusieurs temps.", "Commencer par ce qui se finance de soi-même — le troc aides "
    + "contre impôts de production, la TVA sociale — avant les réformes dont le rendement est plus long à "
    + "venir."),

  // ---------------------------------------------------------------- Points ouverts
  partie("Pour la discussion", "Éléments à trancher avec la fondation"),
  cadre("Les points sur lesquels deux options restent ouvertes. Pour chacun, l'option retenue dans ce "
    + "plan, puis l'alternative."),
  arg("Le niveau des prélèvements.", "Soit raisonner à recettes constantes, comme la thèse, en laissant "
    + "le niveau hors du champ ; soit fixer une cible : ramener la dépense vers une norme européenne "
    + "corrigée — environ 52 % du PIB en 2035, cinq points de moins qu'aujourd'hui — et les prélèvements "
    + "vers 42 %. Dans ce second cas, il faut encore choisir entre la norme corrigée et la convergence "
    + "complète vers la moyenne de la zone euro (49,4 % en 2024)."),
  arg("Les taux réduits de TVA.", "Soit les réduire fortement en compensant les ménages modestes par "
    + "les prestations ; soit les préserver sur les produits de première nécessité."),
  arg("La TVA sociale : quel prélèvement baisser ?", "Soit les cotisations patronales, ce qui réduit "
    + "directement le coût du travail ; soit les prélèvements salariés — CSG d'activité ou cotisations "
    + "vieillesse —, ce qui relève le salaire net sans baisser directement le coût du travail."),
  arg("La transmission.", "Soit exposer les arguments pour et contre sans trancher ; soit en faire un "
    + "axe du rapport, avec un impôt sur l'héritier calculé sur tout ce que chacun reçoit au cours de sa "
    + "vie (abattement élevé exonérant l'immense majorité, barème unique quel que soit le lien de "
    + "parenté, taux réduit pour ce qu'on reçoit jeune, sur le modèle irlandais), la plus-value "
    + "constatée au décès et payée à la revente, et la fermeture des portes de sortie (pacte Dutreil "
    + "plafonné à l'allemande, exit tax durcie, registre des transmissions). Ce second choix suppose de "
    + "corriger d'abord les inégalités qui tiennent à la naissance."),
  arg("Les impôts de production.", "Soit supprimer la C3S et refondre la CVAE ; soit supprimer la C3S, "
    + "la CVAE et la CFE, en rendant aux collectivités une ressource propre par une fiscalité foncière "
    + "modernisée plutôt que par une dotation."),
  arg("L'impôt sur les sociétés.", "Soit s'en tenir à l'assiette, pour que le taux affiché soit le taux "
    + "payé ; soit rendre l'IS progressif — léger pour les petites entreprises, plus lourd pour les très "
    + "grands bénéfices, apprécié au niveau du groupe pour éviter le fractionnement."),
  arg("Les plus-values.", "Soit rechercher la neutralité entre supports ; soit alléger leur imposition "
    + "pour récompenser la prise de risque, voire les exonérer après une longue détention."),
  arg("Les retraites.", "Soit s'en tenir à leur fiscalité ; soit traiter aussi le système : départ à "
    + "65 ans et 45 années de cotisation, un étage de capitalisation pour tous, et une architecture où la "
    + "solidarité — santé de base, famille, minima, autonomie — est financée par l'impôt, la retraite et "
    + "le chômage par la cotisation."),
  arg("Le titre.", "Soit « Un système fiscal pour la France au XXIe siècle » ; soit « Taxer ce qui se "
    + "transmet, libérer ce qui se crée », « Refonder l'impôt » ou « L'impôt de la puissance »."),
];

const enTete = new Header({ children: [new Paragraph({
  border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: BLEU_PALE, space: 4 } },
  children: [run("Un système fiscal pour la France au ", { italics: true, size: 16, color: GRIS }),
             ...siecle({ italics: true, size: 16, color: GRIS }),
             run(" — proposition de plan", { italics: true, size: 16, color: GRIS })],
})] });

const numeroPage = () => new Footer({ children: [new Paragraph({
  alignment: AlignmentType.CENTER,
  children: [new TextRun({ children: [PageNumber.CURRENT], size: 17, color: GRIS })],
})] });

const doc = new Document({
  creator: "Colin Baget",
  lastModifiedBy: "Colin Baget",
  title: "Un système fiscal pour la France au XXIe siècle — proposition de plan",
  styles: {
    default: {
      document: {
        run: { font: POLICE, size: 21, color: ENCRE, language: FR },
        paragraph: { spacing: { after: 80, line: 276, lineRule: LineRuleType.AUTO } },
      },
    },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: POLICE, size: 30, bold: true, color: BLEU },
        paragraph: {
          spacing: { before: 440, after: 200, line: 264, lineRule: LineRuleType.AUTO }, keepNext: true, outlineLevel: 0,
          border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: BLEU_PALE, space: 6 } },
        } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: POLICE, size: 23, bold: true, color: BLEU },
        paragraph: { spacing: { before: 280, after: 80 }, keepNext: true, outlineLevel: 1 } },
    ],
  },
  numbering: {
    config: [{
      reference: "puces",
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: "▪", alignment: AlignmentType.LEFT,
        style: {
          run: { color: BLEU },
          paragraph: { indent: { left: 400, hanging: 260 }, spacing: { after: 90 } },
        },
      }],
    }],
  },
  sections: [{
    properties: {
      titlePage: true,
      page: { margin: { top: 1250, bottom: 1250, left: 1320, right: 1320, header: 620, footer: 620 } },
    },
    headers: { first: new Header({ children: [new Paragraph({ children: [] })] }), default: enTete },
    footers: { first: numeroPage(), default: numeroPage() },
    children: contenu,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  const sortie = path.join(__dirname, "plan-rapport.docx");
  fs.writeFileSync(sortie, buf);
  console.log("écrit :", sortie);
});
