from setuptools import find_packages, setup

setup(
    name='iotiumscraper',
    packages=find_packages(),
    version='0.2.3',
    description='scrape data from kastle and push to postgres',
    author='Raja',
    install_requires=[
        'selenium ',
        'chromedriver_py',
        'psycopg2'
    ]
)
