import logging

def bot_setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    file_handler = logging.FileHandler('bot.log')
    file_handler.setFormatter(formatter)
    
    stream_handler = logging.StreamHandler()  
    stream_handler.setFormatter(formatter)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    
    return logger

logger = bot_setup_logger(__name__)
