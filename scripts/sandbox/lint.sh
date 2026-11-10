#!/usr/bin/env bash
# Contrôles du pointeur de bundle : syntaxe JSON, syntaxe Python, puis vérification des lockfiles.
# Échoue volontairement si pnpm-lock.yaml (ou les autres lockfiles listés) change sans mise à jour de sandbox/BUNDLE.json.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/../.."
python3 -m json.tool sandbox/BUNDLE.json >/dev/null || { echo "ÉCART : sandbox/BUNDLE.json n'est pas un JSON valide" >&2; exit 1; }
python3 -c "import ast,sys; ast.parse(open('scripts/sandbox/verify_bundle.py', encoding='utf-8').read())"
python3 scripts/sandbox/verify_bundle.py
echo "lint OK"
