import logging
import os
from datetime import datetime


log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Define file path
log_filename = datetime.now().strftime("habit_log_%Y-%m-%d_%H-%M-%S.log")
log_file_path = os.path.join(log_dir, log_filename)

# Configure logging
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Connecting to the database.")