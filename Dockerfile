FROM alpine:latest

RUN apk update && \
    apk add python3 && \
    apk add py3-pip && \
    pip3 install --upgrade pip

WORKDIR /usr/mirrorbot
COPY . .

RUN pip3 install -r requirements.txt

CMD [ "python3", "main.py" ]                                                                                                      1,13          All