import time

import numpy as np
import paho.mqtt.client as mqtt
from datetime import datetime

from utils import emit_log, setup_pg_table

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "ur5/joint_angles"

# We imagine the UR5 robot has 6 joints
JOINT_NAMES = [
    "shoulder_pan",
    "shoulder_lift",
    "elbow",
    "wrist_1",
    "wrist_2",
    "wrist_3",
]


# function to generate random joint angles
def generate_joint_angles(t):
    angles = {joint: np.sin(t + i) * np.pi / 4 for i, joint in enumerate(JOINT_NAMES)}
    # add current timestamp
    angles["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    return angles


# MQTT Client setup
client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    emit_log(f"Connected to MQTT broker with result code {rc}")


def publish_joint_angles():
    t = 0
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

    try:
        while True:
            joint_angles = generate_joint_angles(t)
            client.publish(MQTT_TOPIC, str(joint_angles))
            emit_log(f"Published: {joint_angles}")

            t += 0.1
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    setup_pg_table()
    publish_joint_angles()
