FROM quay.io/informaticslab/iris

MAINTAINER niall.robinson@informaticslab.co.uk

RUN apt-get update \
  && apt-get -y install python-pip python-numpy python-scipy git

RUN git clone https://github.com/met-office-lab/cloud-processing-config.git config

ADD [^.]* ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN wget http://download.osgeo.org/proj/proj-4.8.0.tar.gz
RUN wget http://download.osgeo.org/proj/proj-datumgrid-1.5.tar.gz

RUN tar xzf proj-4.8.0.tar.gz
RUN tar xzf proj-datumgrid-1.5.tar.gz

RUN proj-4.8.0/configure 
RUN make
RUN make install 

RUN echo /usr/local/lib >> /etc/ld.so.conf
RUN ldconfig

CMD ./scheduler.py
