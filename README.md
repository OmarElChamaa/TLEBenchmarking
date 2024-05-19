# TLEBenchmarking

DB used : https://data.enseignementsup-recherche.gouv.fr/explore/dataset/fr-esr-referent-e-s-crous-etudiants-refugies-dans-les-universites/export/

Download Format : Json

Benchmarking Data : https://docs.google.com/spreadsheets/d/1jEePfGDo952euuNExDNVvgm3AfDgxZLdvHcJ7oRnYdc/edit#gid=0


Pour ajouter et preparer une base de donnees :
```
    python **add**.py <nom fichier .json>
```


Pour lancer un benchmark :
```
    python **Benchmark**.py <nombre_iterations>
```