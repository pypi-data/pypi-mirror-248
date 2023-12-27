from setuptools import find_packages, setup

setup(
    name='iotiumscraper',
    packages=find_packages(),
    version='0.2.2',
    description='scrape data from kastle and push to postgres',
    author='Raja',
    install_requires=[
        'selenium ',
        'chromedriver_py',
        'email',
        'imaplib',
        'psycopg2'
    ]
)
