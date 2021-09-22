import io
import unittest
import urllib
from unittest import mock

from simple_http_client import Client, FormData

class MockException(urllib.error.HTTPError):
  def __init__(self, url, status):
    super(MockException, self).__init__(
        url, status, 'REASON', 'HEADERS', None
    )

  def getcode(self):
    return self.status

  def info(self):
    return 'ERROR HEADERS'

  def read(self):
    return 'ERROR BODY'

  @property
  def reason(self):
    return 'ERROR REASON'

class MockResponse(urllib.request.HTTPSHandler):

  def __init__(self, status, body):
    self.status = status
    self.body = body

  def getcode(self):
    return self.status

  def info(self):
    return 'HEADERS'

  def read(self):
    return self.body

class MockClient():

  def __init__(self, status=200):
    self._status = status
    self._body = 'RESPONSE BODY'

  def _urlopen(self, url, data=None, method='GET', headers=None):
    if self._status == 200 and 'Content-Type' in headers and 'multipart/form-data' in headers['Content-Type']:
      self._body = 'MULTIPART FORM DATA BODY'
      return MockResponse(self._status, self._body)
    if 200 <= self._status < 299:
      return MockResponse(self._status, self._body)
    else:
      self._body = 'ERROR RESPONSE BODY'
      raise MockException(self._status, self._body)

class TestClient(unittest.TestCase):

  def setUp(self):
    self.client = Client()

  def test__init__(self):
    url = 'hello'
    headers = {'X-Test': 'test', 'X-Test2': 2}
    client = Client(url, headers)
    self.assertEqual(client.url, url)
    self.assertEqual(client.headers, headers)

  def test__update_headers(self):
    headers = {'X-Test3': 'test3'}
    self.client._update_headers(headers)
    self.assertIn('X-Test3', self.client.headers)
    self.client.headers.pop('X-Test3', None)

  @mock.patch('simple_http_client.client.Client._urlopen')
  def test_request__get_200_ok(self, mock_urlopen):
    client = self.client

    mock_client = MockClient()
    mock_urlopen.side_effect = mock_client._urlopen

    r = client.request(url='hello')
    self.assertEqual(client.method, 'GET')
    self.assertEqual(r.status, 200)
    self.assertEqual(r.statusText, 'OK')
    self.assertEqual(r.body, 'RESPONSE BODY')
    self.assertEqual(r.headers, 'HEADERS')

    return

  @mock.patch('simple_http_client.client.Client._urlopen')
  def test_request__post_json_200_ok(self, mock_urlopen):
    client = self.client

    mock_client = MockClient()
    mock_urlopen.side_effect = mock_client._urlopen

    body = {'data': 'test'}
    r = client.request(url='hello', method='POST', body=body)
    self.assertEqual(client.method, 'POST')
    self.assertEqual(client.headers['Content-Type'], 'application/json')
    self.assertEqual(r.status, 200)
    self.assertEqual(r.statusText, 'OK')
    self.assertEqual(r.body, 'RESPONSE BODY')
    self.assertEqual(r.headers, 'HEADERS')

    return

  @mock.patch('simple_http_client.client.Client._urlopen')
  def test_request__post_multipart_200_ok(self, mock_urlopen):
    client = self.client

    form = FormData()
    form.add_file(
      'file', 'test.txt',
      fileHandle=io.BytesIO(b'Hello!'))
    mock_client = MockClient()
    mock_urlopen.side_effect = mock_client._urlopen

    r = client.request(url='hello', method='POST', body=form)
    self.assertEqual(client.method, 'POST')
    self.assertTrue('multipart/form-data' in client.headers['Content-Type'])
    self.assertEqual(r.status, 200)
    self.assertEqual(r.body, 'MULTIPART FORM DATA BODY')

    return

  @mock.patch('simple_http_client.client.Client._urlopen')
  def test_request__get_302_found(self, mock_urlopen):
    client = self.client

    mock_client = MockClient(status=302)
    mock_urlopen.side_effect = mock_client._urlopen

    with self.assertRaises(urllib.error.HTTPError):
      client.request('hello')

    return

  @mock.patch('simple_http_client.client.Client._urlopen')
  def test_request__get_404_not_found(self, mock_urlopen):
    client = self.client
    
    mock_client = MockClient(status=404)
    mock_urlopen.side_effect = mock_client._urlopen

    with self.assertRaises(urllib.error.HTTPError):
      client.request('hello')

    return

  @mock.patch('simple_http_client.client.Client._urlopen')
  def test_request__get_502_bad_gateway(self, mock_urlopen):
    client = self.client
    
    mock_client = MockClient(status=502)
    mock_urlopen.side_effect = mock_client._urlopen

    with self.assertRaises(urllib.error.HTTPError):
      client.request('hello')

    return

if __name__ == '__main__':
  unittest.main(verbosity=2)