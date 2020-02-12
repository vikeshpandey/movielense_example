from time import sleep
from entity_type import EntityType
from runner import personalize
import logging


def wait_until_status_active(current_status, entity_type, arn, time_in_seconds):
    while current_status != 'ACTIVE':
        log.info("status not active yet, will again in %s seconds", time_in_seconds)
        sleep(time_in_seconds)
        time_in_seconds = time_in_seconds**2
        current_status = get_status_from_type(entity_type, arn)
        log.info("status now: %s", current_status)


def get_status_from_type(entity_type, arn):
    if entity_type == EntityType.DATASET_GROUP:
        return personalize.describe_dataset_group(datasetGroupArn=arn)['datasetGroup']['status']
    elif entity_type == EntityType.DATASET_IMPORT_JOB:
        return personalize.describe_dataset_import_job(datasetImportJobArn=arn)['datasetImportJob']['status']
    elif entity_type == EntityType.SOLUTION:
        return personalize.describe_solution(solutionArn=arn)['solution']['status']
    elif entity_type == EntityType.SOLUTION_VERSION:
        return personalize.describe_solution_version(solutionVersionArn=arn)['solutionVersion']['status']
    elif entity_type == EntityType.CAMPAIGN:
        return personalize.describe_campaign(campaignArn=arn)['campaignArn']['status']


def set_logging_properties(file_name):
    logger = logging.getLogger(file_name)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    logger.addHandler(stream_handler)
    return log


if __name__ == '__main__':
    log = set_logging_properties('utils')
