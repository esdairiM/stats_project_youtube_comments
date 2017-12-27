import pprint
from time import time
from src.services.etl import ETLService
from src.services import logger


if __name__ == "__main__":
    logger.init_logger()
    etl=ETLService()
    print("finished building ")
    videoId = '-UAvLhaF-Eg'
    processed_comments=etl.extract_and_transform(videoId).get_comments()
    print(len(processed_comments))
    pprint.pprint(processed_comments[:4])
