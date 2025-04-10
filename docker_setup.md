# Docker Setup Instructions

To use Docker with the expense tracker application, follow these steps:

## 1. Docker Login

First, you need to log in to Docker Hub:

1. Open a terminal/command prompt
2. Run the following command:
```bash
docker login
```
3. Enter your Docker Hub username and password when prompted
   - If you don't have a Docker Hub account, creatve one at https://hub.docker.com/signup

## 2. Verify Docker Installation

Ensure Docker is properly installed:
```bash
docker --version
docker ps
```

## 3. Building the Image

After logging in, you can build the application:
```bash
docker build -t expense-tracker .
```

## 4. Running the Container

Run the container:

1. Create a .env file for email settings (optional):
```bash
# Create .env file
cat > .env << EOL
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=nagaswetha.thumati@gmail.com
SMTP_PASSWORD=bvpnyvrmhgopkjhu
EOL
```

2. Run the container:
```bash
# Without email notifications
docker run -p 8501:8501 expense-tracker

# With email notifications (using .env file)
docker run -p 8501:8501 --env-file .env expense-tracker
```

## Troubleshooting

1. If you get authentication errors:
   - Make sure you're logged in with `docker login`
   - Check your Docker Hub subscription status
   - Try logging out and back in: `docker logout` then `docker login`

2. If the build fails:
   - Check your internet connection
   - Verify Docker daemon is running
   - Try clearing Docker cache: `docker builder prune`

3. If the container won't start:
   - Check if port 8501 is already in use
   - Try a different port: `-p 8502:8501`
   - Check Docker logs: `docker logs [container-id]`

## Docker Commands Reference

Common Docker commands you might need:

```bash
# List running containers
docker ps

# Stop a container
docker stop [container-id]

# Remove a container
docker rm [container-id]

# List images
docker images

# Remove an image
docker rmi expense-tracker

# View logs
docker logs [container-id]

# Interactive shell in container
docker exec -it [container-id] /bin/bash
```

Remember to replace `[container-id]` with your actual container ID, which you can find using `docker ps`.
