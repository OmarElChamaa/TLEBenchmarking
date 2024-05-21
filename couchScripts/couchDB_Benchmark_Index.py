import time
import pandas as pd
import couchdb
import matplotlib.pyplot as plt

# Connect to CouchDB
db_name = 'elections_benchmark'
username = 'admin'
password = 'password'
couch = couchdb.Server('http://localhost:5984/')
couch.resource.credentials = (username, password)
nb_operations = 0

if db_name in couch:
    db = couch[db_name]
else:
    db = couch.create(db_name)

# Define a design document with a view to index the 'Code du département' field
design_doc_id = '_design/elections'
design_doc = {
    "_id": design_doc_id,
    "views": {
        "by_code": {
            "map": "function(doc) { if (doc['Code du département']) { emit(doc['Code du département'], doc); } }"
        }
    }
}

# Check if the design document already exists
if design_doc_id in db:
    # Delete the existing design document
    del db[design_doc_id]

# Save the design document to create the index
db.save(design_doc)


# Define functions for operations

def insertValues(db, df):
    start_time = time.time()
    docs = df.to_dict(orient='records')
    db.update(docs)
    end_time = time.time()
    return end_time - start_time


def updateValues(db, df):
    # Benchmark pour les opérations de mise à jour
    start_time = time.time()
    for _, row in df.iterrows():
        code_du_departement = row.get('Code du département')
        if code_du_departement:
            for doc_id in db:
                doc = db.get(doc_id)
                if 'Code du département' in doc and doc['Code du département'] == code_du_departement:
                    doc['Code du département'] = code_du_departement
                    db.save(doc)
    end_time = time.time()
    return end_time - start_time



def select(db):
    # Benchmark pour les opérations de sélection
    start_time = time.time()
    query_result = db.find({"selector": {"Nom": "Macron"}})
    for doc in query_result:
        pass  # Just fetching the document
    end_time = time.time()
    return end_time - start_time


def fileBenchmark(fileName):
    # Load data from the Excel file
    df = pd.read_excel(fileName)

    # Benchmark for insertion operations
    ajout_times = insertValues(db, df)

    # Benchmark for update operations
    update_times = updateValues(db, df)


    select_times = select(db)

    return ajout_times, update_times, select_times


if __name__ == '__main__':
    file_sizes = [1000]  # Number of elements in the file
    add_times_list = []
    update_times_list = []
    select_times_list = []

    for size in file_sizes:
        fileName = f'../mockData/MOCK_DATA_{size}d.xlsx'
        add_times, update_times, select_times = fileBenchmark(fileName)
        add_times_list.append(add_times)
        update_times_list.append(update_times)
        select_times_list.append(select_times)

    print("Number of operations:", nb_operations)

    # Display time for each file size
    df_times = pd.DataFrame({
        'File Size': file_sizes,
        'Insertion Time': add_times_list,
        'Update Time': update_times_list,
        'Query Time': select_times_list
    })

    print("\nTime taken for each file size:")
    print(df_times)

    # Plotting the graph
    plt.plot(file_sizes, add_times_list, label='Insertion', marker='o')
    plt.scatter(file_sizes, add_times_list, marker='o')

    plt.plot(file_sizes, update_times_list, label='Update', marker='o')
    plt.scatter(file_sizes, update_times_list, marker='o')

    plt.plot(file_sizes, select_times_list, label='Query', marker='o')
    plt.scatter(file_sizes, select_times_list, marker='o')

    plt.xlabel('Number of Elements')
    plt.ylabel('Time (seconds)')
    plt.title('Time taken for operations based on number of elements')
    plt.legend()
    plt.grid(True)

    # Save the graph
    plt.savefig('BenchmarkCouchDB_Indexed.png')
    plt.show()
