# movielense_example

how to execute this example?

Pre-requisites:
- a CSV file in an S3 bucket
- set bucket policy to provide personalize access to the bucket. Follow instructions at: https://docs.aws.amazon.com/personalize/latest/dg/data-prep-upload-s3.html
- create an IAM role which authorizes personalize to access the bucket and other resources needed. follow the link at: https://docs.aws.amazon.com/personalize/latest/dg/aws-personalize-set-up-permissions.html


Please note:
- This example currently does not clean up the resources created. 
The support for which will be added in future. Also, no exception 
handling is in place currently.
- it currently supports interactions dataset only as that is main dataset personalize needs to work. the schema template already
present in the repo under '''scripts'''


instructions for running the project:
- Clone or download the project
- Import into your favourite IDE
- Execute runner.py
    - It will ask for user inputs for multiple inputs and complete the steps