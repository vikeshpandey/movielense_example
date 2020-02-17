
import boto3
import logging


if __name__ == '__main__':
    log = logging.getLogger(__name__)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    log.addHandler(stream_handler)
    personalize = boto3.client('personalize')





# def set_logging_properties(file_name):
#     logger = logging.getLogger(file_name)
#     stream_handler = logging.StreamHandler()
#     stream_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
#     logger.addHandler(stream_handler)
#     return logger



