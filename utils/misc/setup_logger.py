import logging

def bot_setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    

    
    stream_handler = logging.StreamHandler()  
    stream_handler.setFormatter(formatter)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(stream_handler)
    
    return logger

logger = bot_setup_logger(__name__)
