# Use official Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app files
COPY . .

# Add these lines to make sure CORS works
ENV FLASK_APP=main.py
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1

# Expose backend port
EXPOSE 5000

# Run the Flask app
CMD ["python", "main.py"]