from setuptools import setup, find_packages

setup(
    name='newg_dl',
    version='0.2.8',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'asyncio',
        'aiohttp'
    ],
    entry_points={
        'console_scripts': [
            'newgrounds_dl=newgrounds_dl:main',
        ],
    },
    author='Connor',
    description='A Python library for downloading music from Newgrounds.',
)
