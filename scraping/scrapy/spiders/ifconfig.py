### Check actual IP Address ###

import scrapy


class IfconfigSpider(scrapy.Spider):
    name = 'ifconfig'
    allowed_domains = ['ifconfig.me']
    start_urls = ['http://ifconfig.me/']

    def parse(self, response):
        self.log(f"IP : {response.css('#ip_address').get()}")


# --- Reference ---
# https://www.khalidalnajjar.com/stealthy-crawling-using-scrapy-tor-and-privoxy/
