### TLEBenchmarking

#### Utilisation de la base de données :

- **Base de données utilisée** : MySQL et CouchDB
- **Données** : [Résultats de l'élection présidentielle du 10 et 24 avril 2022](https://www.data.gouv.fr/fr/datasets/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-2nd-tour/) au format Xlsx.

#### Configuration Docker et bases de données :

1. **MySQL** :
   ```
   docker pull mysql:latest
   docker run --name elections-mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=elections_benchmark -p 10101:3306 -d mysql:latest
   ```

2. **CouchDB** :
   ```
   docker pull couchdb:latest
   docker run -d --name elections-couchdb -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=password -p 11210:5984 couchdb:latest
   ```

#### Préparation de la base de données :

1. Exécuter le script **add.py** pour ajouter et préparer la base de données.

#### Lancer un benchmark :

2. Exécuter le script **xBenchmark.py** et attendez.
   ```
   python xBenchmark.py
   ```

---

*Assurez-vous d'avoir installé Docker sur votre système pour exécuter les conteneurs. Les scripts **add.py** et **Benchmark.py** nécessitent Python installé sur votre machine.*
