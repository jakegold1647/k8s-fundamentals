FROM python:3.11-slim

WORKDIR /app

# library install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the code
COPY main.py .

EXPOSE 8080

# start it up
CMD ["python", "main.py"]