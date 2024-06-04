import sys
import os
from logging.config import fileConfig
from sqlalchemy import create_engine
from sqlalchemy import pool
from alembic import context

# Ajouter le chemin du répertoire parent au sys.path
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

# Ce modèle est votre module qui contient vos modèles SQLAlchemy
from app.models import Base

# Configuration de la connexion à la base de données
config = context.config

# Lecture du fichier de configuration `alembic.ini`
fileConfig(config.config_file_name)

# Définir l'objet `target_metadata` pour les modèles SQLAlchemy
target_metadata = Base.metadata

# Crée une fonction pour exécuter les migrations
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(config.get_main_option("sqlalchemy.url"))

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
