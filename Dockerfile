FROM python:3.11-slim

WORKDIR /app

# System dependencies for pyodbc
RUN apt-get update && apt-get install -y \
    gcc g++ unixodbc-dev curl gnupg2 apt-transport-https \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY 03_Python_Analysis/ ./03_Python_Analysis/
COPY 04_Streamlit/       ./04_Streamlit/
COPY data/               ./data/
COPY 06_Logs/            ./06_Logs/

EXPOSE 8501

# Streamlit must listen on 0.0.0.0 inside a container
CMD ["streamlit", "run", "04_Streamlit/app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--browser.gatherUsageStats=false"]