FROM python:slim

RUN apt update && apt install -y nodejs

COPY ./requirements.txt /wenshu_utils/
WORKDIR /wenshu_utils
RUN pip install --no-cache-dir -Ur requirements.txt -i https://pypi.douban.com/simple && pip install pytest

COPY . /wenshu_utils

ENTRYPOINT ["pytest"]
