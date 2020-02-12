from enum import Enum


class EntityType(Enum):
    DATASET_GROUP = 'dataset_group'
    DATASET_IMPORT_JOB = 'dataset_import_job'
    SOLUTION = 'solution'
    SOLUTION_VERSION = 'solution_version'
    CAMPAIGN = 'campaign'
