import logging

# TODO: Добавить логирование в файл
def bot_setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    handler = logging.StreamHandler()  
    handler.setFormatter(formatter)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    return logger

logger = bot_setup_logger(__name__)
