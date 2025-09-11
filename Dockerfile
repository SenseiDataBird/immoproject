# Image de base Airflow officielle (inclut Python et Airflow préinstallés)
FROM apache/airflow:2.9.3-python3.11

# Passer root pour installation de dépendances et copie de fichiers
USER root

# Créer les répertoires de travail
RUN mkdir -p /opt/airflow/scripts /opt/airflow/data /opt/airflow/dags

# Copier le code et les données dans l'image
COPY scripts/ /opt/airflow/scripts/
COPY data/ /opt/airflow/data/

# Installer dépendances Python additionnelles (modélisation, data)
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Droits pour l'utilisateur airflow
RUN chown -R airflow:root /opt/airflow && \
    chmod -R 775 /opt/airflow

# Copier le DAG Airflow
COPY airflow/dags/ /opt/airflow/dags/

# Repasser à l'utilisateur airflow
USER airflow

# Dossier de travail
WORKDIR /opt/airflow

# Valeurs par défaut: lancer Airflow en mode standalone (webserver + scheduler)
ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["bash", "-lc", "airflow standalone"]
