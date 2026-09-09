#!/usr/bin/env bash
# Sprawdza higienę repo przed commitem. Wyjście 0 = PASS.
set -u
cd "$(dirname "$0")/.."
fail=0

echo "== frontmatter każdego SKILL.md =="
for f in skills/*/SKILL.md; do
  [ -e "$f" ] || continue
  if ! head -1 "$f" | grep -q '^---$'; then echo "FAIL brak frontmattera: $f"; fail=1; continue; fi
  if ! grep -q '^name:' "$f"; then echo "FAIL brak name: $f"; fail=1; fi
  if ! grep -q '^description:' "$f"; then echo "FAIL brak description: $f"; fail=1; fi
  dir=$(basename "$(dirname "$f")")
  nm=$(grep '^name:' "$f" | head -1 | sed 's/^name:[[:space:]]*//' | tr -d '"'"'")
  if [ "$nm" != "$dir" ]; then echo "FAIL name ($nm) != folder ($dir): $f"; fail=1; fi
  echo "ok $f"
done

echo "== pauzy i półpauzy w plikach repo =="
if grep -rn --include='*.md' --include='*.sh' -e '—' -e '–' . --exclude-dir=.git --exclude-dir=node_modules | grep -v 'tests/' | grep -v 'references/' ; then
  echo "FAIL znaleziono pauzę/półpauzę (poza tests/ i references/, gdzie są przykładami)"; fail=1
else
  echo "ok brak pauz"
fi

echo "== sekrety =="
if grep -rnE --include='*' -e 'sk-[A-Za-z0-9]{20,}' -e 'ghp_[A-Za-z0-9]{20,}' -e 'apify_api_[A-Za-z0-9]+' -e 'AKIA[0-9A-Z]{16}' . --exclude-dir=.git --exclude-dir=node_modules; then
  echo "FAIL wygląda na token"; fail=1
else
  echo "ok brak tokenów"
fi

echo "== pliki prywatne =="
if find . -path ./.git -prune -o \( -name 'groups.json' -o -name 'brand-context*' -o -name '*.csv' \) -print | grep -q .; then
  find . -path ./.git -prune -o \( -name 'groups.json' -o -name 'brand-context*' -o -name '*.csv' \) -print
  echo "FAIL plik prywatny w drzewie"; fail=1
else
  echo "ok brak plików prywatnych"
fi

[ $fail -eq 0 ] && echo "PASS" || echo "FAIL"
exit $fail
