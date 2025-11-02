FROM python:3.11-slim

# Create app directory
WORKDIR /app

# Install system deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY . /app

ENV PORT=8501
EXPOSE 8501

# Run Streamlit frontend by default. To run backend only, override CMD in deployment.
CMD ["streamlit", "run", "streamlit_frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]
