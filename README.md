# 247LiveSports Web Application

## Overview
247LiveSports is a real-time sports web application designed to provide live updates on soccer fixtures and scores. The application is built using Django and leverages WebSockets for real-time data communication, ensuring users get up-to-date information without needing to refresh the page.

## Features
- **Live Updates:** Real-time updates on soccer fixtures, scores, and match statuses using WebSockets.
- **Background Task Processing:** Efficient task management and scheduling with Celery, allowing for periodic data fetching and processing.
- **User-Friendly Interface:** A responsive and dynamic frontend that displays live, scheduled, finished, and upcoming fixtures.
- **Scalability:** Deployed using AWS, with Redis for caching and as a channel layer to support high volumes of traffic.

## Tech Stack
- **Backend:** Django, Channels, Celery
- **Frontend:** HTML, CSS, JavaScript, Django Templates
- **Database:** PostgreSQL
- **Cache/Message Broker:** Redis
- **Deployment:** AWS (EC2, RDS, S3)

## Installation

### Prerequisites
- Python 3.x
- PostgreSQL
- Redis
- Node.js (optional, for frontend builds)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/247livesports.git
   cd 247livesports
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the PostgreSQL database:
   ```bash
   createdb db247livesports
   ```

5. Configure environment variables and update the `settings.py` file with database and Redis configurations.

6. Run migrations:
   ```bash
   python manage.py migrate
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

8. Start Celery worker:
   ```bash
   celery -A project247livesports worker --loglevel=info
   ```

9. Start Celery beat (for periodic tasks):
   ```bash
   celery -A project247livesports beat --loglevel=info
   ```
