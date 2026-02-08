FROM apache/airflow:3.1.7

# Copy requirements.txt and install packages
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
