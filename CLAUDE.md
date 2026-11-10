@AGENTS.md

## Session Chat (bundle hors-ligne)

Le bundle hermétique de cette branche est décrit par `sandbox/BUNDLE.json` (pointeur lisible par script : commit amont, runtimes, empreintes des lockfiles, archive et parties). Vérifier : `make verify-bundle` ; avec l'archive ou ses parties : `make verify-bundle ARGS="--livrable <dossier>"`. `make lint` échoue volontairement si `pnpm-lock.yaml` change sans mise à jour du pointeur. L'archive est sur la branche orpheline `bundle-hermetique-v0.25.1` du fork.
