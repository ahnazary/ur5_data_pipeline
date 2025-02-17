""" This module contains utility functions"""

import logging
import os
import pathlib
from datetime import datetime
from os import getenv

import boto3
import pandas as pd
import sqlalchemy as sa

from pydantic import BaseModel, Field
from typing import List

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


class S3Interface:
    """
    Class to interact with s3
    """

    def __init__(self):
        self.s3_client = boto3.client("s3")
        self.s3_resource = boto3.resource("s3")

    def get_bucket_names(self) -> list:
        """
        Method to get the names of the buckets in s3

        Returns
        -------
        list
            list with the names of the buckets in s3
        """
        response = self.s3_client.list_buckets()
        buckets = [bucket["Name"] for bucket in response["Buckets"]]
        return buckets

    def upload_to_s3(self, bucket_name: str) -> None:
        """
        Method to dump csv from local to AWS s3
        """

        # get current dir path and append file name
        file_path = os.path.join(
            pathlib.Path(__file__).parent.absolute(), "ur5_joint_angles.csv"
        )

        # upload file to s3
        self.s3_client.upload_file(file_path, bucket_name, "ur5_joint_angles.csv")

class JointAngles(BaseModel):
    shoulder_pan: float = Field(..., ge=-3.14, le=3.14)
    shoulder_lift: float = Field(..., ge=-3.14, le=3.14)
    elbow: float = Field(..., ge=-3.14, le=3.14)
    wrist_1: float = Field(..., ge=-3.14, le=3.14)
    wrist_2: float = Field(..., ge=-3.14, le=3.14)
    wrist_3: float = Field(..., ge=-3.14, le=3.14)
    timestamp: str
