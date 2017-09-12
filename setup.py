from setuptools import setup
setup(
    name='nsa',
    packages=['nsa'],
    include_package_data=True,
    install_requires=[
        'discord.py[voice]',
        'youtube_dl',
        'discord',
        'coinmarketcap==3.0',
    ],
)
