import boto3
import utils
from entity_type import EntityType
import logging
from time import sleep


personalize = boto3.client('personalize')
personalize_rt = boto3.client('personalize-runtime')

log = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(stream_handler)
log.setLevel(level=logging.INFO)


def create_schema(schema_name, schema_file):
    log.info("creating schema...")
    with open(schema_file) as f:
        response = personalize.create_schema(
            name=schema_name,
            schema=f.read()
        )

    schema_arn = response['schemaArn']
    log.info("schema created with the arn: %s", schema_arn)

    return schema_arn


def create_dataset_group(dataset_group_name):
    log.info("creating dataset group...")
    response = personalize.create_dataset_group(name=dataset_group_name)
    dsg_arn = response['datasetGroupArn']
    log.info("dataset group created with the arn: %s", dsg_arn)

    description = personalize.describe_dataset_group(datasetGroupArn=dsg_arn)['datasetGroup']
    status = description['status']
    wait_until_status_active(status, EntityType.DATASET_GROUP, description['datasetGroupArn'], 5)
    return dsg_arn


def create_dataset(dataset_name, schema_arn, dataset_group_arn, dataset_type):
    log.info("creating dataset...")
    response = personalize.create_dataset(
        name=dataset_name,
        schemaArn=schema_arn,
        datasetGroupArn = dataset_group_arn,
        datasetType = dataset_type)
    dataset_arn = response['datasetArn']
    log.info("dataset created with arn: %s", dataset_arn)
    return dataset_arn


def import_dataset(job_name, dataset_arn, csv_file_path, role_arn):
    log.info("importing dataset...")
    response = personalize.create_dataset_import_job(
        jobName=job_name,
        datasetArn=dataset_arn,
        dataSource={'dataLocation': csv_file_path},
        roleArn=role_arn)

    dataset_import_job_arn = response['datasetImportJobArn']
    log.info('dataset import job created with arn: %s' + dataset_import_job_arn)

    description = personalize.describe_dataset_import_job(datasetImportJobArn=dataset_import_job_arn)['datasetImportJob']
    current_status = description['status']
    wait_until_status_active(current_status, EntityType.DATASET_IMPORT_JOB, description['datasetImportJobArn'], 5)


def create_solution(solution_name, dataset_group_arn, perform_automl):
    log.info("creating solution...")
    response = personalize.create_solution(
        name=solution_name,
        datasetGroupArn=dataset_group_arn,
        performAutoML=perform_automl)
    solution_arn = response['solutionArn']
    log.info("solution created with arn: %s", solution_arn)

    solution_description = personalize.describe_solution(solutionArn=solution_arn)['solution']
    wait_until_status_active(solution_description['status'], EntityType.SOLUTION, solution_arn, 10)
    return solution_arn


def create_solution_version(solution_arn):
    log.info("creating solution version...")

    solution_version = personalize.create_solution_version(solutionArn=solution_arn)
    solution_version_arn = solution_version['solutionVersionArn']
    log.info("solution version arn is: " + solution_version_arn)

    solution_version_description = personalize.describe_solution_version(solutionVersionArn=solution_version_arn)[
        'solutionVersion']
    current_status = solution_version_description['status']
    wait_until_status_active(current_status, EntityType.SOLUTION_VERSION, solution_version_arn, 10)
    return solution_version_arn


def get_solution_metrics(solution_version_arn):
    solution_metrics = personalize.get_solution_metrics(solutionVersionArn=solution_version_arn)
    log.info("solution metrics are: %s", solution_metrics['metrics'])


def create_campaign(campaign_name, solution_version_arn):
    response = personalize.create_campaign(
        name=campaign_name,
        solutionVersionArn=solution_version_arn,
        minProvisionedTPS=10)
    campaign_arn = response['campaignArn']

    log.info("campaign created with arn: %s", response['campaignArn'])

    description = personalize.describe_campaign(campaignArn=campaign_arn)['campaign']
    wait_until_status_active(description['status'], EntityType.CAMPAIGN, campaign_arn, 10)
    return campaign_arn


def get_recommendations(campaign_arn, user_id):
    response = personalize_rt.get_recommendations(
        campaignArn=campaign_arn,
        userId=user_id)
    log.info("Recommended items for the user are: %s" + user_id)
    for item in response['itemList']:
        log.info(item['itemId'])


########utility methods
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