import sys
import os
from os import path
from alembic import context
from logging.config import fileConfig
from sqlalchemy import engine_from_config,pool
import logging

sys.path.insert(0,(path.dirname(path.dirname(path.abspath(__file__)))))

from app.models import Base
from app.config import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.

config = context.config # context is an object that combines the script_location(opens both versions and env.py arranges it accordingly) and the alembic.ini settings-> config = Congig('alembic.ini)
if config.config_file_name is not None:
    fileConfig(config.config_file_name) # Now fileconfig is a python code that fetches the loggers in the alembic.ini file


#4.Dynamic Url: decide which database to talk to 
#check for an environment variable first(great for render/ heroku)
external_url = os.getenv("DATABASE_URL_EXTERNAL")
if external_url:
    target_url = external_url

else:
    target_url = (
    "postgresql://" + 
    f"{settings.database_username}:{settings.database_password}@" + 
    f"{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)


# 5. INJECTION tell alembic to use this specific URL
config.set_main_option("sqlalchemy.url",target_url)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )# it is the one that compares the database and the metadata ... and writes the code in sql when you run alembic upgrade head --sql in the terminal but does not actually perform the build itself inside the postgres

    with context.begin_transaction():# so the context.begin_transaction allows to rewind the build if there is an error that has occurred... after it checks everything is in place and that no error has occurred
        context.run_migrations() # Now after the safety net has caught no error the actual build begins
        #The alembic revision --autogenerate compares your database and metadata and creates the revision to create the missing table or column in the database
        # Now alembic upgrade head actually performs the transaction
        # this is what that actually runs the env file with the migrations

print(f"DEBUG: Connecting to host: {settings.database_hostname}")
def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    url = config.get_main_option("sqlalchemy.url")
    print(f"ALEMBIC DEBUG: Using URL: {url.split('@')[-1]}") # Safely logs the host only
    connectable = engine_from_config(
        
        config.get_section(config.config_ini_section, {}),#config.config_ini_section.. actually returns the main section in the lembic.ini file which is [alembic]
        prefix="sqlalchemy.",# in the [alembic] focus with only the options starting with sqlalchemy.
        poolclass=pool.NullPool,#after we first compare the difference with the base.metadata and the database we will transport(Pool) the changes only once(NullPool)
        url=url
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
