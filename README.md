# Login System with Hashing (MySQL + bcrypt/passlib)

A simple command-line login system using Python, MySQL, and secure password hashing with `bcrypt`. Falls back to `passlib` if `bcrypt` isn't available. Designed to be GitHub-deployable with minimal setup.

## Features
- Register & login users via CLI
- Secure password hashing (`bcrypt` or `passlib[bcrypt]` fallback)
- MySQL backend for persistence
- Environment variable configuration support via `.env`

## Requirements
- Python 3.8+ (you have 3.13.5)
- MySQL server running and accessible
- Python packages listed in `requirements.txt`

## Setup

1. **Clone / download repository** (or start folder locally)

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   If `bcrypt` fails to build/install on Python 3.13, install fallback:
   ```bash
   pip install "passlib[bcrypt]"
   ```

4. **Create MySQL database**
   Log into your MySQL shell or Workbench and run:
   ```sql
   CREATE DATABASE login_db;
   ```

5. **Configure environment variables**
   Create a `.env` file in the root (you can copy `.env.example`) with:
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_NAME=login_db
   ```

6. **Run the app**
   ```bash
   python main.py
   ```

## Usage
- Choose `1` to register a new user. Passwords are hashed before storage.
- Choose `2` to login. Credentials are verified securely.

## Security Notes
- Passwords are never stored in plaintext. Hashing uses `bcrypt` with salt; fallback uses `passlib`'s bcrypt implementation.
- `.env` is ignored in `.gitignore` so secrets don’t get committed by accident.

## GitHub Deployment Tips
- Add a `README.md`, commit all files, then push to GitHub:
  ```bash
  git init
  git add .
  git commit -m "Initial commit: login system with hashing"
  git branch -M main
  git remote add origin <your-github-repo-url>
  git push -u origin main
  ```

## Optional Improvements
- Wrap CLI in a web interface (Flask/FastAPI)
- Add rate-limiting or account lockout after failed attempts
- Use connection pooling for performance
- Store session tokens for persistent login

## License
MIT

## Continuous Integration
A GitHub Actions workflow (`.github/workflows/ci.yml`) is included to perform syntax checks on push/pull requests.
