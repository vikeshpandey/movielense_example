import utils
from entity_type import EntityType
from runner import personalize, personalize_rt

if __name__ == '__main__':
    log = utils.set_logging_properties('solution_handler')


def create_solution(solution_name, dataset_group_arn, perform_automl):
    log.info("creating solution...")
    response = personalize.create_solution(
        name=solution_name,
        datasetGroupArn=dataset_group_arn,
        performAutoML=perform_automl)
    solution_arn = response['solutionArn']
    log.info("solution created with arn: %s", solution_arn)

    solution_description = personalize.describe_solution(solutionArn=solution_arn)['solution']
    utils.wait_until_status_active(solution_description['status'], EntityType.SOLUTION, solution_arn)
    return solution_arn


def create_solution_version(solution_arn):
    log.info("creating solution version...")

    solution_version = personalize.create_solution_version(solutionArn=solution_arn)
    solution_version_arn = solution_version['solutionVersionArn']
    log.info("solution version arn is: " + solution_version_arn)

    solution_version_description = personalize.describe_solution_version(solutionVersionArn=solution_version_arn)[
        'solutionVersion']
    current_status = solution_version_description['status']
    utils.wait_until_status_active(current_status, 'solution_version', solution_version_arn)
    return solution_version_arn


def get_solution_metrics(solution_version_arn):
    solution_metrics = personalize.get_solution_metrics(solutionVersionArn=solution_version_arn)
    log.info("solution metrics are: %s", solution_metrics['metrics'])


def get_recommendations(campaign_arn, user_id):
    response = personalize_rt.get_recommendations(
        campaignArn=campaign_arn,
        userId=user_id)
    log.info("Recommended items for the user are: %s" + user_id)
    for item in response['itemList']:
        log.info(item['itemId'])


