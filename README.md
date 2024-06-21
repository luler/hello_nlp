# PaddleNLP一键预测功能转接口调用

## 安装

```
git clone https://github.com/luler/hello_nlp.git

pip install -r requirements.txt
```
docker-compose一键启动
``` 
version: "3"

services:
  hello_nlp:
    image: registry.cn-shenzhen.aliyuncs.com/luler/hello_nlp
    restart: always
    ports:
      - 5000:5000
    volumes:
      - ./:/root/work
```

## 运行

``` 
python app.py
```
或者
``` 
docker-compose up -d
```

## 相关接口

参考：https://github.com/luler/hello_nlp/blob/master/taskflow.md

`POST` /api/pos_tagging

`POST` /api/word_segmentation

`POST` /api/ner

`POST` /api/dependency_parsing

`POST` /api/information_extraction

`POST` /api/knowledge_mining

`POST` /api/text_correction

`POST` /api/text_similarity

`POST` /api/sentiment_analysis

`POST` /api/question_answering

`POST` /api/poetry_generation

`POST` /api/dialogue