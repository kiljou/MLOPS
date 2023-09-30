import pandas as pd
import os
import matplotlib.pyplot as plt
# Chemin du répertoire contenant les fichiers CSV
dossier_csv = 'C:/Users/284786/MLOPS/Donnees'

# Fonction pour lire et prétraiter les fichiers CSV
def lire_et_pretraiter_csv(chemin_dossier):
    list_df = []

    for fichier in os.listdir(chemin_dossier):
        if fichier.endswith('.csv'):
            chemin_fichier = os.path.join(chemin_dossier, fichier)
            df = pd.read_csv(chemin_fichier)
            df['Order_ID'] = df['Order Number'] if 'restaurant_1' in fichier else df['Order ID']
            df['Restaurant_ID'] = '1' if 'restaurant_1' in fichier else '2'
            list_df.append(df)

    concatenated_df = pd.concat(list_df, ignore_index=True)
    concatenated_df.drop(columns=['Order ID', 'Order Number'], inplace=True)

    return concatenated_df

# Fonction pour agréger les données par heure
#def aggreguer_par_heure(df):
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Heure'] = df['Order Date'].dt.hour
    df['Date'] = df['Order Date'].dt.date
    df['Chiffre Affaire'] = df['Product Price']*df['Quantity']

    resultat = df.groupby(['Restaurant_ID', 'Date', 'Heure'])['Chiffre Affaire'].sum().reset_index()
    resultat.rename(columns={'Chiffre Affaire': 'Chiffre Affaire'}, inplace=True)
    
    return resultat

def clean(df):
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Chiffre Affaire'] = df['Product Price']*df['Quantity']
    resultat = df.groupby(['Restaurant_ID','Order Date', 'Order_ID'])['Chiffre Affaire'].sum().reset_index()
    resultat.rename(columns=lambda x: x.lower().replace(' ', '_'), inplace=True)
    return resultat

# Fonction pour formater le chiffre d'affaires
def formater_chiffre_affaire(resultat):
    resultat['chiffre_affaire'] = resultat['chiffre_affaire'].apply(lambda valeur: f'{valeur:.2f}')
    return resultat
# Fonction pour créer le graphique en courbe
def creer_graphique(resultat):
    # Créer un graphique en courbe
    fig, ax = plt.subplots(1,1, figsize=(10,5))
    
    ax.plot(resultat['order_date'], resultat['chiffre_affaire'])
    ax.set_title('Chiffre d affaire des restaurants en fonction du temps')
    ax.set_xlabel('Temps')
    ax.set_ylabel('chiffre affaire')
    plt.grid(True)


# Appels aux fonctions
concatenated_df = lire_et_pretraiter_csv(dossier_csv)
#resultat = aggreguer_par_heure(concatenated_df)
resultat = clean(concatenated_df)
resultat = formater_chiffre_affaire(resultat)

# Afficher le résultat
print(resultat)
#creer_graphique(resultat)


# Fonction pour agréger les données par heure
def aggreguer_par_heure(df):
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Heure'] = df['Order Date'].dt.hour
    df['Date'] = df['Order Date'].dt.date
    df['Chiffre Affaire'] = df['Product Price']*df['Quantity']
    
    resultat = df.groupby(['Date', 'Heure'])['Chiffre Affaire'].sum().reset_index()
    resultat.rename(columns=lambda x: x.lower().replace(' ', '_'), inplace=True)
    return resultat

# Appels aux fonctions
resultat = aggreguer_par_heure(concatenated_df)
resultat = formater_chiffre_affaire(resultat)
# Afficher le résultat
print(resultat)
creer_graphique(resultat)
