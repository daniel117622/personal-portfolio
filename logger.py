import logging
import sys

def get_logger(name="flask_app"):
    logger = logging.getLogger(name)
    
    # Guard clause: return early if handlers are already configured
    if logger.handlers:
        return logger
        
    logger.setLevel(logging.INFO)
    
    # Stream logs to stdout for Docker compatibility
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger