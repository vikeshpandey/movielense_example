from runner import personalize
import utils
from entity_type import EntityType


if __name__ == '__main__':
    log = utils.set_logging_properties('dataset_handler')


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
    utils.wait_until_status_active(status, EntityType.DATASET_GROUP, description['datasetGroupArn'])
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
        dataSource={csv_file_path},
        roleArn=role_arn)

    dataset_import_job_arn = response['datasetImportJobArn']
    log.info('dataset import job created with arn: %s' + dataset_import_job_arn)

    description = personalize.describe_dataset_import_job(datasetImportJobArn=dataset_import_job_arn)['datasetImportJob']
    current_status = description['status']
    utils.wait_until_status_active(current_status, EntityType.DATASET_IMPORT_JOB, description['datasetImportJobArn'])
