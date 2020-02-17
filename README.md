# movielense_example

how to execute this example?

Pre-requisites:
- a CSV file in an S3 bucket
- set bucket policy to provide personalize access to the bucket
- create an IAM role which authorizes personalize to access the bucket


Please note:
- This example currently does not clean up the resources created. 
The support for which will be added in future. Also, no exception 
handling is in place currently.

- Clone or download the project
- Import into your favourite IDE
- Execute runner.py
    - It will ask for user inputs, once provided the program will resume