from setuptools import setup

setup(
  name='perfomance_log',
  version='1.0.1',
  description='Perfomance logging',
  author='Alex Yung',
  packages=['perfomance_logging'],
  zip_safe=False,
  install_requires=[
    'structlog',
  ],
  package_data={'': ['perfomance_logging.pyd']},
  include_package_data = True,
)