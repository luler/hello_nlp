FROM python:3.11-slim

MAINTAINER 1207032539@qq.com

RUN apt update -y && apt install -y libgl1-mesa-dev

WORKDIR /root/work

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /root/work

EXPOSE 5000

ENV PPNLP_HOME /root/work/paddlenlp

CMD ["python","app.py"]