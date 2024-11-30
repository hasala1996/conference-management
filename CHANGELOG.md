# CHANGELOG

## [0.0.1] - 2024-11-30
- Initial release of the application with the following features:  - **Endpoints**:
    - Dependency Management:
      - Poetry to manage dependencies.
      - Added pyproject.toml file to manage dependencies.
      - Removed requirements.txt as dependencies are now managed by Poetry.
    - User CRUD Functionality:
      - Added user CRUD functionality to manage users in the database.
      - Added API endpoints for user management (create, read, update, delete).
    - Testing:
      - Added comprehensive unit and integration tests covering endpoints, services, and database interactions.
    - Seed Data Script:
      - Added seed_data.py script to populate the database with initial data.
    - Dockerization:
      - Dockerfile to containerize the application.
      - docker-compose.yml file to define services and manage dependencies.
      - Configured environment variables and networking in Docker Compose for seamless service communication.
      - Developed entrypoint.sh script to handle database migrations and seed data execution upon container startup
    - Database Migrations:
      - Migration setup with Alembic to create necessary tables and manage database schema.
      - Ensured migrations are applied automatically when the Docker container starts.
