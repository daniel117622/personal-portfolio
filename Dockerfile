FROM python:3.11-slim

# Set environment variables to prevent python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the local project files into the container
COPY . /app

# Install Flask, Uvicorn, and the WSGI-to-ASGI adapter
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Uvicorn will run on
EXPOSE 8000

# Command to run the application using Uvicorn
CMD ["uvicorn", "asgi:asgi_app", "--host", "0.0.0.0", "--port", "8000"]