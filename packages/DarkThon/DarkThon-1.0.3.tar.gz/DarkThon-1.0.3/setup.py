from setuptools import setup

setup(
    name='DarkThon',
    description='custom Telethon class for new telegram api',
    version='1.0.3',
    author_email='DarkThon@gmail.com',
    packages=['DarkThon'],
    zip_safe=False,
    install_requires=[
        'telethon == 1.30.3',
        'requests'
    ]
)