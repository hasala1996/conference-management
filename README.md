# My Events - Event Management

## Description

- The "My Events" Event Management API is an application that efficiently manages the entire lifecycle of an event. The API centralizes event-related information, automates manual processes, and enhances user experience by facilitating access to information and the registration process.

- The application is implemented in FastAPI and uses a hexagonal architecture to separate business logic, data access, and API entry points.

- The hexagonal architecture allows a high degree of decoupling between business logic and infrastructure details, which facilitates code scalability and maintainability. The layers of this architecture and how they are implemented in this project are described below.

## Addressed Problems

- **Disorganization**: Provides a centralized platform to store and manage all event-related information, including registrations, schedules, and resources.
- **Manual Processes**: Automates tasks traditionally performed manually, such as attendee registration and report generation, saving time and reducing errors.
- **Difficulty in Decision Making**: Offers precise data and analysis to facilitate strategic decision-making about events.
- **Poor User Experience**: Enhances user experience by making information access and registration processes easier, increasing customer satisfaction.

## Application Benefits

- **Organization and Efficiency**: Centralizes information, automates processes, and reduces errors, improving operational efficiency.

## Objective

The objective is to create a robust backend solution using modern technologies such as FastAPI, GraphQL, SQLAlchemy, Elasticsearch, and Docker.

## Basic Project Structure

```
├── app/
│   ├── adapters/               # Infrastructure adapters (DB, API)
│   │   ├── api/                # API adapter (endpoints)
│   │   │   └── endpoints/      # API endpoints
│   │   ├── database/           # Database adapter
│   │   │   ├── models.py       # Database models
│   │   │   ├── repository/     # Repositories (concrete and abstract)
│   │   │   └── __init__.py
│   ├── core/                   # Application core (business logic)
│   │   ├── session/            # Logic module for session management
│   │   │   ├── services.py     # Business services
│   │   │   └── ports/          # Ports (interfaces)
│   │   └── middleware/         # Error handling middleware
│   └── fast_api/               # FastAPI configuration file
│   ├── alembic                 # Alembic configuration
├── .env                        # Environment variables
└── README.md                   # README file
```

## Installation

### Using Poetry

1. Clone the repository.
2. Navigate to the project directory:
   ```bash
   cd your_repository
   ```
3. Install Poetry if you don't have it yet:
   ```bash
   pip install poetry
   ```
4. Install the project dependencies:
   ```bash
   poetry install
   ```

### Running Without Docker

1. Ensure your `.env` file is configured to use `localhost` for the database name when running without Docker.
2. Use the launch configuration file located in the `.vscode` folder to start the application.

### Using Docker

Running the Project with Docker:
To simplify the setup and ensure consistency across development environments, you can run the project using Docker and Docker Compose.

## Prerequisites
- Docker: Make sure Docker is installed on your machine. You can download it from Docker Desktop.
- Docker Compose: Usually included with Docker Desktop. Verify it's installed by running `docker-compose --version` in your terminal.

### Build and Run the Containers
Being in the app folder of the project, execute:

- `docker-compose up --build`

This command will:

- Build the Docker image for your FastAPI application.
- Start the services defined in `docker-compose.yml`, which include the backend (FastAPI) and the PostgreSQL database.
- Apply migrations and start the development server.

### With Docker

- The application will be available at `http://localhost:8000`.

## Documentation

- The documentation provided by FastAPI is available at `http://localhost:8000/docs`.


## Technologies Used

- **FastAPI**: Framework for building fast and efficient APIs.
- **SQLAlchemy**: ORM for database management.
- **Docker**: For containerization and deployment.

## Database

- The database is managed by SQLAlchemy and Alembic, powered by PostgreSQL.
- In the repo, look for the image called `db_diagram.png`, which details the implemented ER model.

## License

This project is under the MIT License. For more details, see the `LICENSE` file.