FROM python:3.9-slim
RUN apt update -y
RUN pip install flask
RUN pip install pytube
#WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
