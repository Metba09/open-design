# Fichiers découpés

Les fichiers de plus de 90 Mo sont découpés en parties (limite GitHub : 100 Mo par fichier).
Reconstitution :

```bash
cat codegraph.db.gz.part* > codegraph.db.gz
```
