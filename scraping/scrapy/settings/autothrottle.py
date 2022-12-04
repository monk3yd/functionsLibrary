### Requests delay & concurrencies ###

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# Autothrottle (respect): the minimum download delay.
DOWNLOAD_DELAY = 3

# Autothrottle (respect): the max concurrency (requests) hard limit
# download delay will honor only one:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# --- AutoThrottle extension --- 
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
