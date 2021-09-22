import json

class HTTPError(Exception):
  def __init__(self, *error):
    if len(error) == 4:
      self._status = error[0]
      self._statusText = error[1]
      self._body = error[2]
      self._headers = error[3]
    else:
      self._status = error[0].getcode()
      self._statusText = error[0].reason
      self._body = error[0].read()
      self._headers = error[0].info()

  def __reduce__(self):
    return (
      HTTPError,
      (self._status, self._statusText, self._body, self._headers)
    )

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
    return json.loads(self._body.decode('utf-8'))

class URLError(Exception):
  def __init__(self, error):
    self._status = None
    self._statusText = None
    self._body = error.reason
    self._headers = None

  def __reduce__(self):
    return (
      URLError,
      (self._status, self._statusText, self._body, self._headers)
    )

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

def handle_error(error):
  return HTTPError(error)
