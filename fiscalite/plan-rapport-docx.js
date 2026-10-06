// Plan détaillé au format Word.
// Régénération : npm install docx, puis node plan-rapport-docx.js (écrit plan-rapport.docx).
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Header, Footer, AlignmentType,
  HeadingLevel, LevelFormat, BorderStyle, PageNumber,
} = require("docx");

const POLICE = "Cambria";
const ENCRE = "1A1A19";
const OCRE = "C79100";
const FR = { value: "fr-FR" };

// Typographie française : espaces insécables avant la ponctuation haute et dans les guillemets.
const fr = (s) => s
  .replace(/'/g, "’")
  .replace(/ :/g, " :")
  .replace(/ ([;?!])/g, " $1")
  .replace(/« /g, "« ").replace(/ »/g, " »")
  .replace(/(\d) %/g, "$1 %")
  .replace(/(\d) (\d{3})(?!\d)/g, "$1 $2")
  .replace(/ €/g, " €")
  .replace(/(\d) (milliards|points|ans)/g, "$1 $2");

const run = (texte, opts = {}) => new TextRun({ text: fr(texte), language: FR, ...opts });

const para = (texte, opts = {}) => new Paragraph({ children: [run(texte)], ...opts });

// Un argument : affirmation en italique, puis son développement.
const arg = (affirmation, suite = "") => new Paragraph({
  numbering: { reference: "puces", level: 0 },
  children: suite ? [run(affirmation, { italics: true }), run(" " + suite)]
                  : [run(affirmation, { italics: true })],
});

const partie = (titre) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [run(titre)] });
const chapitre = (titre) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [run(titre)] });
const cadre = (texte) => new Paragraph({ children: [run(texte)], spacing: { after: 60 } });

const siecle = (opts = {}) => [
  run("XXI", opts), run("e", { ...opts, superScript: true }), run(" siècle", opts),
];

const contenu = [
  new Paragraph({
    spacing: { after: 80 },
    children: [run("PLAN DÉTAILLÉ", { bold: true, size: 16, color: OCRE, characterSpacing: 20 })],
  }),
  new Paragraph({
    spacing: { after: 160 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: ENCRE, space: 6 } },
    children: [run("Un système fiscal pour le ", { bold: true, size: 36 }), ...siecle({ bold: true, size: 36 })],
  }),
  new Paragraph({
    spacing: { before: 120, after: 120 },
    children: [
      run("La thèse.", { bold: true }),
      run(" À niveau de recettes et de redistribution donnés, toutes les architectures fiscales ne se "
        + "valent pas. Il est possible de concevoir un système plus simple, plus neutre et moins "
        + "destructeur d'activité sans renoncer à ses objectifs de justice ou de financement."),
    ],
  }),

  partie("Première partie — Qu'est-ce qu'un bon impôt ?"),

  chapitre("1. Le pacte fiscal : les principes qui fondent l'impôt"),
  cadre("Partir de la Déclaration de 1789 comme socle commun, et en tirer la grille qui servira à juger "
    + "tout le reste."),
  arg("La Déclaration pose quatre conditions.", "La contribution est nécessaire, répartie selon les "
    + "facultés de chacun, consentie, et son emploi est contrôlé."),
  arg("Elles se traduisent en exigences simples.", "L'impôt doit être légitime, proportionné, "
    + "compréhensible, et ne pas imposer de prélèvement ou de coût qui ne soit justifié par un objectif "
    + "collectif — frais de gestion et coût de conformité compris."),
  arg("Un impôt juste ne se réduit donc pas à son barème.", "Il doit aussi respecter les libertés, la "
    + "capacité contributive et le consentement."),

  chapitre("2. Financer, orienter, corriger : le triangle de l'impôt"),
  cadre("Présenter les trois grandes fonctions du système fiscal à partir d'exemples concrets, puis "
    + "montrer pourquoi aucun impôt ne peut les remplir toutes."),
  arg("Financer l'action publique :", "lever les recettes nécessaires aux dépenses collectives, en "
    + "limitant autant que possible le coût économique du prélèvement."),
  arg("Orienter les comportements :", "encourager ou décourager certains comportements, notamment "
    + "lorsqu'ils produisent des externalités — pollution, tabac."),
  arg("Corriger les inégalités :", "répartir l'effort selon les facultés contributives et assurer le "
    + "degré de redistribution souhaité collectivement, ce qui pose la question du meilleur instrument : "
    + "la progressivité et les dispositifs fiscaux, ou les dépenses publiques et les transferts sociaux ?"),
  arg("Ces objectifs entrent en tension, et l'intuition de Tinbergen dit pourquoi :", "plusieurs "
    + "objectifs nécessitent généralement plusieurs instruments."),
  arg("On ne doit donc pas demander à chaque impôt d'être à la fois efficace, redistributif et "
    + "incitatif.", "C'est l'ensemble du système fiscal et social qui doit tenir les trois sommets du "
    + "triangle."),

  chapitre("3. Prélever mieux : ce que nous apprend l'économie de l'impôt"),
  cadre("Présenter de manière pédagogique, à partir d'exemples concrets, quatre grands enseignements de "
    + "la littérature sur la taxation optimale."),
  arg("Tout impôt a un coût économique.", "Expliquer la perte sèche à partir d'un échange rendu "
    + "impossible par l'impôt — un vendeur prêt à céder à 200 000 €, un acheteur prêt à payer 210 000, "
    + "et 8 % de droits de mutation entre les deux : la vente n'a pas lieu, personne ne paie l'impôt et "
    + "le gain de l'échange est perdu pour tous. Puis introduire les taux marginaux, les réactions "
    + "comportementales, les élasticités et l'intuition de la courbe de Laffer : taxer davantage une "
    + "activité peut réduire l'assiette au point de faire baisser la recette."),
  arg("Tous les impôts ne sont pas également efficaces.", "Pourquoi privilégier des assiettes larges et "
    + "des taux bas ? Pourquoi rechercher la neutralité fiscale, éviter de taxer les intrants et "
    + "privilégier les assiettes peu élastiques ? Introduire la fiscalité pigouvienne, et le classement "
    + "des impôts selon leurs effets sur la croissance établi par l'OCDE, avec ses limites — à commencer "
    + "par celle que reconnaissent ses auteurs, qui jugent eux-mêmes excessive l'ampleur des effets "
    + "estimés."),
  arg("Celui qui paie l'impôt n'est pas toujours celui qu'on croit.", "Introduire l'incidence fiscale : "
    + "une taxe sur les entreprises peut être supportée par les salariés, les consommateurs ou les "
    + "actionnaires, la charge retombant sur celui qui peut le moins s'y soustraire. La répartition "
    + "réelle de l'impôt ne correspond pas nécessairement à sa répartition juridique."),
  arg("La justice fiscale se juge à l'échelle du système.", "Un impôt isolément régressif peut "
    + "s'inscrire dans un système globalement redistributif. Expliquer pourquoi une TVA uniforme "
    + "accompagnée de transferts ciblés peut être plus efficace et tout aussi redistributive qu'une TVA "
    + "à taux réduits — c'est le sens du résultat d'Atkinson et Stiglitz : un taux réduit profite "
    + "davantage, en euros, aux ménages qui consomment le plus."),
  para("La partie se referme sur la thèse, qui en découle. Si ces principes sont relativement simples, "
    + "comment la France s'en est-elle à ce point éloignée ?", { spacing: { before: 120 } }),

  partie("Deuxième partie — Comment la France a perdu le fil"),
  para("Partie narrative, lisible d'une traite. La comparaison internationale n'a pas de chapitre "
    + "autonome : elle sert de test à chaque anomalie — est-elle réellement française, et d'autres pays "
    + "atteignent-ils le même degré de redistribution avec une architecture différente ?"),

  chapitre("4. Un système que personne n'a vraiment dessiné"),
  cadre("Raconter comment le système s'est construit par strates, chaque époque répondant à son "
    + "problème sans que personne ne refasse l'ensemble."),
  arg("Un impôt se choisit d'abord parce qu'il est facile à lever.", "La contribution des portes et "
    + "fenêtres, créée en 1798 et supprimée en 1926, était facile à constater ; elle a muré les façades "
    + "pendant un siècle."),
  arg("1945 : la protection sociale est assise sur le salaire.", "Le choix convenait au plein emploi "
    + "et à une population active en croissance ; il lie pour un demi-siècle le financement social au "
    + "coût du travail."),
  arg("1991 : la CSG tente d'en sortir, et s'arrête à mi-chemin.", "Premier prélèvement assis sur tous "
    + "les revenus ; la CRDS, créée en 1996 pour treize ans, est toujours là."),
  arg("Depuis 1993, on corrige le coût du travail au lieu de changer d'assiette.", "Allègements "
    + "empilés, CICE, puis sa bascule en allègements, chacun avec son seuil et son plafond."),

  chapitre("5. Beaucoup prélever, mais surtout mal prélever"),
  cadre("Une photographie du système actuel : où la France viole-t-elle le plus clairement les principes "
    + "de la première partie ?"),
  arg("La France prélève beaucoup parce qu'elle dépense beaucoup.", "Dépense publique de 57,0 % du PIB "
    + "contre 49,4 % en zone euro, prélèvements de 45,3 % contre 40,8 %, le solde étant emprunté "
    + "(Eurostat, 2024)."),
  arg("La structure est un problème indépendant du niveau.", "On peut prélever 40 % du PIB aussi mal "
    + "que 45."),
  arg("L'euro suivant est le plus taxé au bas de l'échelle des salaires.", "Un célibataire sans enfant "
    + "est prélevé à 64,6 % autour de 67 % du salaire moyen, contre 58,2 % au salaire moyen."),
  arg("La production est taxée avant le profit.", "77 milliards sont dus même quand l'entreprise perd "
    + "de l'argent, à rebours de la règle qui commande de ne pas taxer les intrants."),
  arg("L'épargne est taxée selon son enveloppe, et le sol sur une photographie de 1970.", "Le même "
    + "rendement est imposé de 0 à 55 % selon le support ; la taxe foncière des logements repose "
    + "toujours sur les valeurs locatives de 1970."),
  arg("Au total, la structure est presque à l'envers du classement de l'OCDE.", "25,9 points de PIB "
    + "dans l'avant-dernière catégorie contre 17,5 en moyenne, et le seul prélèvement inférieur à la "
    + "moyenne porte sur la catégorie jugée la plus nocive."),

  chapitre("6. Quand la complexité finit par miner l'efficacité et la justice"),
  cadre("Montrer que la complexité coûte, en efficacité comme en justice, et expliquer pourquoi elle se "
    + "maintient."),
  arg("L'État taxe, puis corrige sa propre taxe.", "Le cas du travail n'est pas isolé : on taxe la "
    + "production puis on verse des aides, on institue un impôt général puis un taux réduit, on crée une "
    + "niche puis un plafonnement de niches. Le système produit ses propres antidotes."),
  arg("Chaque correctif crée de nouveaux arbitrages.", "Optimisation, requalification, et des taux "
    + "affichés qui ne disent plus les taux payés : 474 dépenses fiscales pour 91,8 milliards, dont la "
    + "Cour des comptes écrit que le coût n'est pas connu."),
  arg("La redistribution devient illisible.", "Impôts progressifs, taxes proportionnelles, cotisations, "
    + "exonérations, prestations, avantages liés à l'âge ou au statut : plus personne ne sait dire qui "
    + "paie quoi, d'où des controverses qu'aucun chiffre ne tranche."),
  arg("Le consentement s'use.", "L'article 14 donne à chacun le droit de constater la nécessité de la "
    + "contribution et d'en suivre l'emploi ; un système illisible vide ce droit de sa substance."),
  arg("Et le système survit parce que ses pertes sont concentrées et ses gains diffus.", "Une niche a "
    + "des bénéficiaires qui savent exactement ce qu'ils perdent, quand celui qui gagne cent euros à une "
    + "baisse générale de taux ignore d'où ils viennent ; certains impôts durent parce qu'ils sont peu "
    + "visibles ou faciles à collecter."),
  para("Le problème français n'est donc pas seulement que nous prélevons beaucoup, ni que notre système "
    + "est compliqué : nous avons progressivement substitué l'accumulation de prélèvements, d'exceptions "
    + "et de compensations à une architecture fiscale cohérente. Si l'on cessait de corriger à la marge "
    + "et qu'on essayait enfin de redessiner, que ferait-on ?", { spacing: { before: 120 } }),

  partie("Troisième partie — Quel système fiscal pour la France ?"),
  para("Le mouvement est le suivant : voilà le système qu'on peut construire, voilà les choix qui restent "
    + "ouverts à l'intérieur de ce système, voilà pourquoi il est difficile d'y arriver."),

  chapitre("7. À quoi ressemblerait concrètement un système fiscal plus simple et plus efficace ?"),
  cadre("Passer des principes aux instruments, assiette par assiette, et montrer qu'on peut réellement "
    + "lever les recettes autrement."),
  arg("Beaucoup moins de niches et d'abattements,", "y compris ceux qui tiennent au statut comme "
    + "l'abattement de 10 % sur les pensions : c'est ce qui finance la baisse des taux partout ailleurs."),
  arg("Un impôt sur le revenu à assiette plus large et à taux plus faibles."),
  arg("Une TVA avec beaucoup moins de taux réduits."),
  arg("Une fiscalité de l'épargne plus homogène."),
  arg("Moins de taxation des intrants et de la production,", "selon le principe « zéro aide contre zéro "
    + "impôt de production »."),
  arg("Une fiscalité pigouvienne assumée", "lorsqu'il s'agit de corriger une externalité, à commencer "
    + "par la taxe carbone."),
  arg("Et la preuve que les comptes tombent :", "un tableau en deux colonnes — ce que rapporte chaque "
    + "assiette aujourd'hui, ce qu'elle rapporterait après réforme — et l'effet sur quelques cas types "
    + "et sur les déciles publiés."),

  chapitre("8. Les grands arbitrages : où déplacer la charge fiscale ?"),
  cadre("Une fois les principes posés, certains choix restent discutables et dépendent aussi de "
    + "préférences collectives ; le chapitre les traite comme tels."),
  arg("Faut-il déplacer une partie de la taxation du travail vers la consommation ?", "Le débat sur la "
    + "TVA sociale, avec les précédents allemand de 2007 et danois, et l'échec français de 2012."),
  arg("Quelle place donner à la taxation des transmissions ?", "Un encadré contradictoire. Pour : c'est "
    + "le revenu le moins lié à l'effort et le plus concentré. Contre : c'est l'impôt le plus rejeté, il "
    + "frappe une épargne déjà imposée, et son rendement dépend de la capacité à retenir des assiettes "
    + "mobiles."),
  arg("Comment traiter l'épargne ?", "Arbitrer entre rendement normal, rente et prise de risque."),

  chapitre("9. Pourquoi passer au système cible est si difficile"),
  cadre("Les pertes concentrées et les gains diffus décrits en deuxième partie, vus cette fois du côté "
    + "de celui qui réforme, et ce qu'ils imposent comme méthode."),
  arg("Certaines baisses d'impôt sont politiquement difficiles,", "notamment pour les entreprises."),
  arg("Il faut préserver le rendement et la redistribution,", "et compenser les ménages réellement "
    + "perdants."),
  arg("Le risque principal est que les hausses soient votées avant les compensations."),
  arg("D'où la méthode :", "réformer par paquets cohérents, chaque suppression votée dans le même texte "
    + "que sa compensation, avec une transition progressive."),
];

const doc = new Document({
  creator: "Colin Baget",
  lastModifiedBy: "Colin Baget",
  title: "Un système fiscal pour le XXIe siècle — plan détaillé",
  styles: {
    default: {
      document: {
        run: { font: POLICE, size: 21, color: ENCRE, language: FR },
        paragraph: { spacing: { after: 80, line: 264 } },
      },
    },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: POLICE, size: 27, bold: true, color: ENCRE },
        paragraph: { spacing: { before: 320, after: 120 }, keepNext: true, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: POLICE, size: 22, bold: true, color: ENCRE },
        paragraph: { spacing: { before: 200, after: 60 }, keepNext: true, outlineLevel: 1 } },
    ],
  },
  numbering: {
    config: [{
      reference: "puces",
      levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 400, hanging: 240 }, spacing: { after: 50 } } } }],
    }],
  },
  sections: [{
    properties: {
      titlePage: true,
      page: { margin: { top: 1250, bottom: 1250, left: 1300, right: 1300, header: 600, footer: 600 } },
    },
    headers: {
      first: new Header({ children: [new Paragraph({ children: [] })] }),
      default: new Header({ children: [new Paragraph({
        border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: ENCRE, space: 4 } },
        children: [run("Un système fiscal pour le ", { italics: true, size: 17 }),
                   ...siecle({ italics: true, size: 17 }),
                   run(" — plan détaillé", { italics: true, size: 17 })],
      })] }),
    },
    footers: {
      first: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
        children: [new TextRun({ children: [PageNumber.CURRENT], size: 17 })] })] }),
      default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
        children: [new TextRun({ children: [PageNumber.CURRENT], size: 17 })] })] }),
    },
    children: contenu,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  const sortie = path.join(__dirname, "plan-rapport.docx");
  fs.writeFileSync(sortie, buf);
  console.log("écrit :", sortie);
});
