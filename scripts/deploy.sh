#!/bin/bash

echo "Starting deployment..."

# Build and push Docker images
echo "Building Docker image..."
docker build -t ator-backend .
echo "Docker image built successfully."

# Add additional deployment steps here
# E.g., push to Docker registry, deploy to Kubernetes, etc.

echo "Deployment completed successfully."
