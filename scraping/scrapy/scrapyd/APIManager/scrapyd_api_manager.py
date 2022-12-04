import json
import logging
import os
import pandas as pd
import requests
import sqlite3
import sys
import time


def main():
    # Scrapyd's API Manager
    # https://scrapyd.readthedocs.io/en/latest/api.html

    # logging: debug info warning error critical
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Initialize Scrapyd's API Manager")

    SLEEP_TIME = 180
    logging.info(f"SLEEP_TIME_IN_SECONDS: {SLEEP_TIME}")

    LISTJOBS_PATH = "services/listjobs.json"
    logging.info(f"LISTJOBS_FILE_PATH: {LISTJOBS_PATH}")

    DAEMONSTATUS_PATH = "services/daemonstatus.json"
    logging.info(f"DAEMONSTATUS_FILE_PATH: {DAEMONSTATUS_PATH}")
    
    DATABASE_PATH = "dbs/listjobs.db"
    logging.info(f"DATABASE_PATH: {DATABASE_PATH}")


    logging.info("Listening to scrapyd server...")
    while True:
        logging.info("Checking status...")

        # --- DaemonStatus ---
        # save_daemonstatus(DAEMONSTATUS_PATH)

        # --- ListJobs ---
        save_listjobs(LISTJOBS_PATH)
       
        # W8 for next check
        logging.info(f"Time for next status report: {SLEEP_TIME} seconds...\n")
        time.sleep(SLEEP_TIME)

    # --- Schedule ---
    # spider_data = {}
    # add_to_schedule(spider_data)


def save_listjobs(file_path):
    '''
    Get the list of pending, running and finished jobs of some project.

    Supported Request Methods: GET
    Parameters:
        project (string, option) - restrict results to project name
    '''

    if os.path.exists():

    url = "http://127.0.0.1:6800/listjobs.json"
    response = requests.get(url=url)

    # Update listjobs JSON file
    logging.info("Saving updated listjobs in JSON file...")
    with open(file_path, "w") as file:
        file.write(json.dumps(response.json(), indent=4))

    # Read updated data from listjobs
    logging.info("Reading updated listjobs from JSON file...")
    with open(file_path, "r") as file:
        json_data = json.loads(file.read())
    
    pending_jobs = json_data["pending"]
    running_jobs = json_data["running"]
    finished_jobs = json_data["finished"]  # List of dicts

    # No jobs
    if not pending_jobs and not running_jobs and not finished_jobs:
        logger.warning("Couldn't find any jobs in listjobs...")  # listjobs is empty
        sys.exit()

    # Jobs finished
    if not pending_jobs and not running_jobs and finished_jobs:
        logging.info("Jobs finished...100%")
        finished_df = pd.DataFrame(finished_jobs)
        
        # Save to db
        logging.info("Updating database...")
        update_database(finished_df)
    
    # Jobs almost finished
    if not pending_jobs and running_jobs and finished_jobs:
        logging.info("Jobs almost finished...")
        running_df = pd.DataFrame(running_jobs)
        finished_df = pd.DataFrame(finished_jobs)
        
        # Merge
        # merged_df = finished_df.merge(running_df, how="outer")

        # Save to db
        # update_database(merged_df)
    
    # Jobs are stale (not scraping)
    if pending_jobs and not running_jobs and finished_jobs:
        logging.warning("Jobs are stale (not scraping)...")
        pending_df = pd.DataFrame(pending_jobs)
        finished_df = pd.DataFrame(finished_jobs)
        
        # Merge
        # merged_df = finished_df.merge(pending_df, how="outer")

        # Save to db
        # update_database(merged_df)
    
    # Scraping jobs
    if pending_jobs and running_jobs and finished_jobs:
        logging.info("Scraping...!")
        pending_df = pd.DataFrame(pending_jobs)
        running_df = pd.DataFrame(running_jobs)
        finished_df = pd.DataFrame(finished_jobs)
        
        # Merge
        updated_df = finished_df.merge(running_df, how="outer").merge(pending_df, how="outer")

        # Save to db
        update_database(updated_df)

def update_database(updated_df):
    database = "dbs/listjobs.db"

    logging.info("connecting to sql database...")
    conn = create_connection(database)
    if conn is none:
        logging.error("could not establish connection with database...")

    # if database doesn't exist
    if not os.path.exists(database):
        logging.info(f"creating listjobs database at {database}...")
        updated_df.to_sql(name="jobs", con=conn)

    # else:
        # read db into dataframe
        # database_df = pd.read_sql("select * from jobs", conn)
        
        # print(updated_df)

        # add new entries
        # delta_df = updated_df - database_df

        # update existing entries
        # cur.execute("update listjobs ")

    conn.close()


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def save_daemonstatus(file_path):
    '''
    Load status of a service.

    Supported Request Methods: GET

    '''
    url = "http://localhost:6800/daemonstatus.json"
    response = requests.get(url=url)
    
    # Save into json
    logging.info("Saving daemonstatus in JSON file...")
    with open(file_path, "w") as file:
        file.write(json.dumps(response.json(), indent=4))
    return 0

    # TODO: save into db

def add_to_schedule(spider_data):
    '''
    # Schedule:
    Schedule a spider run (also known as a job), returning the job id.
    
    Supported Request Methods: POST
    Parameters:
        project (string, required) - the project name
        spider (string, required) - the spider name
        setting (string, optional) - a Scrapy setting to use when running the spider
        jobid (string, optional) - a job id used to identify the job, overrides the default generated UUID
        priority (float, optional) - priority for this project’s spider queue — 0 by default
        _version (string, optional) - the version of the project to use
        any other parameter is passed as spider argument
    '''

    url = "http://127.0.0.1:6800/schedule.json"
    response = requests.post(url=url, params=spider_data)
    return response.text

if __name__ == "__main__":
    main()
