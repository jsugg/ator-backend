# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make port available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME ator-backend

# Run run.py when the container launches
CMD ["python", "run.py"]
