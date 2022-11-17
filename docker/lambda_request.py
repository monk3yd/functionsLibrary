import time
import json
import requests

from payloads import payloads, pdf_to_str, generate_request_payload


def main():
    url = "https://osbh7mam5j.execute-api.sa-east-1.amazonaws.com/default/rvm-scanner"

    for payload in payloads:
        pdf_str = pdf_to_str(payload["pdf_path"])
        lambda_payload = generate_request_payload(payload["is_scan"], pdf_str)
        print(f"Test Name: {str(payload['pdf_path'])}")
        headers = {
          'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=lambda_payload)

        print(response.text)


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    finish = time.perf_counter()
    print(f'Finished in {round(finish-start, 2)} second(s)')
