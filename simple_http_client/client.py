import io
import json
import logging
import mimetypes
import urllib.request
from urllib.error import HTTPError
import uuid

from .exceptions import handle_error
from .response import Response

logger = logging.getLogger(__name__)

class FormData(object):
  def __init__(self):
    self.form_fields = []
    self.files = []
    self.boundary = uuid.uuid4().hex.encode('utf-8')
    return

  def get_content_type(self):
    return 'multipart/form-data; boundary={}'.format(
      self.boundary.decode('utf-8'))

  def add_field(self, name, value):
    self.form_fields.append((name, value))

  def add_file(self, fieldname, filename, filedata,
              mimetype=None, content_disposition='form-data'):
    if mimetype is None:
      mimetype = (
        mimetypes.guess_type(filename)[0] or
        'application/octet-stream'
      )
    self.files.append((fieldname, filename, mimetype, filedata, content_disposition))
    return

  @staticmethod
  def _form_data(name):
    return ('Content-Disposition: form-data; '
      'name="{}"\r\n').format(name).encode('utf-8')

  @staticmethod
  def _attached_file(name, filename, content_disposition):
    return ('Content-Disposition: {}; '
      'name="{}"; filename="{}"\r\n').format(
        content_disposition, name, filename).encode('utf-8')

  @staticmethod
  def _content_type(ct):
    return 'Content-Type: {}\r\n'.format(ct).encode('utf-8')

  def __bytes__(self):
    buffer = io.BytesIO()
    boundary = b'--' + self.boundary + b'\r\n'

    for name, value in self.form_fields:
      buffer.write(boundary)
      buffer.write(self._form_data(name))
      buffer.write(b'\r\n')
      buffer.write(value.encode('utf-8'))
      buffer.write(b'\r\n')

    for f_name, filename, f_content_type, body, content_disposition in self.files:
      buffer.write(boundary)
      buffer.write(self._attached_file(f_name, filename, content_disposition))
      buffer.write(self._content_type(f_content_type))
      buffer.write(b'\r\n')
      buffer.write(body)
      buffer.write(b'\r\n')

    buffer.write(b'--' + self.boundary + b'--\r\n')
    return buffer.getvalue()

class Client(object):
  def __init__(self, url=None, headers=None):
    self.url = url
    self.headers = headers or {}
    self.method = 'GET'

  def _update_headers(self, headers):
    self.headers.update(headers)

  def _urlopen(self, url, data, headers, method):
    req = urllib.request.Request(url, data, headers, method)
    try:
      return urllib.request.urlopen(req)
    except HTTPError as e:
      exc = handle_error(e)
      exc.__cause__ = None
      logger.debug('{} Response: {} {}'.format(method, exc.status, exc.body))
      raise exc

  def request(self, url=None, method='GET', headers=None, body=None):
    self.method = method

    if url:
      self.url = url

    if headers:
      self._update_headers(headers)

    if 'User-Agent' not in self.headers:
      with open('../VERSION.txt') as f:
        version = f.read()
      self._update_headers({'User-Agent': 'simple_http_client/v{}'.format(version)})

    if body is None:
      data = None
    else:
      if type(body) == FormData:
        data = bytes(body)
        self.headers.setdefault(
          'Content-Type', body.get_content_type())
        self._update_headers({'Content-length': len(data)})
      elif 'Content-Type' in self.headers and \
          self.headers['Content-Type'] != \
          'application/json':
        data = body.encode('utf-8')
      else:
        self.headers.setdefault(
          'Content-Type', 'application/json')
        data = json.dumps(body).encode('utf-8')
    
    logger.debug('{} Request: {}'.format(self.method, self.url))
    logger.debug('Headers: {}'.format(self.headers))

    if data:
      logger.debug('Payload: {}'.format(data))

    response = Response(self._urlopen(self.url, data, headers=self.headers, method=self.method))

    logger.debug('{} Response: {} {}'.format(method, response.status, response.body))

    return response