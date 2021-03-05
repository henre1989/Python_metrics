FROM python:3
WORKDIR /usr/src/app
#COPY requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip3 install prometheus_client
COPY metrics.py ./
#EXPOSE 8001
CMD [ "python", "./metrics.py" ]