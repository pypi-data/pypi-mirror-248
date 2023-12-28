from setuptools import setup

setup(
    name='geneplore_bare_api',
    version='3.6.0',
    install_requires=[
        'requests',
        'pandas',
        'google-api-python-client',
        'google-api-core',
        'python-dotenv',
        'boto3'
    ],
)