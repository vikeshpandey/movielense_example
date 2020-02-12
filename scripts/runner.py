import boto3

import dataset_handler
import solution_handler
import utils

personalize = boto3.client('personalize')
personalize_rt = boto3.client('personalize-runtime')
file_name = 'schema.json'
INTERACTION_DATASET = 'Interactions'
CSV_FILE_LOCATION = "'dataLocation': 's3://pandvike/personalize/movielense_example/ratings.csv'"
IAM_ROLE_FOR_PERSONALIZE = "'arn:aws:iam::018632230441:role/service-role/AmazonPersonalize-ExecutionRole-1580740463907'"

if __name__ == '__main__':
    log = utils.set_logging_properties('runner')

    print("enter the name for your schema:")
    schema_name = input()
    schema_arn = dataset_handler.create_schema(schema_name, file_name)

    print("enter the name for dataset group:")
    dataset_group_name = input()
    dataset_group_arn = dataset_handler.create_dataset_group(dataset_group_name)

    print("enter the name of the dataset you want to create:")
    dataset_name = input()
    dataset_arn = dataset_handler.create_dataset(dataset_name, schema_arn, dataset_group_arn, INTERACTION_DATASET)

    print("enter the dataset import job name:")
    dataset_import_job_name = input()
    dataset_handler.import_dataset(dataset_import_job_name, dataset_arn, CSV_FILE_LOCATION, IAM_ROLE_FOR_PERSONALIZE)

    print("enter the solution name:")
    solution_name = input()
    solution_arn = solution_handler.create_solution(solution_name, dataset_group_arn, perform_automl=True)
    solution_version_arn = solution_handler.create_solution_version(solution_arn)
    solution_handler.get_solution_metrics(solution_version_arn)

    campaign_arn = create_campaign('arn:aws:personalize:us-east-1:018632230441:solution/MovieLenseSolution/39908009')
    # get_recommendations(campaign_arn='arn:aws:personalize:us-east-1:018632230441:campaign/MovieLensCampaign', user_id='10')
    get_personalized_recommendations(
        campaign_arn='arn:aws:personalize:us-east-1:018632230441:campaign/MovieLensCampaign', user_id='10')
