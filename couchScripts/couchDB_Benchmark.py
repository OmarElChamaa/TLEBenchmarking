import time
import pandas as pd
import couchdb
import matplotlib.pyplot as plt

# Connexion à CouchDB
username = 'admin'
password = 'password'
couch = couchdb.Server(f'http://{username}:{password}@localhost:5984/')
db_name = 'elections_benchmark'
if db_name in couch:
    db = couch[db_name]
else:
    db = couch.create(db_name)

def insertValue(row):
    start_time = time.time()
    db.save(row.to_dict())  # Convert Series to dictionary before saving
    return time.time() - start_time

def insertValues(df):
    values = df.to_dict(orient='records')
    start_time = time.time()
    for value in values:
        db.save(value)
    return time.time() - start_time

def updateValues(iterations):
    start_time = time.time()
    for _ in range(iterations):
        for doc in db.view('_all_docs'):
            doc['Nom'] = 'helicopter'
            db.save(doc)
            break  # Limiting the updates to 'iterations'
    return time.time() - start_time

def select():
    start_time = time.time()
    for _ in db.view('_all_docs'):
        pass
    return time.time() - start_time

def fileBenchmark(fileName, iterations):
    # Charger les données du fichier Excel
    df = pd.read_excel(fileName)

    # Initialiser les listes pour stocker les temps pris pour chaque opération
    addOnebyOne_time = 0

    # Benchmark pour les opérations d'ajout un par un
    for _, row in df.iterrows():
        addOnebyOne_time = addOnebyOne_time + (insertValue(row))

    # Benchmark pour les opérations d'ajout collectif
    addAll_time = insertValues(df)

    # Benchmark pour les opérations de mise à jour
    update_times = updateValues(iterations)

    # Benchmark pour les opérations de sélection
    select_times = select()

    return addOnebyOne_time, addAll_time, update_times, select_times

if __name__ == '__main__':
    file_sizes = [1000, 2000]
    add_one_by_one_times_list = []
    add_times_list = []
    update_times_list = []
    select_times_list = []

    for size in file_sizes:
        fileName = f'../MOCK_DATA_{size}.xlsx'
        add_one_by_one_times, add_times, update_times, select_times = fileBenchmark(fileName, size)
        add_times_list.append(add_one_by_one_times)
        add_one_by_one_times_list.append(add_one_by_one_times)  # Summing up individual times for each iteration
        update_times_list.append(update_times)
        select_times_list.append(select_times)

    # Plotting the graph
    plt.plot(file_sizes, add_one_by_one_times_list, label='Ajout un par un ')
    plt.plot(file_sizes, add_times_list, label='Ajout collectif')
    plt.plot(file_sizes, update_times_list, label='Mise à jour')
    plt.plot(file_sizes, select_times_list, label='Sélection')

    plt.xlabel('Nombre d\'éléments')
    plt.ylabel('Temps (secondes)')
    plt.title('Temps pris pour les opérations en fonction du nombre d\'éléments')
    plt.legend()
    plt.grid(True)
    # Enregistrer le graphique
    plt.savefig('couchDB.png')
    plt.show()
