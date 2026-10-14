# Santé hors Eurostat : notes de sources (`sante_ext`)

Fichiers : `sante_ext.py` (fonctions `telecharger(dossier_brut)` et `extraire(dossier_brut)`), `sante_ext.csv` (format long : `pays, indicateur, annee, valeur, source, note`).
Exécution : `python -I sante_ext.py`, ou `--sans-telechargement` pour relire les fichiers bruts déjà présents.
Fichiers bruts : `.../scratchpad/efficience/sante_raw/`. Extraction du 14/10/2026.
Pays : les 27 de l'UE en codes Eurostat (EL pour la Grèce). Les codes ISO3 de l'OCDE et de l'OMS sont convertis.
La colonne `note` donne l'unité, le type de série et les drapeaux de la source (rupture, estimation, définition différente, provisoire).

Synthèse de couverture (CSV de 3 746 lignes) :

| indicateur | pays | années | absents |
|---|---|---|---|
| sante_ima30 | 24 | 2000-2024 | BG, CY, EL |
| sante_antibiotiques | 25 | 1997-2025 | CY, MT |
| sante_depenses_catastrophiques | 27 | 2000-2021 (irrégulier) | aucun |
| sante_attente | 11 | 2000-2025 | 16 pays, dont FR et DE |
| sante_rd_pharma_ratio | 26 | 2006-2024 | LU |
| sante_surmortalite_12m | 27 | 2020-2025 | aucun |
| sante_inegalite_densite (et `_pond`) | 20 | 1993-2025 | CY, EE, LU, LV, MT (une seule région NUTS 2), DE, IE (pas de données régionales) |

Indicateurs complémentaires, hors identifiants imposés, à utiliser ou non : `sante_ima30_nonchaine`, `sante_attente_mediane`, `sante_attente_silc`, `sante_inegalite_densite_pond`.

---

## sante_ima30 : mortalité à 30 jours après infarctus

- **Source** : OCDE, Health Care Quality Indicators. Flux SDMX `OECD.ELS.HD:DSD_HCQO@DF_AC(2.1)`, `https://sdmx.oecd.org/public/rest/data/OECD.ELS.HD,DSD_HCQO@DF_AC,2.1/all`.
- **Définition** : décès dans les 30 jours après une admission pour IAM, patients de 45 ans et plus. Taux standardisé par âge et sexe (`METHODOLOGY=AGE_SEX_STANDARD`), deux sexes, valeur observée.
  - `MORTAMIO` : données **chaînées** (linked), décès à l'hôpital ou hors de l'hôpital, pour 100 patients.
  - `MORTAMII` : données **non chaînées** (unlinked), décès dans le même séjour hospitalier, pour 100 admissions.
- **Règle appliquée, pays par pays** : on retient toute la série chaînée si le pays en a une, sinon la série non chaînée. La `note` de chaque ligne indique le type retenu.
  - Série chaînée : CZ, DK, EE, ES, FI, FR, HR, HU, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK.
  - Série non chaînée : AT, BE, DE, IE.
  - Aucune donnée : BG, CY, EL.
- **Attention** : les deux séries ne sont pas comparables entre elles. La série chaînée est plus élevée, car elle compte aussi les décès après la sortie. En France en 2015, elle vaut 8,6 contre 5,5 pour la non chaînée. Le classement mélange donc deux définitions. `sante_ima30_nonchaine` donne la série non chaînée pour 23 pays, ce qui permet une comparaison homogène.
- **Profondeur de série** : la série chaînée est parfois plus courte que la non chaînée.
  - FR : chaînée 2013-2017 seulement, non chaînée 2005-2015.
  - LU : chaînée 2003-2015, non chaînée jusqu'en 2023.
  - PT : chaînée 2011-2022, non chaînée jusqu'en 2024.
- **Contrôle France** : 9,2 (2013), puis 7,2 (2017). Le dernier point de la France date de 2017, ce qui est cohérent avec Panorama de la santé. Fourchette des dernières valeurs : NL 5,0 à LV 15,4.

## sante_antibiotiques : consommation d'antibiotiques (J01)

- **Source retenue : repli OCDE.** Health Statistics, flux `OECD.ELS.HD:HEALTH_PHMC@DF_PHMC_CONSUM(1.1)`, `PHARMACEUTICAL=J01`, `UNIT_MEASURE=DDD_10P3HB`.
- **Unité** : doses définies journalières (DDD) pour 1 000 habitants et par jour.
- **Pourquoi pas l'ECDC (ESAC-Net)** : la source n'est pas accessible en données brutes.
  - Le Surveillance Atlas (`atlas.ecdc.europa.eu`) n'a pas de jeu AMC.
  - Le tableau de bord AMC est une application Qlik (`qap.ecdc.europa.eu`, app `8b011a4c-…`). Son moteur websocket renvoie 403 aux clients hors navigateur.
  - Dans les rapports annuels 2023 et 2024 (PDF), les tableaux par pays sont des images.
  - Les « downloadable tables » 2021 et 2022 (xlsx) ne donnent que les sous-groupes ATC, pas le total J01.
  - Ces fichiers sont conservés dans `sante_raw/ecdc/`.
- **Contrôle croisé avec l'ECDC** (rapport ESAC-Net 2024, texte, consommation totale 2024) : NL 9,8 et EL 29,9 dans l'OCDE comme dans l'ECDC. L'OCDE reprend donc le total ville + hôpital d'ESAC-Net, au moins pour ces pays.
- **Limites** :
  - Le flux SDMX ne dit pas, pays par pays, si la valeur couvre le total ou la ville seule. Selon l'ECDC, AT et DE ne déclarent que la ville, et CY et CZ un total non ventilé.
  - Les drapeaux OCDE figurent dans `note`, par exemple « définition différente ».
  - La valeur EL 2025 (27,8) est la seule observation de 2025.
  - CY et MT sont absents.
- **Contrôle France** : 30,6 (1997), 25,1 (2019), 20,3 (2020, effet Covid), 26,5 (2024). Ordre de grandeur cohérent avec l'ECDC, où la France fait partie des pays à forte consommation.

## sante_depenses_catastrophiques : dépenses de santé catastrophiques

- **Source** : OMS Europe, European Health Information Gateway, indicateur `UHCFP_4` « The share of all households with catastrophic health spending » (jeu UHCFP, *Monitoring financial protection in the European Region*).
  - Export : `https://dw.euro.who.int/api/v5/export/UHCFP_4?lang=EN&format=csv`, qui renvoie une URL de téléchargement.
  - Fichier généré par l'OMS le 22/04/2026.
- **Définition (mesure OMS Europe, et non ODD 3.8.2)** : part des **ménages** dont le reste à charge dépasse **40 % de la capacité à payer**. La capacité à payer est la consommation du ménage moins un montant normatif pour les besoins de base (alimentation, logement, charges).
  - Ce n'est pas le seuil ODD 3.8.2 de 10 % ou 25 % du budget total, qui porte sur la population. Ce dernier n'est pas repris.
- **Unité** : % des ménages.
- **Couverture** : 27 pays, mais les points sont rares et irréguliers, car ils suivent les enquêtes budget des ménages. Dernière année : de 2015 (AT, DK, NL, SE…) à 2021 (PL).
- **Contrôle France** : 1,97 % (2011) et 2,07 % (2017), parmi les plus bas de l'UE. Fourchette des dernières valeurs : NL 0,5 % à BG 19,2 %.
- **TLS** : `dw.euro.who.int` n'envoie pas son certificat intermédiaire (Sectigo DV R36).
  - Le module ajoute cet intermédiaire public au magasin de confiance (`SECTIGO_DV_R36_PEM`, tiré de Mozilla CCADB, empreinte SHA-256 dans le code).
  - La vérification TLS reste complète : chaîne jusqu'à la racine système et contrôle du nom d'hôte.
- **Lacune** : la plateforme « UHC watch » (déc. 2024) contient peut-être des années plus récentes. Elle n'a pas d'API identifiée, donc l'extraction s'arrête à la passerelle.

## sante_attente : temps d'attente (indicateur ambigu)

- **Ambiguïté** : le bulletin parle de « temps d'attente moyen » sans préciser l'intervention ni la source. Aucune mesure n'est à la fois harmonisée et disponible pour les 27 pays. Trois séries sont fournies :
  1. **`sante_attente` (retenu)** : OCDE, flux `OECD.ELS.HD:DSD_HEALTH_PROC@DF_WAITING(1.2)`.
     - Mesure : délai **moyen** (`WAIT_MEAN`) en jours, de l'avis du spécialiste à l'intervention (`WAITING_TIME=WTSP`), pour une **prothèse de hanche** (`CM8151_8153`).
     - La moyenne a été préférée à la médiane parce que le bulletin dit « moyen » et parce qu'elle couvre plus de pays : LT et NL en plus.
     - Pays : DK, EE, ES, FI, HU, IT, LT, NL, PL, PT, SE (2000-2025).
     - **France, Allemagne et 14 autres pays ne déclarent pas ces délais à l'OCDE.**
  2. `sante_attente_mediane` : même champ, médiane (indicateur vedette de l'OCDE). 10 pays.
  3. `sante_attente_silc` : Eurostat `hlth_silc_08` (EU-SILC), `reason=WLIST`, 16 ans et plus.
     - Mesure : % de la population déclarant un besoin d'examen médical non satisfait **à cause d'une liste d'attente**.
     - Couvre 27 pays, de 2008 à 2025. Ce n'est pas un délai : la mesure recoupe l'indicateur « besoins non satisfaits » traité ailleurs.
- **Contrôles** :
  - OCDE, moyenne la plus récente : de DK (43 jours) à EE (452 jours, 2020). Médiane des pays : 160 jours. IT 2025 : 84 jours (médiane 45).
  - EU-SILC France : 0,2 % à 0,5 % avant 2020, puis 1,4 % à 1,8 % en 2023-2025.

## sante_rd_pharma_ratio : R&D pharmaceutique rapportée à la dépense pharmaceutique

- **Construction** : `100 × BERD(NACE C21) / dépense HC.5.1`, en %, les deux termes en millions d'euros courants.
  - BERD : Eurostat `rd_e_berdindr2`, `nace_r2=C21` (fabrication de produits pharmaceutiques de base et de préparations pharmaceutiques), `unit=MIO_EUR`.
  - Dépense : Eurostat `hlth_sha11_hc`, `icha11_hc=HC51` (produits pharmaceutiques et autres biens médicaux non durables, tous financeurs), `unit=MIO_EUR`.
  - La `note` donne les deux montants et leurs drapeaux.
- **Limites** :
  - **Numérateur** : la BERD est classée selon l'activité principale de l'entreprise. Les centres de R&D des groupes pharmaceutiques classés ailleurs (R&D, M72, ou holdings) ne sont pas comptés, ce qui sous-estime la R&D dans certains pays. Quelques pays ont des années confidentielles. LU n'a aucune année.
  - **Dénominateur** : HC.5.1 est la dépense pharmaceutique **de ville**. Les médicaments délivrés à l'hôpital sont exclus, ce qui majore le ratio.
  - Les deux montants sont convertis en euros au taux de change courant.
- **Rupture en France** : la BERD C21 passe de 758 M€ (2020) à 2 185 M€ (2021) sans drapeau de rupture chez Eurostat. Le ratio passe de 2,3 % à 6,3 %. C'est très probablement une rupture de méthode (profilage des groupes ou reclassement d'activité), mais je ne l'ai pas vérifiée. Ne pas comparer la France avant et après 2021 sans contrôle.
- **Ordres de grandeur** : FR 2,3-3,3 % (2007-2020), puis 5,9-6,5 % (2021-2024). DE environ 8-10 %. IT environ 2-3 %. ES environ 4 %. BE 23-58 %. DK jusqu'à 79 %. Médiane des dernières années : 4,1 %. Les très fortes valeurs (BE, DK, IE) reflètent des industries exportatrices.
- **Non utilisé** : EFPIA, *The Pharmaceutical Industry in Figures*. Il n'existe pas de série par pays téléchargeable, seulement des PDF annuels.

## sante_surmortalite_12m : surmortalité

- **Source** : Eurostat `demo_mexrt` (surmortalité mensuelle, % par rapport à la moyenne 2016-2019 du même mois), `unit=PC`.
- **Calcul** : **moyenne arithmétique des 12 taux mensuels** de l'année civile. Les années incomplètes ne sont pas calculées ; 2026, partielle, est exclue. Ce n'est pas un taux annuel pondéré par les décès, ni une fenêtre glissante de 12 mois.
- **Années** : 2020-2025, 27 pays.
- **Contrôle France** : 10,5 % (2020), 9,6 % (2021), 11,9 % (2022), 6,1 % (2023), 6,7 % (2024), 7,3 % (2025).

## sante_inegalite_densite / sante_inegalite_densite_pond : inégalité territoriale de densité médicale

- **Données** :
  - Densité de médecins pour 100 000 habitants par région NUTS 2 (`P_HTHAB`, et effectifs `NR`).
    - Série courante : Eurostat `hlth_rs_physreg`.
    - Complément : série historique `hlth_rs_prsrg` (`isco08=OC221`, 1993-2021), pour les couples région-année absents de la série courante. En pratique, la série courante n'a presque rien entre 2011 et 2020.
  - Population : Eurostat `demo_r_pjanaggr3` (sexe T, tous âges, 1er janvier).
- **Cohérence du découpage** : les séries mélangent des codes de plusieurs versions NUTS la même année (par ex. 53 « régions » françaises). Chaque pays-année est donc rattaché à une version NUTS (2024, 2021, 2016, 2013, 2010, 2006, 2003), d'après les listes officielles GISCO (`gisco-services.ec.europa.eu/distribution/v2/nuts/csv/NUTS_AT_<v>.csv`).
  - On retient la version la plus récente entièrement couverte, sinon la mieux couverte, avec au moins 90 % de ses régions.
  - Seules les régions de cette version entrent dans le calcul. Les régions extra-regio (ZZ) sont exclues.
  - La `note` indique la version, n/K régions et les régions manquantes.
- **Formules** :
  - `sante_inegalite_densite` : CV **non pondéré** = écart-type (dénominateur n) / moyenne simple des densités régionales.
  - `sante_inegalite_densite_pond` : CV **pondéré par la population**, avec moyenne et variance pondérées par la population au 1er janvier.
  - Poids : `demo_r_pjanaggr3` si toutes les régions y figurent avec ce code. Sinon, pour les anciens codes NUTS, population implicite = NR × 100 000 / densité, tirée du même jeu Eurostat. La `note` précise le poids utilisé.
- **Couverture** : 20 pays, 1993-2025.
  - Exclus faute de plusieurs régions NUTS 2 : CY, EE, LU, LV, MT.
  - Absents de ces jeux régionaux : DE, IE.
- **Ruptures à connaître** (visibles dans la `note`) :
  - Changement de version NUTS : FR 2013, avec l'ajout de Mayotte, le CV non pondéré passe de 0,15 à 0,20. HR 2021 : 2 puis 4 régions. PL 2021 : 16 puis 17.
  - Changement de série (prsrg puis physreg) : DK 2021, CV de 0,11 à 0,28.
  - Définitions nationales différentes (médecins en exercice, professionnellement actifs ou habilités), drapeau « définition différente » pour EL par exemple.
  - Le CV non pondéré est sensible aux petites régions, comme les régions ultrapériphériques.
- **Contrôle France 2024 (NUTS 2024, 27 régions)** : CV non pondéré 0,191, pondéré 0,122. La dispersion est tirée par l'Île-de-France (forte densité) et Mayotte (très faible densité).

## Reproductibilité et sécurité

- Les téléchargements utilisent `urllib` : User-Agent explicite (l'OCDE refuse celui par défaut), proxy du système, vérification TLS toujours active, jusqu'à 4 essais en cas d'erreur 429/5xx ou de coupure.
- Les fichiers bruts sont lus uniquement comme CSV ou JSON. Aucun code n'est exécuté depuis `sante_raw/`.
- Les sources changent dans le temps : l'OCDE révise ses séries et l'OMS régénère ses exports. Relancer le script peut modifier quelques valeurs.
