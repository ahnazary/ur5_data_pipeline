"""
Module that reads joint angles published by the UR5 robot.
The angles are stored in csv files and dumpled to a postgres database on exit.
"""

import os
from datetime import datetime

import numpy as np
import paho.mqtt.client as mqtt
import pandas as pd

from utils import S3Interface, emit_log, pg_engine, setup_pg_table

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "ur5/joint_angles"

# We will be storing the angles in a pandas df, so later on we can save it to a CSV in cloud (AWS S3) or a postgres
columns = [
    "shoulder_pan",
    "shoulder_lift",
    "elbow",
    "wrist_1",
    "wrist_2",
    "wrist_3",
    "timestamp",
]
data_list = []
engine = pg_engine()


def on_connect(client, userdata, flags, rc):
    emit_log(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    global data_list
    try:
        joint_angles = eval(msg.payload.decode())

        # Convert to DataFrame format
        row = list(joint_angles.values())
        data_list.append(row)
        emit_log(f"Received: {dict(zip(columns, row))}")

    except Exception as e:
        emit_log(f"Error: {e}")


def start_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        # Convert data list to DataFrame
        df = pd.DataFrame(data_list, columns=columns)
        df.to_csv("ur5_joint_angles.csv", index=False)
        df.to_sql("ur5_joint_angles", engine, if_exists="append", index=False)

        # Upload to S3, if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set
        if all(
            key in os.environ for key in ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]
        ):
            s3 = S3Interface()
            s3.upload_to_s3("ur5-joint-angles") # change the bucket name accordingly

        emit_log("Data saved to CSV in file named ur5_joint_angles.csv")


if __name__ == "__main__":
    setup_pg_table()
    start_mqtt_client()
