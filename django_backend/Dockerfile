# Use an official Python runtime as a parent image
FROM python:3.11.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Copy requirements.txt and install Python dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project
COPY . /code/

# Expose port 8000
EXPOSE 8000