from setuptools import setup, find_packages


setup(
    name='bughunter9',
    version='9.13',
    py_modules=['bughunter9'],
    install_requires=[
        'colored==1.4.4',
        'colorama==0.4.6',
        'ipaddress==1.0.23',
        'requests==2.26.0',
        'beautifulsoup4==4.10.0',
        'tqdm==4.62.3',
        'termcolor==1.1.0',
        'retry==0.9.2',
        'bs4==0.0.1',
        'ipcalc',
        'emoji',
        'dnspython',

        # Add other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'bughunter9 = bughunter9:main'
        ]
    },
)
