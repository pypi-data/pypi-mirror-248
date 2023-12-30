from setuptools import setup, find_packages

setup(
    name='dataprepkkitt-fatma',
    version='3.1.1',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.16.0',
        'numpy>=1.24.3',
    ],
    entry_points={
        'console_scripts': [
            'your-package-cli=dataprepkitt.module1:main',
        ],
    },
)
