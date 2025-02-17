""" This module contains utility functions"""

import logging
from os import getenv

import sqlalchemy as sa

logger = logging.getLogger(__name__)


def emit_log(message: str, log_level: int = logging.INFO):
    """Creates a custom logger and emits logs.

    Args:
        log_level (int): Log level.
        message (str): Message to log.

    Returns:
        None
    """
    logger.setLevel(log_level)

    ch = logging.StreamHandler()
    ch.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    logger.log(log_level, message)

def pg_engine():
    """
    Function that returns a postgres engine
    If a DATABASE_URL environment variable is set, it will connect to the database specified in the URL
    Otherwise, it will connect to a local postgres database
    """

    connection_string = getenv("DATABASE_URL")
    return (
        sa.create_engine("postgresql://postgres:postgres@localhost:5433/postgres")
        if connection_string is None
        else sa.create_engine(connection_string)
    )

def setup_pg_table():
    """
    Function that creates a postgres table called ur5_joint_angles if it doesn't exist
    If a DATABASE_URL environment variable is set, it will connect to the database specified in the URL
    Otherwise, it will connect to a local postgres database
    """

    engine = pg_engine()

    query = sa.text(
        """
        CREATE TABLE IF NOT EXISTS ur5_joint_angles (
            shoulder_pan FLOAT,
            shoulder_lift FLOAT,
            elbow FLOAT,
            wrist_1 FLOAT,
            wrist_2 FLOAT,
            wrist_3 FLOAT,
            timestamp TIMESTAMP
        )
        """
        )
    

    with engine.connect() as conn:
        conn.execute(query)
        conn.commit()
        emit_log("Table created successfully")



