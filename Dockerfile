FROM python:alpine
RUN apk add --no-cache python3   
RUN pip install influxdb requests dnspython
ADD main.conf /opt/main.conf
ADD namecheap.py /opt/
CMD ["python", "/opt/namecheap.py"]