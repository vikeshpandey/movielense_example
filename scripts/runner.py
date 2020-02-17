import solution_handler


file_name = 'schema.json'
INTERACTION_DATASET = 'Interactions'


if __name__ == '__main__':
    print("""before running this code, ensure that your CSV file is formatted as per the format
             desired by schema.json and IAM role has sufficient privliges, Also the s3 bucket 
             should have a trust relationship with the role assumed byp personalize""")

    print("enter the name for your schema: ")
    schema_name = input()
    schema_arn = solution_handler.create_schema(schema_name, file_name)

    print("enter the name for dataset group:")
    dataset_group_name = input()
    dataset_group_arn = solution_handler.create_dataset_group(dataset_group_name)

    print("enter the name of the dataset you want to create:")
    dataset_name = input()
    dataset_arn = solution_handler.create_dataset(dataset_name, schema_arn, dataset_group_arn, INTERACTION_DATASET)

    print("enter the dataset import job name:")
    dataset_import_job_name = input()
    print("enter the csv file location:")
    csv_file_location = input()
    print("enter the role arn personalize will assume:")
    iam_role_for_personalize = input()
    solution_handler.import_dataset(dataset_import_job_name, dataset_arn, csv_file_location, iam_role_for_personalize)

    print("enter the solution name:")
    solution_name = input()
    solution_arn = solution_handler.create_solution(solution_name, dataset_group_arn, perform_automl=True)

    solution_version_arn = solution_handler.create_solution_version(solution_arn)

    solution_handler.get_solution_metrics(solution_version_arn)

    print("enter campaign name:")
    campagin_name = input()
    campaign_arn = solution_handler.create_campaign(campagin_name, solution_version_arn)

    print("enter the user id for which you want to get recommendations:")
    user_id = input()
    solution_handler.get_recommendations(campaign_arn, user_id)
