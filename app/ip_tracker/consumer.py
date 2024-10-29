import json
import logging
import threading
from typing import Dict

import uvicorn
from confluent_kafka import Consumer, KafkaException
from fastapi import FastAPI

from settings.config import (BOOTSTRAP_SERVER_KAFKA, GROUP_KAFKA,
                             NAME_TOPIC_KAFKA, SLEEP_INTERVAL)

app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

origins = [
    "*",
]

app.title = "Lumu Api IPs tracker"
app.version = "1.0"

unique_ips = set()

conf: Dict = {
    "bootstrap.servers": BOOTSTRAP_SERVER_KAFKA,
    "group.id": GROUP_KAFKA,
    "auto.offset.reset": "earliest",
}
consumer = Consumer(conf)
consumer.subscribe([NAME_TOPIC_KAFKA])


def consume_messages():
    """
    Continuously consumes messages from the Kafka topic and adds unique IP addresses
    to the unique_ips set.

    This function runs in a separate thread.
    """
    while True:
        try:
            msg = consumer.poll(SLEEP_INTERVAL)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())

            message_value = json.loads(msg.value().decode("utf-8"))
            unique_ips.add(message_value["device_ip"])
            logging.info(f"Received message: {message_value}")
        except KafkaException as ke:
            logging.error(f"Kafka error: {ke}")
        except json.JSONDecodeError as je:
            logging.error(f"JSON decoding error: {je}")
        except Exception as e:
            logging.error(f"Error consuming messages: {e}")


threading.Thread(target=consume_messages, daemon=True).start()


@app.get(
    "/api/v1/unique_ip_count",
    status_code=200,
    response_description="Count of unique IP addresses"
)
def get_unique_ip_count():
    """
    Returns the current count of unique IP addresses seen in the messages.

    - **Responses:**
      - **200**: Returns the count of unique IP addresses successfully.

    **Returns:**
        dict: A dictionary containing the count of unique IP addresses.
        - Example: `{"unique_ip_count": 5}`
    """
    return {"unique_ip_count": len(unique_ips)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
