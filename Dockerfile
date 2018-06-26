FROM python:3.6
WORKDIR /app
ADD requirements.txt /app/requirements.txt
RUN wget "http://ftp.us.debian.org/debian/pool/main/o/opus/libopus0_1.1-2_amd64.deb" && dpkg -i "libopus0_1.1-2_amd64.deb"
RUN pip install -r requirements.txt
COPY . /app
CMD python3 -m nsabot