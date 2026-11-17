# Bloc « fiscalité du capital », v4 : ce qui change

*Script : `calculs/pfu4_equivalence.py` (→ `pfu4.json`, `pfu4_calculs.txt`). Il importe `pfu3_neutralite.py`, qui
n'est pas modifié. Recettes, règle (iv), Dutreil, table annuelle : pfu3 inchangé. Annexe : `annexes/annexe_pfu.tex`
(nouvelles sections « Conditions exactes de l'équivalence » et « Doctrine de long terme », exit tax réécrite).*

## 1. Conditions exactes de l'équivalence [S]

Règle : t·a = D(V) − D(V − tG). L'égalité des charges `D(V) + t(G − a) = tG + D(V − tG)` est **exacte pour une revente
immédiate**, quel que soit le barème, le lien de parenté ou l'abattement, puisque `a` est calculé sur les droits de
chaque bénéficiaire (a = 270 k€ pour un enfant, 405 k€ pour un frère, 495 k€ pour un neveu, 0 pour le conjoint ;
exemple 100 k€ → 1 M€). Il faut trois conditions :
1. **Même PFU à la vente qu'au calcul de a.** Sinon l'écart vaut (t' − t)(G − a) : −3 150 € si le PFU passe à 30,9 %
   (fin de la CRDS), −40 320 € à 25 %.
2. **Droits de droit commun.** Sous pacte Dutreil, l'écart restant est l'exonération elle-même.
3. **Chaque héritier porte l'impôt latent de ses titres.** L'égalité est exacte si les titres sont partagés au prorata
   des parts. S'ils vont à un seul enfant, elle reste exacte dans une même tranche, sinon l'écart est faible (+14 824 €
   pour 1,2 M€ de titres et 1,2 M€ de maison). Mais cet enfant supporte seul l'impôt (222 k€ contre 173 k€ chacun si le
   parent avait vendu). Le partage devrait évaluer les titres nets de l'impôt latent [à expertiser].

**Revente différée.** On compare l'héritier qui garde les titres et celui qui a replacé le produit dans le même actif.
La valeur gagne F = (1+g)^n et l'actualisation se fait au taux ρ :
`W_B − W_A = [tG(1 − t)(F − 1) + t·a]/(1+ρ)^n − t·a`. Exemple à 10 ans : +35 391 € (3,5 % de V) si g = ρ = 4 % ; ≈ 0
(+1 175 €) si la valeur suit l'inflation (g = 2 %, ρ = 4 %) ; −27 506 € à valeur constante (a n'est pas revalorisé) ;
+68 165 € à 25 ans. C'est l'avantage du report propre à toute imposition à la réalisation, pas un effet de la
transmission.

**Phrase pour la note** (remplace « transmettre puis vendre coûte exactement ce que coûte vendre puis transmettre ») :
« Résultat : l'héritier qui vend aussitôt paie exactement ce qu'auraient payé son parent et lui si le parent avait
vendu ; s'il garde les titres, il bénéficie du même report d'impôt que tout détenteur. » Titre de g9 : ajouter « en cas
de revente immédiate ».

## 2. Doctrine de long terme (deux paragraphes pour la note) [C]

**La réforme améliore la neutralité entre vendre et transmettre, au prix possible de celle entre consommer et
épargner.** Fermer l'effacement supprime l'incitation à garder ses titres jusqu'au décès. Mais elle alourdit la
taxation de l'épargne accumulée. Un partisan de la taxation de la consommation objectera que le rendement normal de
l'épargne, qui ne fait que rémunérer l'attente, ne devrait pas être taxé, et que taxer davantage des plus-values de
long terme, en partie nominales, creuse l'écart entre consommer aujourd'hui et consommer demain. L'objection est
fondée : nous corrigeons une anomalie de l'imposition à la vente, nous ne construisons pas un impôt sur la dépense.

**À long terme, taxer les gains réels et les rentes, pas l'attente.** Une fois les recettes de l'élargissement
constatées, trois chantiers suivront. D'abord, distinguer plus-values réelles et nominales en indexant le prix
d'acquisition (0,6 à 0,9 Md€ par an). Ensuite, réexaminer la taxation du rendement normal, par exemple par une
déduction du rendement sans risque, sur le modèle norvégien [non relu, à expertiser]. Enfin, baisser le PFU à mesure
que l'assiette élargie rapporte. L'élargissement vient d'abord, parce qu'il rend une baisse de taux durable ; l'ordre
inverse creuserait le déficit sans corriger l'anomalie.

## 3. Exit tax : arbitrage à expertiser, pas de durcissement mécanique [C]

- **Régime** : sursis automatique dans l'UE et l'EEE ; dégrèvement après 2 ans, 5 ans au-delà de 2,57 M€ (LF 2019,
  qui a remplacé les 15 ans) [S, texte du CGI non relu]. Des amendements au PLF 2026
  qui rétablissaient le régime initial ont été rejetés au Sénat (au moins un).
- **Rendement** [E] : 138 M€ encaissés de 2012 à 2017, soit environ 23 M€ par an, pour 5,75 Md€ d'impositions
  théoriques (réponse ministérielle, JO Sénat, 2018). En 2011, 158 foyers déclaraient 1,35 Md€ de plus-values (chiffre
  tiré d'un amendement, non vérifié). Aucune évaluation française des départs n'a été trouvée.
- **Norvège** [E] : la fin des échappatoires au départ, la hausse de l'impôt sur la fortune et celle sur les dividendes
  ont provoqué au plus une centaine de départs, presque tous dans le dernier millième. La hausse des recettes de l'impôt
  sur la fortune est passée de 75 % à 71,5 % (Ring, NBER WP 35854, 2026).
- **Arbitrage** : un délai long protège l'impôt latent, qui grossit avec la fin de l'effacement. Mais le régime
  2011-2018 a peu rapporté, le sursis est de droit dans l'UE, et un délai long peut aussi dissuader les installations.
  **À expertiser** : données DGFiP sur les départs, sursis et dégrèvements depuis 2019 ; droit de l'Union et
  conventions ; imposition de la plus-value transmise à un non-résident.
- **Phrase pour la note** (remplace « nous proposons de durcir l'exit tax ») : « Faut-il durcir l'exit tax ? Elle a
  peu rapporté et ses effets sur les départs ne sont pas mesurés : nous en faisons un arbitrage à expertiser, pas un
  durcissement automatique. »

## Sources ajoutées

- Réponse ministérielle, JO Sénat (question n° 05844, 2018) ; amendements Sénat LF 2026 (I-1319, I-1388, I-1497).
- Ring, M. (2026), « Taxing Entrepreneurial Wealth: Evidence from Norway, 2021–2025 », NBER WP 35854 (résumé lu).
- Commentaire doctrinal, Études fiscales internationales (15/6/2026) : régime de l'art. 167 bis.
