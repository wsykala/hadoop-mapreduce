FROM sequenceiq/hadoop-docker

RUN yum -y update
RUN yum -y install centos-release-scl
RUN yum -y install rh-python36

# Hack for python3 (thanks CentOS!)
RUN ln -s /opt/rh/rh-python36/root/usr/bin/python /usr/bin/python3

WORKDIR /mapreduce
COPY . .

# Make them executable so Hadoop does not complain (again because of lack of python3 on CentOS)
RUN chmod +x reducer.py
RUN chmod +x mapper.py

RUN python3 -m pip install -r requirements.txt