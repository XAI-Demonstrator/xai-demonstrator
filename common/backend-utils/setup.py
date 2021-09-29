from setuptools import setup

setup(name='xaidemo',
      description='Shared utilities for XAI Demonstrator backends',
      url='http://github.com/xai-demonstrator/xai-demonstrator',
      author='The XAI Demonstrator team',
      author_email='xai.demonstrator@gmail.com',
      license='Apache 2.0',
      packages=['xaidemo'],
      install_requires=[
          'aiofiles==0.7.0',
          'opentelemetry-api==1.5.0',
          'opentelemetry-sdk==1.5.0',
          'opentelemetry-instrumentation-fastapi',
          'opentelemetry-exporter-jaeger==1.5.0',
          'opentelemetry-exporter-gcp-trace==1.0.0',
          'opentelemetry-propagator-gcp==1.0.0',
          'fastapi',
          'pydantic'
      ],
      zip_safe=False)
