FROM python:3-alpine
RUN mkdir -p /usr/app/
WORKDIR /usr/app/
COPY . .
RUN pip install -r requirements.txt
ENV BOT_TOKEN=""
ENV CHANNEL_ID=""
ENV BEFORE_MINUTES=""
ENV SLEEP_TIME=""
ENTRYPOINT ["python", "temp-chat-beta.py"]