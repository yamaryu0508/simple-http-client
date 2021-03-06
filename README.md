# Simple HTTP Client for Python

## Installation

### Prerequisites
- Python version 3.7+

### Install Package
```
pip install git+https://github.com/yamaryu0508/simple-http-client
```

## Quick Start
Here is a quick example:
```python
# Example#1 Access to Google web site
from simple_http_client import Client
client = Client()

url = 'https://www.google.com/'
response = client.request(url)
print(response.body)
```

```python
# Example#2 Access to Kintone
import base64, os, urllib.parse
from simple_http_client import Client, FormData, HTTPError

client = Client()

BASE_URL = os.environ.get('KINTONE_BASE_URL') # https://example.kintone.com
AUTH_TOKEN = base64.b64encode((
  '{}:{}'.format(
    os.environ.get('KINTONE_USERNAME'),
    os.environ.get('KINTONE_PASSWORD')
  )
).encode()).decode()

APP = 60465

url = '{}/k/v1/record.json'.format(BASE_URL)

body = {
  'app': APP,
  'record': {
    'Test': {
      'value': 'test'
    }
  }
}

try:
  response = client.request(
    url,
    method='POST',
    headers={
      'X-Cybozu-Authorization': AUTH_TOKEN
    }
    body=body
  )
  print(response.status)
  print(response.headers)
  print(response.body)
  print(response.to_dict)
except HTTPError as e:
  print(e.to_dict)
```
### HTTP client - `simple_http_client.Client.request`
This method requires parameters bellow.

`simple_http_client.Client.request(url=None, method='GET', headers=None, body=None)`

- url (required): should be string
- method: should be string (`GET`, `POST`, `PUT`, `DELETE`, `PATCH`)
- headers: should be dictionary
- body: should be string, dictionary (JSON) or `FormData`

### Response class
Response class contains attributes bellow.
- status: stauts code
- statusText: `OK`
- body: response body
- headers: response headers
- to_dict: dictionary of response body

### Exception class
Exception class contains attributes bellow.
- status: stauts code
- statusText: exception reason (`Bad Request`, etc.)
- body: response body
- headers: response headers
- to_dict: dictionary of response body

## Usage
- [Example Code](https://github.com/yamaryu0508/simple-http-client/tree/main/examples)

## License
[The MIT License (MIT)](https://github.com/yamaryu0508/simple-http-client/blob/main/LICENSE)