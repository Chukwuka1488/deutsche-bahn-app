# Intentionally using an older Python image with vulnerabilities
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Intentional vulnerability: Running as root user
# Create database directory
RUN mkdir -p /app/data

# Expose port
EXPOSE 5000

# Intentional vulnerability: No health check defined
# Intentional vulnerability: Running as root without creating non-root user

# Run the application
CMD ["python", "app.py"]
