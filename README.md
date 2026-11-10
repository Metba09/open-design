# Bundle hermétique open-design v0.25.1

Branche orpheline : aucun lien avec l'historique du code. Elle contient uniquement l'archive du bundle, découpée en parties
de 90 Mo (limite de 100 Mo par fichier de GitHub).

Source : commit 07a86b1041531bfa0bec1006d9c0993985fee560 de ce dépôt. Construit le 2026-11-09 (Node 24.22.1, linux/x86_64).

Reconstituer et vérifier :

    cat open-design-bundle-v0.25.1.tar.gz.part* > open-design-bundle-v0.25.1.tar.gz
    sha256sum -c SHA256SUMS --ignore-missing
    tar -xzf open-design-bundle-v0.25.1.tar.gz && cd open-design-bundle && bash scripts/setup.sh && bash scripts/check.sh

Licences à examiner avant toute redistribution : voir LICENSES/NOTICE.md dans l'archive (ffmpeg GPLv3, gsap).
