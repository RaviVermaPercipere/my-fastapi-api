import os
import logging

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/etl.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)