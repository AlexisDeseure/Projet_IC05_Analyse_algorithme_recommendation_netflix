import csv
import pandas as pd
import os

def trier(csv_file_path):
    new_csv_file_path = 'temporaire.csv'
    columns_to_keep = ['ID', 'recommendations']
    with open(csv_file_path, 'r', encoding='utf-8') as input_file:
        reader = csv.DictReader(input_file, delimiter=';')
        fieldnames = reader.fieldnames
        rows_extended = []
        max_recommendations = 0
        for row in reader:
            new_row = {column: row[column] for column in columns_to_keep}
            recommendations = row["recommendations"].split(",")
            max_recommendations = max(max_recommendations, len(recommendations))
            for i, recommendation in enumerate(recommendations, start=1):
                column_name = f"recommendation{i}"
                new_row[column_name] = recommendation
            rows_extended.append(new_row)
    extended_fieldnames = columns_to_keep + [f"recommendation{i}" for i in range(1, max_recommendations + 1)]
    with open(new_csv_file_path, 'w', newline='', encoding='utf-8') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=extended_fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(rows_extended)
    
    print("Les colonnes ont été supprimées et les recommandations ont été triées avec succès.")
    # print("Le fichier de sortie est prêt :", new_csv_file_path)
    # print("Les colonnes du fichier de sortie :", extended_fieldnames)


def modifier_csv(new_csv_file_path):
    df = pd.read_csv(new_csv_file_path, delimiter=';')
    new_rows = []
    for _, row in df.iterrows():
        recommendations = str(row['recommendations']).split(',')  
        for recommendation in recommendations:
            new_row = {
                'Source': row['ID'],  # Modification de la colonne 'ID' en 'source'
                'Target': recommendation.strip()  # Modification de la colonne 'recommendations' en 'target'
            }
            new_rows.append(new_row)
            
    new_df = pd.DataFrame(new_rows)
    new_csv_file_path1 = 'fichier_liens.csv'
    new_df.to_csv(new_csv_file_path1, index=False, sep=';')
    print("Le fichier a été modifié avec succès. Le fichier de sortie est prêt :", new_csv_file_path1)


def menu(csv_file_path=None):
    if csv_file_path is None:
        csv_file_path = input("Entrez le chemin du fichier csv à traiter (partiel ou absolu): ")
    if not(os.path.exists(csv_file_path)):
        print("Le fichier n'existe pas. Veuillez réessayer.")
        menu()
        return
    print("Que souhaitez-vous faire ?")
    print("1. Fichier de liens")
    print("2. Fichier de noeuds")
    choix = input("Votre choix (1, 2) : ")

    if choix == "1":
        trier(csv_file_path)
        modifier_csv('temporaire.csv')
        os.remove('temporaire.csv')
        menu(csv_file_path)
        
    elif choix == "2":
        df = pd.read_csv(csv_file_path, delimiter=';')       
        df = df.rename(columns={'titres': 'Label'})
        df = df.rename(columns={'ID': 'Id'})
        df = df.rename(columns={'genres': 'Genres'})
        df = df.rename(columns={'netflix_original': 'Netflix_original'})
        df = df.rename(columns={'nombre_occurrence': 'Nombre_occurrence'})
        columns_to_keep = ['Id', 'Label', 'Genres', 'Netflix_original', 'Nombre_occurrence']
        df = df[columns_to_keep]
        new_csv_file_path = 'fichier_noeuds.csv'
        df.to_csv(new_csv_file_path, index=False, sep=';')
        print("Le fichier a été modifié avec succès. Le fichier de sortie est prêt :", new_csv_file_path)
        print("Les colonnes du fichier de sortie :", columns_to_keep)
    else:
        print("Choix invalide. Veuillez sélectionner 1 ou 2.")
        menu(csv_file_path)

if __name__ == "__main__":
    menu()
