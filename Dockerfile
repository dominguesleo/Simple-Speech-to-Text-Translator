#syntax=docker/dockerfile:1
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt main.py ./
RUN pip install gradio whisper translate gtts
EXPOSE 7861
CMD python main.py