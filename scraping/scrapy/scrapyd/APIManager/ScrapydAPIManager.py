import json
import logging
import os
import pandas as pd
import requests
import sqlite3
import sys
import time

from pathlib import Path


class ScrapydAPIManager:
    # Scrapyd's API Manager
    # https://scrapyd.readthedocs.io/en/latest/api.html

    def __init__(self):
        # logging: debug info warning error critical
        logging.basicConfig(level=logging.DEBUG)
        logging.info("Initialize Scrapyd's API Manager")

        self.SLEEP_TIME = 180
        logging.info(f"SLEEP_TIME_IN_SECONDS: {self.SLEEP_TIME}")

        self.LISTJOBS_PATH = Path("services/listjobs.json")
        logging.info(f"LISTJOBS_FILE_PATH: {self.LISTJOBS_PATH}")

        self.DAEMONSTATUS_PATH = Path("services/daemonstatus.json")
        logging.info(f"DAEMONSTATUS_FILE_PATH: {self.DAEMONSTATUS_PATH}")

        self.DATABASE_PATH = Path("../dbs/listjobs")
        logging.info(f"DATABASE_PATH: {self.DATABASE_PATH}")

    
    def connect_to_scrapyd(self, service):
        logging.info("Connecting to scrapyd server...")

        # --- ListJobs ---
        if service == "listjobs":
            logging.info("Starting listjobs service...")
            while True:
                self.start_listjobs_service()
                
                logging.info(f"Time left for next server status report: {self.SLEEP_TIME} seconds...\n")
                time.sleep(self.SLEEP_TIME)
    
    def start_listjobs_service(self):
        '''
        Get the list of pending, running and finished jobs of some project.

        Supported Request Methods: GET
        Parameters:
            project (string, option) - restrict results to project name
        '''

        logging.info("Connecting to listjobs service...")
        URL = "http://127.0.0.1:6800/listjobs.json"
        response = requests.get(url=URL)

        # Update listjobs JSON file
        logging.info("Create/Update listjobs JSON file...")
        with open(self.LISTJOBS_PATH, "w") as file:
            file.write(json.dumps(response.json(), indent=4))

        # Read updated data from listjobs
        logging.info("Reading listjobs data...")
        with open(self.LISTJOBS_PATH, "r") as file:
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
            status = "finished"
            finished_df = pd.DataFrame(finished_jobs)
            
            logging.info("Updating database...")
            self.update_database(finished_df, status)
        
        # Jobs almost finished
        if not pending_jobs and running_jobs and finished_jobs:
            logging.info("Jobs almost finished...")
            status = "almost finished"
            running_df = pd.DataFrame(running_jobs)
            finished_df = pd.DataFrame(finished_jobs)
            
            # Merge
            # merged_df = finished_df.merge(running_df, how="outer")

            # Save to db
            # update_database(merged_df)
        
        # Jobs are stale (not scraping)
        if pending_jobs and not running_jobs and finished_jobs:
            logging.warning("Jobs are stale (not scraping)...")
            status = "stale"
            pending_df = pd.DataFrame(pending_jobs)
            finished_df = pd.DataFrame(finished_jobs)
            
            # Merge
            # merged_df = finished_df.merge(pending_df, how="outer")

            # Save to db
            # update_database(merged_df)
        
        # Scraping jobs
        if pending_jobs and running_jobs and finished_jobs:
            logging.info("Scraping...!")
            status = "scraping"
            pending_df = pd.DataFrame(pending_jobs)
            running_df = pd.DataFrame(running_jobs)
            finished_df = pd.DataFrame(finished_jobs)
            
            # Merge dataframes
            new_df = finished_df.merge(running_df, how="outer").merge(pending_df, how="outer")

            self.update_database(new_df, status)
    
    def update_database(self, updated_df=None, service_status=None):
        if service_status == "finished":
            max_uid = max(updated_df.index)
            logging.info(f"Creating/updating listjobs database at {self.DATABASE_PATH}_{max_uid}")

            logging.info("Connecting to database...")
            conn = self.create_connection(f"{self.DATABASE_PATH}_{max_uid}.db")
            if conn is None:
                logging.error("Could not establish connection with database...")

            # create db
            logging.info("Creating jobs table...")
            updated_df.to_sql(name="jobs", con=conn)
            conn.close()

        # except ValueError as err:
        #     logging.error(f"{err} Trying to read database instead...")

            # read db into dataframe
            # database_df = pd.read_sql("SELECT * FROM jobs", conn)

            # cur = conn.cursor()
            # Create tmp table
            # updated_df.to_sql("tmp", conn, if_exists="replace")

            # Update tmp table
            # cur.execute("UPDATE jobs SET jobs.start_time = tmp.start_time, jobs.end_time = tmp.end_time, jobs.pid = tmp.pid WHERE jobs.id IN (SELECT tmp.id FROM tmp);")

            # conn.commit()

            # c.execute("INSERT INTO jobs ([key], project, spider, id, start_time, end_time) " + \
            #           "SELECT [key], project, spider, id, start_time, end_time " + \
            #           "FROM tmp t " + \
            #           "WHERE NOT EXISTS " + \
            #           "   (SELECT 1 FROM jobs sub " + \
            #           "    WHERE sub.[key] = t.[key]);")
            # conn.commit()

    
    # --- Utilities ---    
    def create_connection(self, db_file):
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