import awswrangler as wr
import boto3
import json
import random
import time


from botocore.config import config
from datetime import datetime


def main():
    # --- Athenas client configuration ---
    config = Config(
       retries = {
          "max_attempts": 3,  # default: 3
          "mode": "standard"
       }
    )
    # --- Instantiate client ---
    athena = boto3.client("athena", config=config)

    # --- Execute Athenas SQL query ---
    epoch = datetime.now().strftime("%s")
    key = f"pjud_scraper/query_results/{epoch}"
    queryStart = athena.start_query_execution(
        QueryString = "SELECT litigantes.nombre_o_razon_social, litigantes.rut, litigantes.sujeto, suma.partition_3 FROM pjud.litigantes, pjud.suma WHERE litigantes.rut='18354881-6' AND litigantes.partition_3=suma.partition_3 LIMIT 20;",
        QueryExecutionContext = {
            "Database": "pjud"
        }, 
        ResultConfiguration = {"OutputLocation": f"s3://pjud.data.athena.queries/{key}"}
    )

    # --- Start & check Athenas SQL query status ---
    check_athenas_query_state(client=athena, query=queryStart)

    # --- Query results ---

    results = athena.get_query_results(QueryExecutionId=queryStart["QueryExecutionId"])
    results = athena.get_query_results(QueryExecutionId=queryStart["QueryExecutionId"])
    json_data = json.dumps(results, indent=4)
    meta = json_data["ResponseMetadata"]

    rows = json_data["ResultSet"]["Rows"]  # list of dicts
    for row in rows:
        columns = row["Data"]
        for col in columns:
            col = col["VarCharValue"]

def check_athenas_query_state(client, query):
    backoff_in_seconds = 1
    while True:
        queryExecution = client.get_query_execution(QueryExecutionId=query["QueryExecutionId"])
        status_state = queryExecution["QueryExecution"]["Status"]["State"]
        print(f"Athenas State: {status_state}...ID {query['QueryExecutionId']}")

        # if Finished for any reason
        if status_state != "QUEUED" and status_state != "RUNNING":
            print(f"Exit Athenas Status: {status_state}")
            break

        # Exponential backoff sleep algorithm
        x = 0
        sleep = (
            backoff_in_seconds * 2 ** x + 
            random.uniform(0, 1)
        )
        time.sleep(sleep)
        x += 1

    return status_state