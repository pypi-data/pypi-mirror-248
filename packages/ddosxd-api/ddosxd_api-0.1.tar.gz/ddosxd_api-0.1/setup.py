from setuptools import setup, find_packages

setup(
    name='ddosxd_api',
    version='0.1',
    description='ddosxd api client',
    author='ddosxd',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'requests',
        'httpx'
    ],
)
