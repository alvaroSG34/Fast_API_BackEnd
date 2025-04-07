import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# 👉 Agregamos la ruta raíz al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 🔧 Importamos nuestras configuraciones y modelos
from app.core.config import settings
from app.db.base import Base
from app import models  # ¡Importante para registrar todos los modelos!

# Configuración de Alembic
config = context.config

# ⛽ Usamos la URL desde el archivo .env
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Configuración de logs
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 👉 Esta metadata es usada por 'autogenerate' para saber qué debe crear
target_metadata = Base.metadata

def run_migrations_offline():
    """Ejecuta migraciones sin conectar a la base."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Ejecuta migraciones con conexión activa."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # detecta cambios de tipo (opcional)
        )

        with context.begin_transaction():
            context.run_migrations()

# 🔁 Ejecuta offline u online según contexto
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
