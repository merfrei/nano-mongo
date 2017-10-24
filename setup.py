from setuptools import setup

setup(name='nano-mongo',
      version='0.1.0',
      description='Utils to use MongoDB in Python based projects',
      url='http://github.com/merfrei/nano-mongo',
      author='Emiliano M. Rudenick',
      author_email='emr.frei@gmail.com',
      license='MIT',
      packages=['nano_mongo'],
      install_requires=[
          'pymongo',
      ],
      zip_safe=False)
