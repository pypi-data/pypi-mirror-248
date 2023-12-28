from setuptools import setup, find_packages

VERSION = '1.0'

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(name="mcprotection-dashboard",
      version=VERSION,
      author='seuskaszeba',
      author_email='mcp@xyz.com',
      license='MIT',
      description='A simple library used in the mcprotection dashboard',
      packages=find_packages(),
      install_requires=['']
      )
