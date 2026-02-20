# VULNERABILITY: Old base image
FROM python:3.8

# VULNERABILITY: Running as root
WORKDIR /app

# VULNERABILITY: No health check
COPY requirements.txt .
RUN pip install -r requirements.txt

# VULNERABILITY: Exposing debug mode
ENV FLASK_ENV=development
ENV FLASK_DEBUG=True

COPY . .

# VULNERABILITY: No resource limits
EXPOSE 5000

CMD ["python", "app.py"]
