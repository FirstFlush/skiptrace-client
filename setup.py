from setuptools import setup, find_packages

setup(
    name='tracer',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'click',
        'pynacl',
        'termcolor',
        # ... other dependencies
    ],
    entry_points={
        'console_scripts': [
            'tracer=main:tracer',
        ],
    },
)
