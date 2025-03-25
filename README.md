<div align="center">

# Stock-Pulse

![Logo](logo.png)

# Tech stack:
![Vue.js](https://img.shields.io/badge/vuejs-%2335495e.svg?style=for-the-badge&logo=vuedotjs&logoColor=%234FC08D)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![NodeJS](https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white)
![Express.js](https://img.shields.io/badge/express.js-%23404d59.svg?style=for-the-badge&logo=express&logoColor=%2361DAFB)
![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white) Demo: https://www.youtube.com/watch?v=oe0EWDdG6dk
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
  
![image](https://github.com/user-attachments/assets/5f1ca67e-e418-4ae4-adc6-c7ac3a9c7001)
![image](https://github.com/user-attachments/assets/8f2abbf3-8fe5-407e-aca5-ab2724d1dc68)
![image](https://github.com/user-attachments/assets/fa79a790-dc4e-409b-8380-8cc8a717723d)
![image](https://github.com/user-attachments/assets/2ebd3c8c-eb0c-4a32-a992-80d265dc7097)
![image](https://github.com/user-attachments/assets/d0b96d2b-60d4-4774-9c76-11c793344b67)
![image](https://github.com/user-attachments/assets/44837cc6-fe9e-4115-9321-5b71a2e44ced)
![image](https://github.com/user-attachments/assets/46f5e7c4-0e93-4397-91e2-354082813368)
![image](https://github.com/user-attachments/assets/7ecbed41-2359-432d-bda5-e14d01322136)
![image](https://github.com/user-attachments/assets/d0702131-22a6-48ee-b79d-895589616c82)








