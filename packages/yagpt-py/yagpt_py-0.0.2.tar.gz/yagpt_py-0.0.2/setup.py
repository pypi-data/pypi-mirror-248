from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='yagpt_py',
  version='0.0.2',
  author='Danila Suravenkov',
  author_email='keepwannadie@gmail.com',
  description='alpha version of YandexGPT package for Python.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/Misfit-s/yagpt_py',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.12',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='files speedfiles AI GPT language model',
  project_urls={
    'GitHub': 'https://github.com/Misfit-s/yagpt_py'
  },
  python_requires='>=3.6'
)