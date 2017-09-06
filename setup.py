from setuptools import setup
setup(
    name='nsa',
    packages=['nsa'],
    include_package_data=True,
    install_requires=[
        'discord.py[voice]',
        'youtube_dl',
        'discord',
        'coinmarketcap',
        'PySocks',
        'PyNaCl',
        'google-auth-oauthlib[tool]',
        'google-assistant-sdk'
    ],
)
