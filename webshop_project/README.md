Webshop Product Catalog

A containerized microservice-based webshop architecture built for high-performance product management.

Tech Stack

- Backend: Python (FastAPI) - Modern, asynchronous REST API.
- Database: PostgreSQL - Relational data store for persistence.
- Caching: Redis - In-memory database used for high-speed product listings caching.
- Message Broker: RabbitMQ (Pika) - Asynchronous event processing pipeline.
- Frontend: Responsive HTML5, CSS3 (Flexbox/Grid), and vanilla JavaScript.
- Infrastructure: Docker & Docker Compose for multi-container orchestration.

Features

- Automated Database Seeding: On startup, the backend automatically reads product records from `backend/products.txt` and populates the database if it is empty.
- Caching Layer: Product API responses are cached in Redis to minimize database load and optimize retrieval times.
- Message Broker Simulation: Adding new products triggers asynchronous background notifications sent through a RabbitMQ inventory queue.
- Responsive Layout: The UI is dynamically optimized for both standard desktop screens (1366px) and mobile views (360px).

Setup & Execution

To spin up the entire infrastructure, run the following command from the root directory:

```bash
docker-compose down
docker-compose up --build
