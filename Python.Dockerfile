FROM python:3.10-alpine3.15

WORKDIR /home/tonconnector

RUN ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime

COPY . .

RUN python3 -m pip install --upgrade pip setuptools-scm wheel
RUN python3 -m pip install -r requirements.txt


CMD ["python3", "bot.py"]
