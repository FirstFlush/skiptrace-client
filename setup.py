from setuptools import setup, find_packages

setup(
    name='webweaver-cli',
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
            'webweaver-cli=main:webweaver_cli',
        ],
    },
)
