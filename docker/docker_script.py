import time
import json
import requests

from payloads import payloads, pdf_to_str, generate_payload


def main():
    url = "http://localhost:9000/2015-03-31/functions/function/invocations"

    for payload in payloads:
        # payload = random.choice(payloads)
        pdf_str = pdf_to_str(payload["pdf_path"])
        docker_payload = generate_payload(payload["is_scan"], pdf_str)
        print(f"Test Name: {str(payload['pdf_path'])}")
        headers = {
          'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=json.dumps(docker_payload))
        print(response.text)
        print()


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    finish = time.perf_counter()
    print(f'Finished in {round(finish-start, 2)} second(s)')
