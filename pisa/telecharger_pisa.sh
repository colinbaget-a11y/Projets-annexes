#!/usr/bin/env bash
# Télécharge les fichiers PISA listés dans manifest_acces_pisa.csv.
#   usage : ./telecharger_pisa.sh [cycle] [motif]
#   ex.   : ./telecharger_pisa.sh "PISA 2022" SPSS        -> fichiers SPSS de PISA 2022
#           ./telecharger_pisa.sh "PISA 2003"             -> tout PISA 2003 (données TXT via Wayback + syntaxes SPSS)
# Les fichiers 2015-2025 viennent directement de webfs.oecd.org ; les .zip 2000-2012 (bloqués par
# Cloudflare sur www.oecd.org) sont pris sur la copie de l'Internet Archive (colonne access_url).
set -euo pipefail
cycle="${1:-}"; motif="${2:-}"
dest="${PISA_DIR:-./data}"; mkdir -p "$dest"
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
python3 - "$cycle" "$motif" <<'PY' | while IFS=$'\t' read -r cyc url; do
import csv,sys,re
cyc,motif=sys.argv[1],sys.argv[2]
for r in csv.DictReader(open('manifest_acces_pisa.csv',encoding='utf-8')):
    if r['status']=='blocked' or not r['access_url']: continue
    if cyc and r['cycle']!=cyc: continue
    if motif and not re.search(motif, r['section']+' '+r['label']+' '+r['official_url'], re.I): continue
    print(r['cycle']+'\t'+r['access_url'])
PY
  sub="$dest/$(echo "$cyc" | tr ' ' '_')"; mkdir -p "$sub"
  f="$sub/$(basename "${url%%\?*}")"
  if [ -s "$f" ]; then echo "déjà présent : $f"; continue; fi
  echo "-> $url"
  curl -sS -L --retry 3 --retry-delay 5 -A "$UA" -o "$f" "$url" || { echo "ÉCHEC : $url" >&2; rm -f "$f"; }
done
