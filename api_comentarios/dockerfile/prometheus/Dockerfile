# Prometheus container
FROM prom/prometheus as prometheus
COPY prometheus.yml /etc/prometheus/

# App container
FROM python:3.9 as app
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
