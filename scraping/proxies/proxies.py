# Brightdata generate proxies

def generate_session_proxy(code):
    username = "brd-customer-hl_xxxxxxx-zone-data_center"
    session_id = random()  # random between 0 - 1
    password = "rb9601f3ildw"
    port = 22225

    # proxy_url = f"http://{username}:{password}@zproxy.lum-superproxy.io:{port}"  # General
    proxy_url = f"http://{username}-country-{code}-session-{session_id}:{password}@zproxy.lum-superproxy.io:{port}"

    return proxy_url

def generate_proxies():
    NUM_OF_PROXIES = 3000
    # Read countries
    # with open("data.json", "r") as file:
    #     data = list(map(json.loads, file))[0]

    codes = ["cl", "pe", "de", "us", "ar", "at", "ca", "cz", "fi", "hu", "in", "nz", "gb", "uy", "pl", "br"]  # list with all country codes
    # for country in data:
    #     codes.append(country["Code"].lower())

    proxies = []
    for _ in range(NUM_OF_PROXIES):  # Number of wanted proxies
        random_country_code = choice(codes)
        proxies.append(generate_session_proxy(code=random_country_code))

    # Remove duplicate proxy urls
    proxies = list(dict.fromkeys(proxies))

    proxies_path = "proxy-list.txt"
    if os.path.exists(proxies_path):
        os.remove(proxies_path)

    # Save proxy urls to file
    with open(proxies_path, "a") as file:
        for proxy in proxies:
            file.write(f"{proxy}\n")

    return proxies


def get_id_tables_map(process, path: Path):
    # Execute only if constructor doesn't exist
    if not path.exists():
        process.crawl("dev_constructor")
        process.start()

    # Read constructor data
    with open(path) as file:
        id_tables_map = json.load(file)

    return id_tables_map

