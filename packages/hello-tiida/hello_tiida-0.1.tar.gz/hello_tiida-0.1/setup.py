from setuptools import setup, find_packages

setup(
    name='hello_tiida',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'hello_tiida=hello_tiida.main:hello_tiida',
        ],
    },
)
