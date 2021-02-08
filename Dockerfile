FROM centos:7

RUN yum -y install epel-release && yum clean all
RUN yum -y install python-pip && yum clean all
RUN yum -y install unzip && yum clean all
RUN yum -y install xorg-x11-apps && yum clean all

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt


COPY server /
WORKDIR /


CMD ["gunicorn", "--timeout=180", "--workers=20", "--bind=0.0.0.0:80", "Server:app"]
