![image](https://github.com/user-attachments/assets/5f1ca67e-e418-4ae4-adc6-c7ac3a9c7001)<div align="center">

# Stock-Pulse

![Logo](logo.png)

</div>

# Installation Guide

## 1.3.1 Cloning the Project

1. Download the repository containing the system (frontend: Vue, backend: Node.js, and Python scripts).
2. The structure should include at least three separate projects for each part of the application:
   - `www/frontend/`
   - `www/backend/`
   - `lstm/`

## 1.3.2 Docker Configuration

1. Make sure Docker and Docker Compose are installed on your system.
2. In the main project folder (or a dedicated directory), include the following files (if they are not already present):
   - A `Dockerfile` for each service
   - `docker-compose.yml`

## 1.4 Example `docker-compose.yml` Structure

```yaml
version: '3'
services:
  python-lstm:
    build:
      context: ./lstm
      dockerfile: Dockerfile
    environment:
      - FLASK_APP=src/app.py
    ports:
      - "5000:5000"
    networks:
      - app-network
    volumes:
      - ./lstm:/app

  backend:
    build:
      context: ./www/backend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    networks:
      - app-network
    depends_on:
      - python-lstm

  frontend:
    build:
      context: ./www/frontend
      dockerfile: Dockerfile
    ports:
      - "8080:80"
    networks:
      - app-network
    depends_on:
      - backend
    volumes:
      - ./www/frontend:/app

networks:
  app-network:
    driver: bridge
```

## 1.4.1 Building and Running Containers

1. Navigate to the main directory (where the `docker-compose.yml` file is located).
2. Run the following command to build the containers:

   ```bash
   docker-compose build
   ```

3. Start the containers:

   ```bash
   docker-compose up -d
   ```

4. Verify that the services are running:

   - Frontend: [http://localhost:8080](http://localhost:8080)
   - Backend: [http://localhost:3000](http://localhost:3000)
   - Python LSTM: [http://localhost:5000](http://localhost:5000)

## 1.4.2 Environment Configuration

- Depending on your needs, add environment variables (e.g., API keys, database credentials) either in `.env` files or directly in the `docker-compose.yml`.
- Make sure each container is properly configured:
  - Python services: install required libraries listed in `requirements.txt`
  - Node.js services: install dependencies from `package.json`

## 1.4.3 Test Run

1. After launching the containers, check the logs:

   ```bash
   docker-compose logs -f
   ```

2. Make sure all services are up and listening on their designated ports.
3. Test the communication between services:
   - Frontend should be able to call backend endpoints
   - Backend should be able to call the Python LSTM algorithm
