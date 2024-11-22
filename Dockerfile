# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Dash runs on
EXPOSE 8050

# Command to run the app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8050", "app:server"]
