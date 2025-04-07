# FastAPI BackEnd Project

## Overview
This project is a FastAPI application that provides a backend for user management and authentication functionalities. It is structured to separate concerns and maintain a clean architecture.

## Project Structure
```
Fast_API_BackEnd
├── app
│   ├── api
│   │   └── v1
│   │       ├── routes_auth.py      # Contains authentication-related routes
│   │       └── routes_user.py      # Contains user management routes
│   ├── core
│   │   └── config.py               # Configuration settings for the application
│   └── main.py                     # Entry point of the FastAPI application
└── README.md                       # Documentation for the project
```

## File Descriptions

### app/main.py
This file is the entry point of the FastAPI application. It creates an instance of the FastAPI app, sets up CORS middleware, and includes routers for user and authentication routes.

### app/api/v1/routes_auth.py
This file contains the routes related to authentication. It defines the endpoints for user login, registration, and other authentication-related functionalities.

### app/api/v1/routes_user.py
This file contains the routes related to user management. It defines the endpoints for user creation, retrieval, updating, and deletion.

### app/core/config.py
This file contains the configuration settings for the application, such as environment variables and application settings.

## Getting Started

### 1. Create a Virtual Environment
To isolate the project dependencies, create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

- On Windows:
  ```bash
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### 2. Install Dependencies
Install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory of the project and add the following variables:

```env
DATABASE_URL=postgresql://<user>:<password>@<host>/<database_name>
FRONTEND_ORIGIN=http://localhost:3000
```

Replace `<user>`, `<password>`, `<host>`, and `<database_name>` with your database credentials and configuration.

### 4. Run the Application
Start the FastAPI application using an ASGI server like `uvicorn`:

```bash
uvicorn app.main:app --reload
```

The application will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## License
This project is licensed under the MIT License.