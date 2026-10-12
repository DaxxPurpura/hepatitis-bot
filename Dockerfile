FROM python:3.12-slim
WORKDIR /app
RUN useradd -m bot
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
USER bot
CMD ["python3", "main.py"]
