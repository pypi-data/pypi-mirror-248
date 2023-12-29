from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='RndTextGen',
  version='0.0.1',
  author='Lincoln Cox (Dmitry Vakhnenko)',
  author_email='just.kcgo@gmail.com',
  description='This is a python library for generating random text.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/LincolnCox29/Random-Text-Generator',
  packages=find_packages(),
  install_requires=[],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'Operating System :: OS Independent'
  ],
  keywords='Random Text',
  project_urls={
    'GitHub': 'https://github.com/LincolnCox29'
  },
  python_requires='>=3.11'
)