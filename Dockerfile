FROM nikolaik/python-nodejs:python3.10-nodejs20-slim

RUN apt-key adv --refresh-keys --keyserver keyserver.ubuntu.com
RUN apt-get update -y
RUN apt-get -y install build-essential sudo postgresql libpq-dev postgresql-client curl \
    postgresql-client-common libncurses5-dev libjpeg-dev zlib1g-dev git wget redis-server && \
    wget -O /usr/local/bin/wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/8ed92e8cab83cfed76ff012ed4a36cef74b28096/wait-for-it.sh && \
    chmod +x /usr/local/bin/wait-for-it.sh

RUN pip install --upgrade pip
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./frontend/package*.json /code/frontend/
RUN npm install --prefix /code/frontend
RUN npm install --global serve vite

COPY . /code
WORKDIR /code
RUN cd /code/frontend && npm run build

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

ENTRYPOINT [ "sh", "entrypoint.sh" ]
