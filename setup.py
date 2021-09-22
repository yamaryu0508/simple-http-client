import os
from setuptools import setup, find_packages

with open('README.md') as f:
  readme = f.read()

with open('VERSION.txt') as f:
  version = f.read()

with open('LICENSE') as f:
  license = f.read()

def read_requirements():
  """Parse requirements from requirements.txt."""
  reqs_path = os.path.join('.', 'requirements.txt')
  with open(reqs_path, 'r') as f:
    requirements = [line.rstrip() for line in f]
  return requirements

setup(
  name='simple_http_client',
  version=version,
  description='Simple HTTP REST client for Python',
  long_description_content_type='text/markdown',
  long_description=readme,
  author='Ryu Yamashita',
  author_email='yamaryu0508@yahoo.co.jp',
  url='https://github.com/yamaryu0508/simple-http-client',
  install_requires=read_requirements(),
  license=license,
  packages=['simple_http_client'],
  python_requires='!=2.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*',
  classifiers=[]
)