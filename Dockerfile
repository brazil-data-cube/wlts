FROM python:3.7

RUN apt-get update && apt-get install -y build-essential git vim \
    && rm -rf /var/lib/apt/lists/*

ADD . /wlts

WORKDIR /wlts

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN pip3 install --upgrade pip && \
    pip install --upgrade setuptools && \
    pip install --upgrade wheel

RUN pip install -e .[all]
RUN pip install gunicorn

EXPOSE 5000

CMD ["gunicorn", "-w4", "--bind=0.0.0.0:5000", "wlts:app", "--timeout", "350"]