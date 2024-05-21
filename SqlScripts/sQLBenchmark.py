import time
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

# Connexion à MySQL avec le mot de passe
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="elections_benchmark",
    port=10101
)


def insertValue(cursor, row):
    start_time = time.time()
    cursor.execute("""
    INSERT INTO elections (`Code du département`, `Libellé du département`, `Code de la commune`, `Libellé de la commune`, `Etat saisie`, `Inscrits`, `Abstentions`, `% Abs/Ins`, `Votants`, `% Vot/Ins`, `Blancs`, `% Blancs/Ins`, `% Blancs/Vot`, `Nuls`, `% Nuls/Ins`, `% Nuls/Vot`, `Exprimés`, `% Exp/Ins`, `% Exp/Vot`, `N°Panneau`, `Sexe`, `Nom`, `Prénom`, `Voix`, `% Voix/Ins`, `% Voix/Exp`)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row['Code du département'], row['Libellé du département'], row['Code de la commune'],
        row['Libellé de la commune'], row['Etat saisie'], row['Inscrits'], row['Abstentions'], row['% Abs/Ins'],
        row['Votants'], row['% Vot/Ins'], row['Blancs'], row['% Blancs/Ins'], row['% Blancs/Vot'], row['Nuls'],
        row['% Nuls/Ins'], row['% Nuls/Vot'], row['Exprimés'], row['% Exp/Ins'], row['% Exp/Vot'], row['N°Panneau'],
        row['Sexe'], row['Nom'], row['Prénom'], row['Voix'], row['% Voix/Ins'], row['% Voix/Exp']
    ))
    return time.time() - start_time


def insertValues(cursor, df):
    values = []
    for index, row in df.iterrows():
        values.append((
            row['Code du département'], row['Libellé du département'], row['Code de la commune'],
            row['Libellé de la commune'], row['Etat saisie'], row['Inscrits'], row['Abstentions'], row['% Abs/Ins'],
            row['Votants'], row['% Vot/Ins'], row['Blancs'], row['% Blancs/Ins'], row['% Blancs/Vot'], row['Nuls'],
            row['% Nuls/Ins'], row['% Nuls/Vot'], row['Exprimés'], row['% Exp/Ins'], row['% Exp/Vot'], row['N°Panneau'],
            row['Sexe'], row['Nom'], row['Prénom'], row['Voix'], row['% Voix/Ins'], row['% Voix/Exp']
        ))

    insert_query = """
    INSERT INTO elections (`Code du département`, `Libellé du département`, `Code de la commune`, `Libellé de la commune`, `Etat saisie`, `Inscrits`, `Abstentions`, `% Abs/Ins`, `Votants`, `% Vot/Ins`, `Blancs`, `% Blancs/Ins`, `% Blancs/Vot`, `Nuls`, `% Nuls/Ins`, `% Nuls/Vot`, `Exprimés`, `% Exp/Ins`, `% Exp/Vot`, `N°Panneau`, `Sexe`, `Nom`, `Prénom`, `Voix`, `% Voix/Ins`, `% Voix/Exp`)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    start_time = time.time()

    cursor.executemany(insert_query, values)
    return time.time() - start_time


def updateValues(cursor, iterations):
    query = f"""
    UPDATE  elections set Nom = 'helicopter' LIMIT {iterations}
    """
    start_time = time.time()
    cursor.execute(query)
    return time.time() - start_time


def select(cursor):
    query = f"""
    SELECT `Code du département`
    FROM elections
    WHERE Nom = 'Macron'
    """
    start_time = time.time()
    cursor.execute(query)
    return time.time() - start_time


def fileBenchmark(fileName, iterations):
    # Créer un curseur pour exécuter les requêtes SQL
    cursor = conn.cursor()

    # Charger les données du fichier Excel
    excel_file = fileName
    df = pd.read_excel(excel_file)

    # Convertir les types de données à des types Python standard
    df = df.astype(str)

    # Initialiser les listes pour stocker les temps pris pour chaque opération
    addOnebyOne_time = 0

    # Benchmark pour les opérations d'ajout un par un
    for i in range(len(df)):
        row = df.iloc[i]  # Get row data
        start_time = time.time()
        insertValue(cursor, row)
        addOnebyOne_time = addOnebyOne_time + time.time() - start_time
        # Valider les changements après chaque insertion
        conn.commit()

    # Benchmark pour les opérations d'ajout collectif
    addAll_times = insertValues(cursor, df)

    # Read and process the result set from the insert operation
    for result in cursor:
        pass

    # Benchmark pour les opérations de mise à jour
    update_times = updateValues(cursor, iterations)

    # Read and process the result set from the update operation
    for result in cursor:
        pass

    # Benchmark pour les opérations de mise à jour
    select_times = select(cursor)

    # Read and process the result set from the select operation
    for result in cursor:
        pass

    # Valider les changements
    conn.commit()

    # Fermer
    cursor.close()

    return addOnebyOne_time, addAll_times, update_times, select_times


if __name__ == '__main__':
    file_sizes = [1000, 2000, 4000, 5000, 10000, 20000, 40000, 80000]
    add_one_by_one_times_list = []
    add_times_list = []
    update_times_list = []
    select_times_list = []

    for size in file_sizes:
        fileName = f'../mockData/MOCK_DATA_{size}.xlsx'
        add_one_by_one_times, add_times, update_times, select_times = fileBenchmark(fileName, size)
        add_times_list.append(add_times)
        add_one_by_one_times_list.append(add_one_by_one_times)  # Summing up individual times for each iteration
        update_times_list.append(update_times)
        select_times_list.append(select_times)

    # Configuration de l'affichage pour voir toutes les colonnes
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    df_times = pd.DataFrame({
        'Taille du fichier': file_sizes,
        'Temps Ajout un par un': add_one_by_one_times_list,
        'Temps Ajout collectif': add_times_list,
        'Temps Mise à jour': update_times_list,
        'Temps Sélection': select_times_list
    })

    print("\nTemps pour chaque taille de fichier:")
    print(df_times)

    # Plotting the graph
    plt.plot(file_sizes, add_one_by_one_times_list, label='Ajout un par un', marker='o')
    plt.scatter(file_sizes, add_one_by_one_times_list, marker='o')

    plt.plot(file_sizes, add_times_list, label='Ajout collectif', marker='o')
    plt.scatter(file_sizes, add_times_list, marker='o')

    plt.plot(file_sizes, update_times_list, label='Mise à jour', marker='o')
    plt.scatter(file_sizes, update_times_list, marker='o')

    plt.plot(file_sizes, select_times_list, label='Sélection', marker='o')
    plt.scatter(file_sizes, select_times_list, marker='o')

    plt.xlabel('Nombre d\'éléments')
    plt.ylabel('Temps (secondes)')
    plt.title('Temps pris pour les opérations en fonction du nombre d\'éléments')
    plt.legend()
    plt.grid(True)

    # Enregistrer le graphique
    plt.savefig('BenchmarkSQL.png')
    plt.show()


