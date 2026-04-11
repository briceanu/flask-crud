# Use official Python base image
FROM python:3.13

# Set working directory inside container
WORKDIR /app

# Copy only requirements first to leverage cache
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

# Copy the rest of the code
COPY . .

# Expose Flask port
EXPOSE 5000

ENV FLASK_APP=app.main
ENV FLASK_ENV=development