from setuptools import setup, find_packages

setup(
  name='evm_indexer',
  version='0.0.2',
  packages=find_packages(),
  description='EVM compatible blockchain indexer',
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  author='Omchain Foundation',
  author_email='info@omchain.io',
  url='https://github.com/OmchainFoundation/evm-indexer',
  license='LICENSE',
  install_requires=[
    'web3>=6.0.0',
    'requests>=2.22.0',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3.6',
    'License :: OSI Approved :: MIT License'
  ],
  python_requires='>=3.6'
)