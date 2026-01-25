import logging
import datetime
import os
from config.paths import LOG_PATH

# Create log folder if it doesn't exist
os.makedirs(LOG_PATH, exist_ok=True)

# Generate a timestamp for the log filename
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

rag_agent_log_filename = os.path.join(LOG_PATH, f"rag_agent_{timestamp}.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(module)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(rag_agent_log_filename, encoding='utf-8'),
        logging.StreamHandler()
    ],
    force=True
)
log = logging.getLogger(__name__)

def log_node_start(node_name:str):
    log.info(f"{node_name} starts to work")
    return

def log_node_end(node_name:str, time_cost: float|None = None):
    if time_cost is not None:
        log.info(f"{node_name} finishes working, time costed: {time_cost} seconds.")
    else:
        log.info(f"{node_name} finishes working.")
    return