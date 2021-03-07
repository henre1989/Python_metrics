FROM python:3
WORKDIR /usr/src/app
RUN pip3 install prometheus_client && pip3 install paramiko
USER root
RUN mkdir /root/.ssh
COPY id_rsa /root/.ssh
RUN chmod 600 /root/.ssh/id_rsa
COPY metrics.py ./
CMD [ "python", "./metrics.py" ]