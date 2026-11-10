#!/usr/bin/env python3
"""Vérifie le pointeur sandbox/BUNDLE.json (stdlib seule, aucun accès réseau).

  verify_bundle.py                      lockfiles et versions de runtime du dépôt vs pointeur
  verify_bundle.py --livrable DIR       idem, puis l'archive du bundle trouvée dans DIR :
                                        SHA-256 vérifié AVANT toute ouverture, puis lockfiles
                                        contenus dans l'archive comparés au pointeur
  verify_bundle.py --pointer FICHIER    autre pointeur (tests)

DIR contient soit l'archive complète, soit ses parties (*.partNN, branche orpheline du fork).
Chaque écart est signalé « ÉCART : … » ; code de sortie 1 s'il y en a, 0 sinon.
Une archive altérée ne produit jamais de traceback.
"""
import argparse
import hashlib
import json
import sys
import tarfile
import tempfile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAX_MEMBER = 32 * 1024 * 1024  # un lockfile ne dépasse jamais 32 Mo : garde-fou anti-bombe
ecarts = []


def say(msg, err=False):
    (sys.stderr if err else sys.stdout).write(msg + "\n")


def ecart(msg):
    ecarts.append(msg)
    say("ÉCART : " + msg, err=True)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_pointer(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        ecart(f"pointeur illisible ({path}) : {e}")
        return None
    if data.get("schema") != 1:
        ecart(f"schéma de pointeur inattendu : {data.get('schema')!r} (attendu 1)")
        return None
    return data


def check_repo(p):
    """Lockfiles du dépôt et versions de runtime vs pointeur."""
    for name, attendu in p["lockfiles_sha256"].items():
        f = ROOT / name
        if not f.is_file():
            ecart(f"lockfile absent du dépôt : {name}")
        elif sha256_file(f) != attendu:
            ecart(f"{name} différent du pointeur (régénéré ? mettre à jour BUNDLE.json et le livrable)")
        else:
            say(f"OK : {name} = pointeur")
    node = p["runtimes"]["node"]
    try:
        nv = (ROOT / ".node-version").read_text().strip().lstrip("v")
    except OSError as e:
        ecart(f".node-version illisible : {e}")
        nv = None
    if nv is not None:
        if nv.split(".")[0] != node.split(".")[0]:
            ecart(f".node-version ({nv}) et Node du bundle ({node}) : versions majeures différentes")
        else:
            say(f"OK : Node {node} compatible avec .node-version ({nv})")
    try:
        pm = json.loads((ROOT / "package.json").read_text(encoding="utf-8")).get("packageManager")
    except (OSError, ValueError) as e:
        ecart(f"package.json illisible : {e}")
        return
    if pm != "pnpm@" + p["runtimes"]["pnpm"]:
        ecart(f"packageManager ({pm}) différent de pnpm@{p['runtimes']['pnpm']}")
    else:
        say(f"OK : packageManager = {pm}")


def assemble_parties(d, b, tmp):
    """Vérifie chaque partie, les concatène dans tmp en recalculant le hash. Renvoie le chemin ou None."""
    parts = b.get("parts", [])
    for part in parts:
        f = d / part["name"]
        if not f.is_file():
            ecart(f"partie absente : {part['name']}")
            return None
        if sha256_file(f) != part["sha256"]:
            ecart(f"partie altérée : {part['name']} (SHA-256 différent du pointeur) ; archive non ouverte")
            return None
    out = Path(tmp) / b["tarball"]
    h = hashlib.sha256()
    with open(out, "wb") as o:
        for part in parts:
            with open(d / part["name"], "rb") as f:
                for chunk in iter(lambda: f.read(1 << 20), b""):
                    h.update(chunk)
                    o.write(chunk)
    if h.hexdigest() != b["tarball_sha256"]:
        ecart("archive reconstituée : SHA-256 différent du pointeur ; archive non ouverte")
        return None
    say(f"OK : {len(parts)} parties vérifiées, archive reconstituée = pointeur")
    return out


def check_livrable(p, dossier):
    b = p["bundle"]
    d = Path(dossier)
    if not d.is_dir():
        ecart(f"dossier livrable introuvable : {dossier}")
        return
    with tempfile.TemporaryDirectory() as tmp:
        tarball = d / b["tarball"]
        if tarball.is_file():
            if sha256_file(tarball) != b["tarball_sha256"]:
                ecart(f"{b['tarball']} : SHA-256 différent du pointeur ; archive non ouverte")
                return
            say(f"OK : SHA-256 de {b['tarball']} = pointeur")
        else:
            tarball = assemble_parties(d, b, tmp)
            if tarball is None:
                if not any(("partie" in e or "archive" in e) for e in ecarts):
                    ecart(f"ni {b['tarball']} ni ses parties dans {dossier}")
                return
        comparer_lockfiles_archive(p, tarball)


def comparer_lockfiles_archive(p, tarball):
    b = p["bundle"]
    wanted = {f"{b['tar_root']}/app/{n}": n for n in p["lockfiles_sha256"]}
    trouves = {}
    try:
        with tarfile.open(tarball, "r:gz") as tf:
            for m in tf:
                n = wanted.get(m.name)
                if n is None or not m.isfile():
                    continue
                if m.size > MAX_MEMBER:
                    ecart(f"{m.name} : taille anormale ({m.size} octets)")
                    return
                trouves[n] = hashlib.sha256(tf.extractfile(m).read()).hexdigest()
                if len(trouves) == len(wanted):
                    break
    except (tarfile.TarError, KeyError, OSError, EOFError, zlib.error) as e:
        ecart(f"archive illisible ({type(e).__name__}) : {e}")
        return
    for n, attendu in p["lockfiles_sha256"].items():
        if n not in trouves:
            ecart(f"{n} absent de l'archive")
        elif trouves[n] != attendu:
            ecart(f"{n} de l'archive différent du pointeur")
        else:
            say(f"OK : {n} de l'archive = pointeur")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--pointer", default=str(ROOT / "sandbox" / "BUNDLE.json"))
    ap.add_argument("--livrable", metavar="DIR")
    a = ap.parse_args(argv)
    p = load_pointer(a.pointer)
    if p is not None:
        try:
            check_repo(p)
            if a.livrable:
                check_livrable(p, a.livrable)
        except KeyError as e:
            ecart(f"champ manquant dans le pointeur : {e}")
    if ecarts:
        say(f"ÉCHEC : {len(ecarts)} écart(s)", err=True)
        return 1
    say("verify_bundle : OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
