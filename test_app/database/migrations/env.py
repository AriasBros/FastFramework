import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import URL, pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from backend.src.app.database.config import DatabaseConfig
from backend.src.app.utils import get_settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name, disable_existing_loggers=False)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    config_data = config.get_section(config.config_ini_section, {})

    if not config_data.get("sqlalchemy.url"):
        database_config = DatabaseConfig.from_settings(get_settings())
        url = URL.create(
            drivername=database_config.driver,
            username=database_config.username,
            password=database_config.password,
            host=database_config.host,
            port=database_config.port,
            database=database_config.database,
        )
        config_data["sqlalchemy.url"] = url.render_as_string(hide_password=False)

    connectable = async_engine_from_config(
        config_data,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


run_migrations_online()
