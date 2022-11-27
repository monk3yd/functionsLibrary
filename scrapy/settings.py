# Scrapy settings for bookies_odds project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "bookies_odds"

SPIDER_MODULES = ["bookies_odds.spiders"]
NEWSPIDER_MODULE = "bookies_odds.spiders"


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

#### Headers ####

#### Cookies ####
# Disable cookies (enabled by default)
COOKIES_ENABLED = False

### Handlers ####
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # "bookies_odds.middlewares.ProxyMiddleware.ProxyMiddleware": 543,

    ## Rotating User Agents
    # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    # 'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,

    ## Rotating Free Proxies
    # 'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
    # 'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
}

#### Proxies ####
# https://pypi.org/project/scrapy-rotating-proxies/
ROTATING_PROXY_LIST_PATH = 'proxies.txt'

# ROTATING_PROXY_LIST = [
#     ""
# ]

ROTATING_PROXY_PAGE_RETRY_TIMES = 3


#### Playwright ####
# Browser use for playwright request.
# Options (str): chromium (default), firefox, webkit
PLAYWRIGHT_BROWSER_TYPE = "firefox"

PLAYWRIGHT_CONTEXTS = {
    "persistent": {
        "user_data_dir": "persistent/",  # will be a persistent context
    },
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# The integer values determine the order in which the item is run through the
# pipelines. It is customary to define these number in the 0-1000 range.
ITEM_PIPELINES = {
   'chocolatescraper.pipelines.PriceToUSDPipeline': 100,
   'chocolatescraper.pipelines.DuplicatesPipeline': 200,
}

#### Requests delay & concurrencies ####
# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# Autothrottle (respect): the minimum download delay.
DOWNLOAD_DELAY = 3

# Autothrottle (respect): the max concurrency (requests) limit
# download delay will  honor only one:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

#### AutoThrottle extension ####
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True

# The initial download delay
AUTOTHROTTLE_START_DELAY = 5

# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60

# The average number of requests Scrapy should be sending in parallel to
# each remote server. Desired concurrency the crawler try to approach.
# Not a hard limit.
AUTOTHROTTLE_TARGET_CONCURRENCY = 5.0

# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

#### Logs ####
LOG_ENABLED = True
LOG_FILE_APPEND = False
LOG_LEVEL = "DEBUG"


#### Cache ####
# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = False
# HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"


#### Archives ####
# Configure maximum concurrent requests performed by Scrapy (default: 16)
# Disable whe using autothrottle, replaced by AUTOTHROTTLE_TARGET_CONCURRENCY
# CONCURRENT_REQUESTS = 5

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'bookies_odds.middlewares.BookiesOddsSpiderMiddleware': 543,
# }


# Whether or not to fail on broken responses. Up to the user to decide if it
# makes sense to process broken responses considering they may contain partial or incomplete content.
# Managed with errcallback func
# DOWNLOAD_FAIL_ON_DATALOSS = False

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'pjud_scraper (+http://www.yourdomain.com)'
# USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; rv:100.0) Gecko/20100101 Firefox/100.0"

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Accept-Language": "en-US,en;q=0.5",
#     "Connection": "keep-alive",
#     "DNT": "1",
#     "Referer": "https://google.com",
#     "Sec-Fetch-Dest": "document",
#     "Sec-Fetch-Mode": "navigate",
#     "Sec-Fetch-Site": "none",
#     "Sec-Fetch-User": "?1",
#     "Upgrade-Insecure-Requests": "1",
   #  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:100.0) Gecko/20100101 Firefox/100.0",
# }
