import requests
import httpx

headers = "Mozilla/5.0 (X11; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0"
url = "https://httpbin.org/headers"

### Synchronous

## No sessions

# requests
response = requests.get(url, headers=headers)
print(response.text)

# httpx
response = httpx.get(url, headers=headers)
print(response.text)

## Sessions

# requests
with requests.Session() as session:
    response = session.get(url, headers=headers)
    print(response.text)

# httpx
with httpx.Client() as client:
    response = client.get(url, headers=headers)
    print(response.text)

### Asynchronous
## Session
# httpx
async with httpx.AsyncClient() as client:
    response = await client.get(url, headers=headers)
    print(response.text)
