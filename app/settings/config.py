import logging
from typing import List
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


NAME_TOPIC_KAFKA: str = "ip_tracker"
BOOTSTRAP_SERVER_KAFKA: str = "localhost:29092"
GROUP_KAFKA: str = "ip_tracker_group"
SLEEP_INTERVAL: int = 1
IP_RANGE_START: int = 0
IP_RANGE_END: int = 255
ERROR_CODE_MIN: int = 0
ERROR_CODE_MAX: int = 10

TIMESTAMP_FORMATS: List = [
    "%Y-%m-%dT%H:%M:%S.%fZ",
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%S",
    "unix_millis",
    "unix_seconds",
]