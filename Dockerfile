FROM openjdk:8-jdk-slim

RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*
RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install  -r requirements.txt

COPY src/ /app/src/
COPY features/ /app/features/
COPY data/data.csv /app/data/data.csv


COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh
RUN useradd -m devopuser
USER devopuser

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["app"]
