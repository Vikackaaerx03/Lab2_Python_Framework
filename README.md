# Password Security Lab v2.0 | Authentication & Access Control

A high-performance, asynchronous web application built with **FastAPI**. This iteration (Lab 2) implements a complete User Authentication system, persistent data storage using **SQLAlchemy**, and an Administrative Dashboard with Role-Based Access Control (**RBAC**).

---

## Overview

The **Password Lab** has evolved from a static analyzer into a dynamic, data-driven security tool. It evaluates user input against strict entropy criteria, manages user sessions, and provides an administrative layer for system oversight.

---

## Lab 2 Technical Objectives

The primary goal of this update was to implement robust backend logic and secure data management:

* **Stateful Authentication:** Full Login/Logout cycle using secure, HTTP-only Cookie sessions.
* **Relational Data Modeling:** Normalized database schema with one-to-many relationships (Users ↔ Passwords).
* **Security Middleware:** Integrated dependency injection to protect private routes and validate active sessions.
* **Complexity Enforcement:** Enhanced registration logic with server-side validation (14+ characters, symbols, casing).
* **Administrative Interface:** A synchronized, dual-pane dashboard for real-time user and record management.

---

## Tech Stack

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (High-performance Python ASGI framework)
- **Database (ORM):** [SQLAlchemy](https://www.sqlalchemy.org/) with SQLite3 for local persistence
- **Templating:** [Jinja2](https://palletsprojects.com/p/jinja/) (Dynamic server-side HTML rendering)
- **Authentication:** Cookie-based session management
- **Frontend:** Modern CSS3 featuring Flexbox layouts and **Glassmorphism** UI design
- **Server:** [Uvicorn](https://www.uvicorn.org/) (ASGI web server)

---

## Project Architecture

The project follows a modular directory structure to ensure scalability and separation of concerns:

```text
Lab2_Python_Framework/
├── app/
│   ├── routers/
│   │   ├── auth.py          
│   │   └── password.py      
│   ├── static/
│   │   └── style.css        
│   ├── templates/
│   │   ├── admin.html       
│   │   ├── index.html       
│   │   ├── login.html      
│   │   ├── register.html    
│   │   └── result.html     
│   ├── database.py          
│   ├── dependencies.py      
│   ├── main.py             
│   └── models.py           
├── database.db              
├── pyproject.toml          
└── README.md                
```
## Installation & Deployment
1. Clone the Repository
``` bash
git clone [https://github.com/Vikackaaerx03/Lab2_Python_Framework.git](https://github.com/Vikackaaerx03/Lab2_Python_Framework.git)
cd Lab2_Python_Framework
```
2. Environment Configuration
``` bash
# Initialize virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/macOS)
source .venv/bin/activate
``` 
3. Dependency Resolution
``` bash
pip install fastapi uvicorn jinja2 sqlalchemy python-multipart
``` 
4. Application Launch
``` bash
uvicorn app.main:app --reload
The server will be available at: http://127.0.0.1:8000
``` 
## Administrative Oversight
The Admin Panel (/admin) is restricted to accounts with the admin role. It provides a synchronized view of the system state:

User Directory: Real-time list of registered accounts with the ability to revoke access (Delete).

Vault Access: View and manage passwords that have cleared all security entropy checks.

Data Integrity: Cascading deletions ensure that removing a user automatically purges their associated password records.

## Author
Victoriia Roslav Group: KN-732

University: National Technical University "Kharkiv Polytechnic Institute" (NTU "KhPI")

Faculty: Computer Science and Software Engineering
