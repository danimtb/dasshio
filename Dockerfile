FROM armhf/python:3.6
MAINTAINER Julian Kahnert <mail@juliankahnert.de>

VOLUME /app
WORKDIR /app
COPY . .

# install dependencies
RUN apt-get update
RUN apt-get install -y \
    gcc \
    libnet1 \
    tcpdump

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "button.py"]
