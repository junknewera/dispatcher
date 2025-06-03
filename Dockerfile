FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY etl/ etl/
COPY data/ data/
COPY scripts/ scripts/
CMD ["sh", "-c", "python etl/extract.py && python etl/transform.py && python etl/load.py"]