# discord-nsa-bot

Bot does the needful


## Setup

``python ./setup.py``

``export DISCORD_API_TOKEN=<YOUR API TOKEN>``

## Run

``python ./app.py``

# Optional setup

This bot can run in openshift if you create an S2I build and use quay.io/jtcressy/discord-nsa-bot as a build image.

I will probably tweak the build pipeline on quay.io to build separate images at some point.

# Soon<sup>tm</sup>

I plan to have an ``:onbuild`` tag that is just a ``centos/python-35-centos7`` image with some necessary RPM's to get
opus to work for voice client stuff. This would be the builder image for use on an OpenShift build config.

The ``:latest`` tag will be a fully installed bot so that you should be able to do

``docker run -dit -e DISCORD_API_TOKEN=<api token> quay.io/jtcressy/discord-nsa-bot``

to run the bot inside a normal container.
