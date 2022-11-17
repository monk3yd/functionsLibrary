import os
import json
import boto3
import random
import time

from payloads import payloads, pdf_to_str, generate_payload


def main():
    ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    SECRET_KEY = os.getenv("AWS_SECRET_KEY")

    # Instantiate lambda
    client = boto3.client(
        "lambda",
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name="sa-east-1"
    )
    for payload in payloads:
        start = time.perf_counter()
        # payload = random.choice(payloads)
        pdf_str = pdf_to_str(payload["pdf_path"])
        lambda_payload = generate_payload(payload["is_scan"], pdf_str)
        print(f"Test Name: {str(payload['pdf_path'])}")

        lambda_response = client.invoke(
            FunctionName="rvm-scanner",
            InvocationType="RequestResponse",
            Payload=json.dumps(lambda_payload),
        )
        dict_lambda_response = json.loads(lambda_response["Payload"].read().decode("UTF-8"))  # bytes to dict
        print(dict_lambda_response)
        finish = time.perf_counter()
        print(f'Finished in {round(finish-start, 2)} second(s)')
        print()


if __name__ == "__main__":
    # start = time.perf_counter()
    main()
    # finish = time.perf_counter()
    # print(f'Finished in {round(finish-start, 2)} second(s)')
