FROM sequenceiq/hadoop-docker

RUN yum -y update ; yum clean all
RUN yum -y install centos-release-scl ; yum clean all
RUN yum -y install rh-python36 ; yum clean all
RUN yum -y install vixie-cron ; yum clean all

# Hack for python3 (thanks CentOS!)
RUN ln -s /opt/rh/rh-python36/root/usr/bin/python /usr/bin/python3

WORKDIR /mapreduce
COPY . .

# Crontab daemon fix
RUN mv bootstrap.sh /etc/
RUN chmod 700 /etc/bootstrap.sh
RUN crontab cronfile

# Make them executable so Hadoop does not complain (again because of lack of python3 on CentOS)
RUN chmod +x reducer.py
RUN chmod +x mapper.py

RUN python3 -m pip install -r requirements.txt
