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


def fileBEnchmark(fileName):
    # Créer un curseur pour exécuter les requêtes SQL
    cursor = conn.cursor()

    # Charger les données du fichier Excel
    excel_file = fileName
    df = pd.read_excel(excel_file)

    # Convertir les types de données à des types Python standard
    df = df.astype(str)

    # Initialiser les listes pour stocker les temps pris pour chaque opération
    ajout_times = []
    update_times = []
    select_times = []

    # Benchmark pour les opérations d'ajout
    start_time = time.time()
    for i in range(len(df)):
        row = df.iloc[i]  # Get row data
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

    # Valider les changements
    conn.commit()
    end_time = time.time()
    ajout_times.append(end_time - start_time)

    # Benchmark pour les opérations de mise à jour
    start_time = time.time()
    for i in range(len(df)):
        row = df.iloc[i]  # Get row data
        cursor.execute("""
        UPDATE elections SET Voix = %s WHERE `Code du département` = %s
        """, (
            row['Voix'], row['Code du département']
        ))

    # Valider les changements
    conn.commit()
    end_time = time.time()
    update_times.append(end_time - start_time)

    # Benchmark pour les opérations de requête
    start_time = time.time()
    for i in range(len(df)):
        cursor.execute("""
        SELECT * FROM elections WHERE `Code du département` = %s
        """, (
            df.iloc[i]['Code du département'],
        ))
        result = cursor.fetchall()  # Récupérer tous les résultats pour vider le curseur

    end_time = time.time()
    select_times.append(end_time - start_time)

    # Fermer le curseur
    cursor.close()

    return ajout_times, update_times, select_times


if __name__ == '__main__':
    file_sizes = [1000, 5000, 10000, 20000]
    ajout_times_list = []
    update_times_list = []
    select_times_list = []

    for size in file_sizes:
        fileName = f'../MOCK_DATA_{size}.xlsx'
        ajout_times, update_times, select_times = fileBEnchmark(fileName)
        ajout_times_list.append(sum(ajout_times))
        update_times_list.append(sum(update_times))
        select_times_list.append(sum(select_times))

    # Plotting the graph
    plt.plot(file_sizes, ajout_times_list, label='Ajout')
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
