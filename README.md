# Orchestrator Backend

## Overview
The Orchestrator Backend is a Python Flask application providing RESTful APIs for the SaaS API Testing Orchestrator. It handles API test execution, management, and integration with other system components.

## Architecture
The backend is designed with a modular approach, separating concerns into distinct services and layers.

```mermaid
graph LR
    A[API Gateway] --> B[Authentication Service]
    A --> C[Test Management Service]
    A --> D[Performance Testing Service]
    B --> E[Database]
    C --> E
    D --> E
```

## Getting Started

### Prerequisites
- Python (v3.8 or later)
- pip (Python package manager)
- Virtual environment (recommended)

### Installation
Clone the repository:
```bash
git clone https://github.com/ator-backend
```

Navigate to the cloned directory:
```bash
cd ator-backend
```

Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate # On Windows use venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### Configuration
Set up the necessary environment variables in a .env file or export them directly:

```env
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URI=mysql+pymysql://user:password@localhost/dbname
```


### Running the Server

To start the Flask development server:
```bash
flask run
```

The API will be available at http://localhost:5000.

## Testing
To run unit tests, execute:

```bash
python -m unittest
```


## Contributing
I encourage contributions to the project. Please read our contributing guidelines for more information.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
