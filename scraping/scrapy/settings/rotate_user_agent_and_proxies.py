### User-Agent & Proxy Pool Rotation Configuration ###

DOWNLOADER_MIDDLEWARES = {
    # Own Proxy Middleware
    "project_name.middlewares.MiddlewareClass": 543,

    # Rotating User Agents
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,

    # Rotating Proxies
    'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
    'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
}

# Path to file with proxy urls, one line per url
ROTATING_PROXY_LIST_PATH = 'proxies.txt'

# Each element in list is a url
ROTATING_PROXY_LIST = []

# Retry with same url before rotate
ROTATING_PROXY_PAGE_RETRY_TIMES = 3

# --- Reference ---
# https://github.com/rejoiceinhope/crawler-demo/tree/master/crawling-basic/scrapy_user_agents
# https://pypi.org/project/scrapy-rotating-proxies/
