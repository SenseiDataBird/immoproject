import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder

# Lecture des données brutes
df = pd.read_csv('house_pred.csv')

# Création d'une copie pour le ML
df_ml = df.copy()

# Vérification des valeurs manquantes
print("Valeurs manquantes par colonne :")
print(df_ml.isnull().sum())

# Traitement des valeurs manquantes
# Pour les colonnes numériques, on remplace par la médiane
numeric_columns = ['Area', 'YearBuilt']
for col in numeric_columns:
    df_ml[col].fillna(df_ml[col].median(), inplace=True)

# Pour les colonnes catégorielles, on remplace par le mode (la valeur la plus fréquente)
categorical_columns = ['Location', 'Garage', 'Condition']
for col in categorical_columns:
    df_ml[col].fillna(df_ml[col].mode()[0], inplace=True)

# Standardisation des données numériques
scaler = StandardScaler()
df_ml[['Area', 'YearBuilt']] = scaler.fit_transform(df_ml[['Area', 'YearBuilt']])

# One Hot Encoding pour toutes les variables catégorielles
ohe = OneHotEncoder(sparse_output=False, drop='first')
all_cat_encoded = ohe.fit_transform(df_ml[['Location', 'Garage', 'Condition']])

# Création des noms de colonnes pour les variables encodées
location_categories = ohe.categories_[0][1:]  # On exclut la première catégorie (drop='first')
garage_categories = ohe.categories_[1][1:]
condition_categories = ohe.categories_[2][1:]
new_columns = [f'Location_{cat}' for cat in location_categories] + \
              [f'Garage_{cat}' for cat in garage_categories] + \
              [f'Condition_{cat}' for cat in condition_categories]

# Création d'un DataFrame avec les variables encodées
encoded_df = pd.DataFrame(all_cat_encoded, columns=new_columns)

# Concaténation des données
df_ml = pd.concat([
    df_ml.drop(['Location', 'Garage', 'Condition'], axis=1),  # Suppression des colonnes originales
    encoded_df  # Ajout des colonnes encodées
], axis=1)

# Sauvegarde du jeu de données prétraité
df_ml.to_csv('house_pred_for_ml.csv', index=False)

print("\nPrétraitement terminé !")
print("\nAperçu des données prétraitées :")
print(df_ml.head())

print("\nInformations sur les colonnes :")
print(df_ml.info()) 