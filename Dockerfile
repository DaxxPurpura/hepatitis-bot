FROM python:3.12-slim
RUN useradd -m bot
WORKDIR /app
RUN chown bot:bot /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=bot:bot . .
USER bot
CMD ["python3", "main.py"]
