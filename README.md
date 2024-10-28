# Messenger

This project is a Telegram bot backend built using **FastAPI**, **Aiogram** for bot handling, **SQLAlchemy** for database ORM, **Celery** for background tasks, and **Jinja2** for templating. **PostgreSQL** is used as the database, and **WebSocket** is implemented to handle real-time events.


## Features
- Telegram bot interactions handled with Aiogram
- RESTful API endpoints created with FastAPI
- Database management with SQLAlchemy and PostgreSQL
- Background task processing with Celery and Redis
- Real-time updates using WebSocket
- Templating for responses and messages with Jinja2
- Asynchronous handling of requests for improved performance

## Technologies Used
- **FastAPI** - For building the REST API.
- **Aiogram** - For managing Telegram bot interactions.
- **SQLAlchemy** - For ORM and database management.
- **PostgreSQL** - As the relational database.
- **Celery** - For background task management.
- **Redis** - As a broker for Celery tasks.
- **Jinja2** - For templating responses.
- **WebSocket** - For real-time communication.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/gafurov001/mini_telegram.git
   cd mini_telegram