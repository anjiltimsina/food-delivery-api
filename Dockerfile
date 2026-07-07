# Use official python image
FROM python:3.11-slim

# Set working directory insider container
WORKDIR /app

# Copy requirements first(for caching)
COPY requirements.txt .

#Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of teh code
COPY . .

# Expose port 8001
EXPOSE 8001

#Run the app
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
