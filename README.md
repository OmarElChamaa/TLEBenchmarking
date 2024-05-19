# TLEBenchmarking

DB used :
 https://www.data.gouv.fr/fr/datasets/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-2nd-tour/
Download Format : Xlsx

Benchmarking Data : https://docs.google.com/spreadsheets/d/1jEePfGDo952euuNExDNVvgm3AfDgxZLdvHcJ7oRnYdc/edit#gid=0

Create docker and db
```
 docker pull mysql:latest
docker run --name elections-mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=elections_benchmark -p 10101:3306 -d mysql:latest
```

Create couch and db
```
  docker pull couchdb:latest
docker run -d --name elections-couchdb -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=password -p 5984:5984 couchdb:latest


```



Pour ajouter et preparer une base de donnees :
```
    python **add**.py
```


Pour lancer un benchmark :
```
    python **Benchmark**.py <nombre_iterations>
```

