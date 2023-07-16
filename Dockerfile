# syntax=docker/dockerfile:1
   
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install djitellopy opencv-python pygame
CMD ["python", "bt-server.py"]