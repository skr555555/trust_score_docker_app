
FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y curl nmap && \
    pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
