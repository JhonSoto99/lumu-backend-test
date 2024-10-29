import json
import logging
import random
import time
from datetime import datetime, timezone
from typing import Dict

from confluent_kafka import Producer

from settings.config import (BOOTSTRAP_SERVER_KAFKA, ERROR_CODE_MAX,
                             ERROR_CODE_MIN, IP_RANGE_END, IP_RANGE_START,
                             NAME_TOPIC_KAFKA, SLEEP_INTERVAL,
                             TIMESTAMP_FORMATS)

conf: Dict = {"bootstrap.servers": BOOTSTRAP_SERVER_KAFKA}
producer = Producer(conf)


def delivery_report(err, msg) -> None:
    """Reports the delivery status of a message to Kafka.

    Args:
        err (KafkaError): Error, if any, when sending the message.
        msg (Message): Message that was attempted to send.
    """
    if err:
        logging.error(f"Failed to deliver message: {err}")
    else:
        logging.info(
            f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}"
        )


def generate_timestamp() -> str:
    """Generates a timestamp in various formats.

    Returns:
        str: A formatted timestamp string.
    """
    fmt = random.choice(TIMESTAMP_FORMATS)
    now = datetime.now(timezone.utc)
    if fmt == "unix_millis":
        return str(int(now.timestamp() * 1000))
    elif fmt == "unix_seconds":
        return str(int(now.timestamp()))
    else:
        return now.strftime(fmt)


def generate_device_ip() -> str:
    """Generates a random device IP address within the specified range.

    Returns:
        str: A randomly generated IP address.
    """
    return ".".join(str(random.randint(IP_RANGE_START, IP_RANGE_END)) for _ in range(4))

def produce_messages():
    """Function to produce messages continuously."""
    try:
        while True:
            message = {
                "timestamp": generate_timestamp(),
                "device_ip": generate_device_ip(),
                "error_code": random.randint(ERROR_CODE_MIN, ERROR_CODE_MAX),
            }
            producer.produce(
                NAME_TOPIC_KAFKA,
                json.dumps(message).encode("utf-8"),
                callback=delivery_report,
            )
            producer.poll(1)
            time.sleep(SLEEP_INTERVAL)
    except KeyboardInterrupt:
        logging.info("Production manually interrupted.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        producer.flush()
        logging.info("All messages were successfully sent.")


if __name__ == "__main__":
    try:
        while True:
            message = {
                "timestamp": generate_timestamp(),
                "device_ip": generate_device_ip(),
                "error_code": random.randint(ERROR_CODE_MIN, ERROR_CODE_MAX),
            }
            producer.produce(
                NAME_TOPIC_KAFKA,
                json.dumps(message).encode("utf-8"),
                callback=delivery_report,
            )
            producer.poll(1)
            time.sleep(SLEEP_INTERVAL)
    except KeyboardInterrupt:
        logging.info("Production manually interrupted.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        producer.flush()
        logging.info("All messages were successfully sent.")
