FROM python:2.7
ADD appendList.py /

COPY requirements.txt /requirements.txt

WORKDIR /

RUN pip install -r requirements.txt

CMD [ "python", "./appendList.py" ]