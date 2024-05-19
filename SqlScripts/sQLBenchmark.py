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
    return time.time()-start_time



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
    return time.time()-start_time


def updateValues(cursor, iterations):
    query = f"""
    UPDATE  elections set Nom = 'helicopter' LIMIT {iterations}
    """
    start_time = time.time()
    cursor.execute(query)
    return time.time() - start_time

def select(cursor, iterations):
    query = f"""
    SELECT `Code du département`
    FROM elections
    LIMIT {iterations}
    """
    start_time = time.time()
    cursor.execute(query)
    return time.time() - start_time






def fileBenchmark(fileName,iterations):
    # Créer un curseur pour exécuter les requêtes SQL
    cursor = conn.cursor()

    # Charger les données du fichier Excel
    excel_file = fileName
    df = pd.read_excel(excel_file)

    # Convertir les types de données à des types Python standard
    df = df.astype(str)

    # Initialiser les listes pour stocker les temps pris pour chaque opération
    addOnebyOne_times = []
    addAll_times = []
    update_times = []
    select_times = []

    # Benchmark pour les opérations d'ajout un par un
    duration = 0
    for i in range(len(df)):
        row = df.iloc[i]  # Get row data
        duration = duration + insertValue(cursor, row)

    # Valider les changements
    conn.commit()
    addOnebyOne_times.append(duration)


     # Benchmark pour les opérations d'ajout
    addAll_times.append(insertValues(cursor,df))
    conn.commit()


    # Benchmark pour les opérations de mise à jour
    update_times.append(updateValues(cursor,iterations))
    conn.commit()



    # Benchmark pour les opérations de mise à jour
    select_times.append(select(cursor,iterations))
    conn.commit()

    # Fermer le curseur
    cursor.close()

    return addOnebyOne_times, addAll_times, update_times, select_times


if __name__ == '__main__':
    file_sizes = [1000]
    add_one_by_one_times_list = []
    add_times_list = []
    update_times_list = []
    select_times_list = []

    for size in file_sizes:
        fileName = f'../MOCK_DATA_{size}.xlsx'
        add_one_by_one_times, add_times , update_times, select_times = fileBenchmark(fileName,size)
        add_times_list.append(sum(add_one_by_one_times))
        add_one_by_one_times_list.append(sum(add_one_by_one_times))
        update_times_list.append(sum(update_times))
        select_times_list.append(sum(select_times))

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
    plt.savefig('operations_temps.png')
    plt.show()
