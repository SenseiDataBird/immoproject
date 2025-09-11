from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

# DAG pédagogique minimal: 2 tâches séquentielles
# - preprocess_data: exécute scripts/data_processing.py dans le dossier data
# - train_model: exécute scripts/model_training.py dans le dossier projet (attend data/house_pred_for_ml.csv)

default_args = {
    "owner": "cdp-demo",
}

with DAG(
    dag_id="pipeline_immo_demo",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,  # Lancement manuel pour la démo
    catchup=False,
    default_args=default_args,
    description="Pipeline démo: nettoyage → entraînement XGBoost",
) as dag:

    preprocess_data = BashOperator(
        task_id="preprocess_data",
        bash_command="cd /opt/airflow/data && python /opt/airflow/scripts/data_processing.py",
    )

    train_model = BashOperator(
        task_id="train_model",
        bash_command="cd /opt/airflow && python /opt/airflow/scripts/model_training.py",
    )

    preprocess_data >> train_model
