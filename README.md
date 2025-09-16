# Bookstore API Service

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
  - [Python Environment](#python-environment)
  - [Docker Setup](#docker-setup)
- [Linting and Code Quality](#linting-and-code-quality)
- [Pre-commit Hooks Setup](#pre-commit-hooks-setup)
- [Database](#database)
  - [Database Migrations](#database-migrations)
  - [Development Database Setup](#development-database-setup)
- [Local Development Setup](#local-development-setup)
- [Testing](#testing)
  - [Unit Tests](#unit-tests)

## Requirements

- Python 3.11 (managed via `pyenv`)
- Docker & Docker Compose

## Setup

### Python Environment

1. Install the required Python version using `pyenv`:
```bash
    pyenv install 3.11
    pyenv local 3.11
```

2. Create a virtual environment and install dependencies using the following command:
```bash
    make setup-local-environment
```

3. Activate virtual environment with the following command:

```bash
    source .venv/bin/activate
```

### Docker Setup

For local development, a Docker container is used.

1. Create a `.env.local` file with the following variables for Books Service (books-service/.env):
```bash
    ENVIRONMENT=local
    SERVICE_NAME=books-service
    DATABASE_USERNAME=postgres
    DATABASE_PASSWORD=postgres
    DATABASE_HOSTNAME=books-database
    DATABASE_PORT=8001
    DATABASE_NAME=books-service
```

2. Create a `.env.local` file with the following variables for Orders Service (orders-service/.env):
```bash
    ENVIRONMENT=local
    SERVICE_NAME=orders-service
    DATABASE_USERNAME=postgres
    DATABASE_PASSWORD=postgres
    DATABASE_HOSTNAME=localhost
    DATABASE_PORT=8001
    DATABASE_NAME=orders-service
    BOOKS_API_URL=http://books-service:80
```

3. To run the project locally with docker compose, use the following command:
```bash
    make up
```

4. To stop the containers, use the following command:
```bash
    make down
```

## Linting and Code Quality

Ruff, Isort and Mypy are the tools used for this purpose. In order to run the linters on the code, use the following command:
```bash
    make check
```

In case only one of them is needed, the following commands will do:

    - ruff - used for linting

    ```bash
        make lint
    ```

    - isort - used for sorting imports

    ```bash
        make sort-imports
    ```

    - mypy - used for type checking

    ```bash
        make type-check
    ```

In case you want ruff to format your code to follow the style guidelines, run:

```bash
    make format
```

## Pre-commit Hooks Setup

Run the following command to allow isort and ruff to be executed by pre-commit
```bash
    pre-commit install
```

## Database

This project consists of two independent services—Books Service and Orders Service—each with its own database and migration setup using Alembic
.

Each service maintains its own database schema and migration history. Migrations must be managed separately for each service.

### Database Migrations
Before applying or generating migrations, ensure that the local environment is up and the respective service containers are running.

#### Applying Database Migrations
In order to apply database migration files to the database, use the following command:

# Apply migrations for books-service
```bash
    make migrate-books
```

# Apply migrations for orders-service
```bash
    make migrate-orders
```

#### Generating Database Migration Files
In order to generate migration (version) files, run the following command:

# Generate migration for books-service
```bash
    make makemigrations-books
```

# Generate migration for orders-service
```bash
    make makemigrations-orders
```

Version needs to be adjusted, since alembic generates hashed version strings, and for readability / tracking purposes we'll use integers. An example is changing the version / migration file from the hash value to 000001.

Also, previous migrations need to be applied to the database before generating new migration files.

## Local Development Setup
Once pyenv is installed and the python verison locally is 3.11, by following the following commands everything will be ready for development / testing:

1. Setup Python Virtual Environment
```bash
    make setup-local-environment
```

2. Run docker compose
```bash
    make up
```

3. Apply migrations
```bash
    make migrate-local
```

## Testing

### Unit Tests
Run the following command to execute unit tests
```bash
    make unit-tests
```
