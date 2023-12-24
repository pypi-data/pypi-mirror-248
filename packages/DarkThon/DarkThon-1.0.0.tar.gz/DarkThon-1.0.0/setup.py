from setuptools import setup

setup(
    name='DarkThon',
    description='custom Telethon class for working with session on server',
    version='1.0.0',
    author_email='mihajlovic.aleksa@gmail.com',
    packages=['telebytes'],
    zip_safe=False,
    install_requires=[
        'telethon == 1.30.3',
        'requests'
    ]
)