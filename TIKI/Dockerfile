FROM python:3.12

RUN apt-get update && apt-get install -y wget unzip curl gnupg ca-certificates \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./src /app
COPY requirements.txt /app

RUN pip install --upgrade pip && pip install -r requirements.txt 
CMD ["python", "/app/index.py"]
