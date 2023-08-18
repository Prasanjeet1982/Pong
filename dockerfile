# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable to specify host and port for FastAPI
ENV HOST=0.0.0.0 PORT=80

# Run FastAPI when the container launches
CMD ["uvicorn", "filename:app"]
