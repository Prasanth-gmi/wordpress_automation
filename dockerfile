# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
COPY main01.py /app/
COPY client.py /app/
COPY tasks.py /app/
COPY agents.py /app/
COPY tools /app/tools/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/
# Set environment variables
ENV WORDPRESS_USER=""
ENV WORDPRESS_PASSWORD=""
ENV WORDPRESS_SITE_URL=""

# Expose the port the application runs on
EXPOSE 8000 5001 5002

# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "main01:app", "--host", "0.0.0.0", "--port", "8000"]   


