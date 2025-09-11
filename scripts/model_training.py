import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb
import joblib

# Chargement des données prétraitées
df = pd.read_csv('data/house_pred_for_ml.csv')

# Séparation des features (X) et de la target (y)
X = df.drop('Price', axis=1)
y = df['Price']

# Division en ensembles d'entraînement et de test (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Création et entraînement du modèle XGBoost
model = xgb.XGBRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    min_child_weight=1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

model.fit(X_train, y_train)

# Évaluation du modèle
y_pred = model.predict(X_test)

# Calcul des métriques
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("\nRésultats de l'évaluation du modèle :")
print(f"RMSE : {rmse:.2f}")
print(f"R² : {r2:.4f}")

# Écriture des métriques dans un fichier (pour Airflow/K8s)
metrics_path = "/opt/airflow/data/metrics.txt"
with open(metrics_path, "w", encoding="utf-8") as f:
    f.write(f"RMSE: {rmse:.2f}\nR2: {r2:.4f}\n")

# Affichage de l'importance des features
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': model.feature_importances_
})
feature_importance = feature_importance.sort_values('Importance', ascending=False)
print("\nImportance des features :")
print(feature_importance)

# Sauvegarde du modèle
joblib.dump(model, 'immo_model.joblib')

# Fonction pour faire des prédictions
def predict_price(features):
    """
    Fait une prédiction de prix basée sur les features fournies
    
    Args:
        features (dict): Dictionnaire contenant les features nécessaires
        
    Returns:
        float: Prix prédit
    """
    # Conversion des features en DataFrame
    features_df = pd.DataFrame([features])
    
    # Prédiction
    prediction = model.predict(features_df)[0]
    
    return prediction

# Exemple d'utilisation
if __name__ == "__main__":
    # Exemple de features pour tester le modèle
    test_features = X_test.iloc[0].to_dict()
    predicted_price = predict_price(test_features)
    actual_price = y_test.iloc[0]
    
    print("\nExemple de prédiction :")
    print(f"Prix prédit : {predicted_price:.2f}")
    print(f"Prix réel : {actual_price:.2f}") 
