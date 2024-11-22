# Base image with Python
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Copy the app's code into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Dash will run on
EXPOSE 8050

# Run the app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8050", "app:server"]
