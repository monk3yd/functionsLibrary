import random

from stem import Signal
from stem.control import Controller
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware


def generate_session_proxy():
    username = "brd-customer-c_d98f5543-zone-zone1"
    password = "c1459bza97sy"
    port = 22225
    session_id = random.random()
    countries = ["cl"]
    # proxy_url = f"http://{username}-country-{countries[0]}-session-{session_id}:{password}@zproxy.lum-superproxy.io:{port}"
    proxy_url = f"http://{username}:{password}@zproxy.lum-superproxy.io:{port}"
    return proxy_url

class ProxyMiddleware(HttpProxyMiddleware):
    def process_response(self, request, response, spider):
        # Get a new identity depending on the response
        if response.status != 200:
            # new_tor_identity()
            return request
        return response

    def process_request(self, request, spider):
        # Set the Proxy
        # A new identity for each request
        # Comment out if you want to get a new Identity only through process_response
        request.meta["proxy"] = generate_session_proxy()  # Rotate proxy
        print(f"Autogenerate proxy {request.meta['proxy']} for url {request.url}")

        # request.meta["proxy"] = "http://brd-customer-c_d98f5543-zone-zone1:c1459bza97sy@zproxy.lum-superproxy.io:22225",  # General proxy

        # new_tor_identity()
        # request.meta['proxy'] = 'http://127.0.0.1:8118'  # Tor proxy


# def new_tor_identity():
#     with Controller.from_port(port=9051) as controller:
#         controller.authenticate(password='s2Q#x2Sk4CwfJV')
#         controller.signal(Signal.NEWNYM)