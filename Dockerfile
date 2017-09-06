FROM centos/python-35-centos7

USER root

RUN yum install opus -y && \
    yum install epel-release -y && \
    rpm --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro && \
    rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm && \
    yum install ffmpeg -y

USER 1001