# movielense_example

how to execute this example?

Pre-requisites:
- a CSV file in an S3 bucket
- CSV file should have exactly 3 columns (USER_ID, ITEM_ID, TIMESTAMP) - it can have more columns as well but since the schema had
only these columns(and these 3 are the mandatory ones) that is why CSV has to match the schema. Please edit the CSV to conform to schema. You can
use any online tool to do that for you. One of the link to do that is: https://onlinecsvtools.com/delete-csv-columns

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