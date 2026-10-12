# ==========================================
# Stage 1: Compile TypeScript (Node context)
# ==========================================
FROM node:20-slim AS frontend-builder

WORKDIR /build

# Install typescript globally for the build step
RUN npm install -g typescript

# Copy the TypeScript source into the builder
COPY static/ts/ ./static/ts/

# Compile the TypeScript file (creates /build/static/ts/calendar.js)
RUN tsc static/ts/calendar.ts

# Move and rename the output so Stage 2 can easily grab it
RUN mv static/ts/calendar.js calendar-compile.js

# ==========================================
# Stage 2: Final Python Image
# ==========================================
FROM python:3.11-slim

# Set environment variables to prevent python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 1. Copy the local project files into the container (including your static/js folder)
COPY . /app

# 2. OVERRIDE/ADD the compiled JS file into the static/js folder
COPY --from=frontend-builder /build/calendar-compile.js /app/static/js/calendar-compile.js

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "--bind", "0.0.0.0:8000", "wsgi:app"]