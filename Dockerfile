FROM python:3.6-alpine
MAINTAINER Julian Kahnert <mail@juliankahnert.de>

VOLUME /usr/src/app
WORKDIR /usr/src/app

# install dependencies
RUN apt install libnet
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "button.py"]
