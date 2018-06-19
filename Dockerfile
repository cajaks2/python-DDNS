FROM ubuntu:16.04
RUN apt-get update; apt-get install python3 python-dev python3-dev \
     build-essential libssl-dev libffi-dev \
     libxml2-dev libxslt1-dev zlib1g-dev libcurl4-openssl-dev \
     python-pip -y
RUN pip install pycurl dnspython
ADD main.conf /opt/main.conf
ADD namecheap.py /opt/
CMD ["python", "/opt/namecheap.py"]