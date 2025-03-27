# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create the data directory for outputs
RUN mkdir -p /data/outputs

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["fastapi", "run"]