# RacePulse

RacePulse is a web application for exploring Formula 1 race data.

## Getting Started

Follow these steps to get RacePulse up and running on your local machine.

### Prerequisites

* Python (version 3.12 or higher)
* Django (version 5.2 or higher)
* MYSQL (or your preferred database)
* Node.js and npm

### 1. Database Setup

1.  Download the F1 database dump from the official `f1db` GitHub releases page.
    > [https://github.com/f1db/f1db/releases/](https://github.com/f1db/f1db/releases/)

2.  Restore the database dump to your local MYSQL instance.
3.  Open the `settings.py` file in the project's main directory.
4.  Update the database configuration with your local database details (username, password, and database name).
5.  I also use **postgres** as main db for sessions

### 2. Installation and Running the Project

#### 2.1 Backend

1.  Install the required Python packages. It's recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```
2.  Start the Django development server.
    ```bash
    python manage.py runserver
    ```
    The application will now be accessible at `http://127.0.0.1:8000`.

#### 2.2 Frontend

This project uses Tailwind CSS. To enable the live-reloading of styles, you need to run the Tailwind CSS server.

1.  Start the Tailwind development server.
    ```bash
    python manage.py tailwind start
    ```

#### 2.3 Command-Line Utilities

* **Django Shell:** To interact with your models and database via a Python shell, use:
    ```bash
    python manage.py shell
    ```

### 3. Frontend Development

If you need to add new npm packages or modify the frontend JavaScript, follow these steps:

1.  Navigate to the `frontend` directory.
    ```bash
    cd frontend
    ```
2.  Install your new npm package.
    ```bash
    npm install [package-name]
    ```
3.  After installing, run webpack to bundle your assets and make them available throughout the project.
    ```bash
    npx webpack --mode development
    ```
