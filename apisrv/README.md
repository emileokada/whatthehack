# How to test locally

1. Install SAM local using npm:

        npm install -g aws-sam-local

2. Update `template.yml` to change the API.

3. Update `lambda_function.py` to implement the API.

3. Test it for a single request:

      echo '{"httpMethod": "GET"}' | sam local invoke BeerPlaces

4. Run the service on localhost

      sam local start-api

Based on this [AWS blog](https://aws.amazon.com/blogs/aws/new-aws-sam-local-beta-build-and-test-serverless-applications-locally/)
