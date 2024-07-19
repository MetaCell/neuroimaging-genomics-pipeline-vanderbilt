#!/bin/bash

# Variables
IMAGE_NAME="brain-genomics"
CONTAINER_NAME="pipeline"
DOCKERFILE_PATH="."

# Build the Docker image
echo "Building Docker image..."
docker build -t $IMAGE_NAME $DOCKERFILE_PATH

# Check if the build was successful
if [ $? -eq 0 ]; then
    echo "Docker image built successfully."
else
    echo "Failed to build Docker image."
    exit 1
fi

# Stop and remove any existing container with the same name
if [ $(docker ps -aq -f name=$CONTAINER_NAME) ]; then
    echo "Stopping and removing existing container..."
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi

# Run the Docker container
echo "Running Docker container..."
docker run -it --name $CONTAINER_NAME $IMAGE_NAME -c /bin/bash