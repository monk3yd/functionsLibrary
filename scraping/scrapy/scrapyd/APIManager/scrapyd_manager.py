from ScrapydAPIManager import ScrapydAPIManager
def main():
    service = "listjobs"
    manager = ScrapydAPIManager()
    manager.connect_to_scrapyd(service=service)
    

if __name__ == "__main__":
    main()