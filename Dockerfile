FROM quay.io/informaticslab/iris

MAINTAINER niall.robinson@informaticslab.co.uk

RUN git clone https://github.com/met-office-lab/cloud-processing-config.git config

ADD [^.]* ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ./scheduler.py
