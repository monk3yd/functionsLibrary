### Playwright ###

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

# --- General configurations: apply to all spiders ---


# Browser used for playwright requests
# Options (str): chromium (default), firefox, webkit
PLAYWRIGHT_BROWSER_TYPE = "firefox"

PLAYWRIGHT_CONTEXTS = {
    "default": {
        "viewport": {
            "width": 1920,
            "height": 1080,
        },
        "persistent": {
            "user_data_dir": "persistent/",  # will be a persistent context
        },
    }
}

PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 10000

PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": False,
    "channel": "firefox",
    "proxy": {
        "server": 'http://127.0.0.1:8118' 
    },
}

# --- For customized configuration per spider use custom_settings = {} ---
# spdier.py snippet example #
class BookiesSpider(scrapy.Spider):
    name = "spider_name"
    custom_settings = {
        "PLAYWRIGHT_CONTEXTS": {
            "default": {
                "viewport": {
                    "width": 1920,
                    "height": 1080,
                },
            }
        },
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "headless": False,
            "channel": "firefox",
            "proxy": {
                "server": 'http://127.0.0.1:8118'
            },
        },
    }

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
