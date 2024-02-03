# DOCKERIZED-PYTHON-MICROSERVICES-APPLICATION
Develop a Python-based project with Docker, focusing on user  authentication, API key generation, and logging across three microservices.

# Python Microservices Application

This project comprises three interconnected microservices using Python, Flask, Docker, and MongoDB.
It has 3 Microservices
- Data service (data_controller.py) - it contains registering a user and initiating login and generate authorization token

- Processing Service (api_key_generator_service.py) - it is mainly for api_key generating by providing authorization token and checking whether the user is valid or not .if the user is valid generating an api_key.

- Logging service (log_service.py) - This service is to Monitoring the user Register, Login Activities


## Prerequisites

- Docker installed on your machine.
- Replace placeholder values in Dockerfiles and docker-compose.yml with your actual MongoDB connection string and secret key.

## Build and Run

1. Build the Docker containers:

   ```bash
   docker-compose build

    ```
2. Run the Docker containers:

   ```bash
   docker-compose up

    ```


