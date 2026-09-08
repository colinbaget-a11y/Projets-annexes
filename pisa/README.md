# Accès aux bases PISA (2000 → 2025) et chiffrage PISA / PIB

Vérifié le 8 septembre 2026 depuis un environnement cloud (proxy HTTPS, sans navigateur).

## 1. Ce qui est accessible

L'OCDE publie un index unique de tous les fichiers : `https://webfs.oecd.org/pisa2022/index.html`
(PISA 2000 → PISA 2025 + PISA for Development). Résultat des tests fichier par fichier dans
`manifest_acces_pisa.csv` (162 fichiers ; colonne `status`) :

| Cycle | Format publié | Accès direct | Solution de repli |
|---|---|---|---|
| 2015, 2018, 2022, 2025 | SPSS/SAS zippés sur `webfs.oecd.org` | oui (≈ 10 Go au total, ~250 ko/s) | – |
| 2000, 2003, 2006, 2009 (+ERA), 2012 | données TXT zippées + syntaxes SPSS/SAS sur `www.oecd.org/content/dam/...` | **non pour les .zip** (challenge JavaScript Cloudflare) ; oui pour les syntaxes SPSS (.txt) | copie intégrale des .zip sur l'Internet Archive (`web.archive.org`, snapshots 2021-2024), testée fichier par fichier |
| PISA for Development | zips sur `www.oecd.org` | non (Cloudflare), sauf 6 fichiers | aucune trouvée |

Seuls les fichiers de syntaxe SAS (.sas) de 2000-2012 restent inaccessibles ; ils sont redondants
avec les syntaxes SPSS, disponibles.

PISA 2025 : les résultats ont été publiés le 8 septembre 2026 et les fichiers élèves/écoles/enseignants
(`CY09_MS_*_PUF.zip`, 1,6 Go) sont déjà en ligne.

Vérifications faites : téléchargement complet + `unzip` d'un fichier de chaque source (PISA 2022 écoles
depuis webfs, PISA 2000 et 2003 écoles depuis l'Internet Archive), lecture du .SAV avec `pyreadstat`
(21 629 écoles, 80 pays ; 282 écoles en France), concordance du TXT 2000 avec la syntaxe SPSS.

Pièges : `www.oecd.org` bloque tout client non-navigateur (HTML, .zip, .xlsx) ; les PDF et .txt passent.
Un navigateur ne résout pas le problème ici (Chromium ne traverse pas le proxy de la session).

## 2. Utilisation

```bash
./telecharger_pisa.sh "PISA 2022" SPSS     # fichiers SPSS de PISA 2022 dans ./data/PISA_2022
./telecharger_pisa.sh "PISA 2003"          # données TXT (via Internet Archive) + syntaxes SPSS
python3 chiffrage_pisa_pib.py              # les deux chiffrages, paramètres explicites en tête de script
```

Le chiffrage et ses sources sont commentés dans `note_chiffrage.md` ; la revue de littérature (25 textes lus,
paramètres, identification, textes inaccessibles) est dans `note_litterature.md` ; `simulation_ocde2010.py` réplique
la projection OCDE 2010 pour la France et l'inverse pour une baisse. `graphiques.html` est une page autonome
(ouvrir dans un navigateur) avec les cinq graphiques : série France, années de scolarité, PIB par l'effet de
niveau, comparaison des deux cadres, accès aux fichiers ; chaque graphique a sa table de données.
