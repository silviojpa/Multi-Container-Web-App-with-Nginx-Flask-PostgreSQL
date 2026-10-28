FROM python:3.10-slim
WORKDIR /app
RUN pip install flask psycopg2-binary
COPY . /app
EXPOSE 5000
CMD ["python", "app.py"]
