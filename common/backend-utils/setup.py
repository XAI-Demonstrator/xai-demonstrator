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
          'opentelemetry-api==0.17b0',
          'opentelemetry-sdk==0.17b0',
          'opentelemetry-instrumentation-fastapi==0.17b0',
          'opentelemetry-exporter-jaeger==0.17b0',
          'opentelemetry-exporter-google-cloud==0.17b0',
          'opentelemetry-tools-google-cloud==0.17b0',
          'fastapi',
          'pydantic'
      ],
      zip_safe=False)
