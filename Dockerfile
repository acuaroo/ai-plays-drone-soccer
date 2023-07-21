# syntax=docker/dockerfile:1
   
FROM python:3.9
WORKDIR /app
COPY . .
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx
RUN pip install djitellopy opencv-python pygame

CMD ["python", "bt-server.py"]

EXPOSE 8889/udp
EXPOSE 8890/udp
EXPOSE 11111/udp