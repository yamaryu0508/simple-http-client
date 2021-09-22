import json

class Response(object):
  def __init__(self, response):
    self._status = response.getcode()
    self._statusText = 'OK'
    self._body = response.read()
    self._headers = response.info()

  @property
  def status(self):
    return self._status

  @property
  def statusText(self):
    return self._statusText

  @property
  def body(self):
    return self._body

  @property
  def headers(self):
    return self._headers

  @property
  def to_dict(self):
    if self._body:
      return json.loads(self._body.decode('utf-8'))
    else:
      return None