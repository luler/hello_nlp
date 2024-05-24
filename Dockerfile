FROM python:3.7

MAINTAINER 1207032539@qq.com

RUN apt update -y && apt install -y libgl1-mesa-dev

RUN pip install paddlepaddle==2.3.0 paddlenlp==2.3.0rc1 -i https://mirror.baidu.com/pypi/simple

COPY . /root/work

WORKDIR /root/work

RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

EXPOSE 5000

ENV PPNLP_HOME /root/work/paddlenlp

CMD ["python","app.py"]