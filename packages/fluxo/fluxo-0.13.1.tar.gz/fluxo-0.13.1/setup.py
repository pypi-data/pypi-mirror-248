from setuptools import setup, find_packages

setup(
    name='fluxo',
    version='0.13.1',
    packages=find_packages(),
    package_data={
        '': ['fluxo_server/assets/*'],
    },
)
