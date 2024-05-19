# TLEBenchmarking

DB used : https://data.enseignementsup-recherche.gouv.fr/explore/dataset/fr-esr-referent-e-s-crous-etudiants-refugies-dans-les-universites/export/
https://www.data.gouv.fr/fr/datasets/parrainages-des-candidats-a-lelection-presidentielle-francaise-de-2022/#/resources
Download Format : Json

Benchmarking Data : https://docs.google.com/spreadsheets/d/1jEePfGDo952euuNExDNVvgm3AfDgxZLdvHcJ7oRnYdc/edit#gid=0

Create docker and db
```
 docker pull mysql:latest
docker run --name elections-mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=elections_benchmark -p 10101:3306 -d mysql:latest
```


Pour ajouter et preparer une base de donnees :
```
    python **add**.py
```


Pour lancer un benchmark :
```
    python **Benchmark**.py <nombre_iterations>
```

