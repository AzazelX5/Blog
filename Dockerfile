FROM python:3.6.5
ENV PYTHON PYTHONUNBUFFERED 1
RUN mkdir /blog
WORKDIR /blog
ADD blog/requirements.txt /blog
RUN pip install -r requirements.txt
