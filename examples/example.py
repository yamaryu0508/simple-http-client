import base64
import logging
import os
from simple_http_client import Client, FormData, HTTPError
import urllib.parse

logging.basicConfig(level=logging.ERROR)
logging.getLogger('simple_http_client').setLevel(level=logging.DEBUG)

client = Client()

BASE_URL = os.environ.get('KINTONE_BASE_URL')
AUTH_TOKEN = base64.b64encode((
  '{}:{}'.format(
    os.environ.get('KINTONE_USERNAME'),
    os.environ.get('KINTONE_PASSWORD')
  )
).encode()).decode()

APP = 894

url = '{}/k/v1/records.json?{}'.format(
  BASE_URL,
  urllib.parse.urlencode({
    'app': APP,
    'query': 'limit 1',
    'fields[0]': '$id',
    'totalCount': 'true'
  })
)
print(url)
try:
  response = client.request(url, headers={
    'X-Cybozu-Authorization': AUTH_TOKEN
  })
  print(response.to_dict)
except HTTPError as e:
  print(e.to_dict)