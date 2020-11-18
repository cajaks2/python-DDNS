ARG ARCH=
FROM ${ARCH}python:alpine
RUN pip install requests dnspython ipaddr
ADD main.conf /opt/main.conf
ADD namecheap.py /opt/
CMD ["python", "/opt/namecheap.py"]
