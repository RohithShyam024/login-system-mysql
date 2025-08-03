import os
import getpass
try:
    import dotenv
    dotenv.load_dotenv()
except ImportError:
    pass  # .env support optional

# Try to import bcrypt; if unavailable fallback to passlib
use_passlib = False
try:
    import bcrypt
except ImportError:
    try:
        from passlib.hash import bcrypt as passlib_bcrypt
        use_passlib = True
    except ImportError:
        print("❌ Neither bcrypt nor passlib[bcrypt] is installed. Please install one of them.")
        exit(1)

import mysql.connector
from mysql.connector import errorcode

def get_env(name, default=None):
    return os.getenv(name) or default

# Load connection info from environment or prompt
DB_HOST = get_env('DB_HOST', 'localhost')
DB_USER = get_env('DB_USER', 'root')
DB_PASSWORD = get_env('DB_PASSWORD', None)
DB_NAME = get_env('DB_NAME', 'login_db')

if DB_PASSWORD is None:
    # don't echo password
    DB_PASSWORD = getpass.getpass(prompt='MySQL password: ')

def connect():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            auth_plugin='mysql_native_password'  # fallback if auth issues
        )
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"Database '{DB_NAME}' does not exist. Please create it and rerun. (e.g. CREATE DATABASE {DB_NAME};)")
        elif err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access denied: check your username/password.")
        else:
            print(f"Database connection error: {err}")
        exit(1)

def setup_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username VARCHAR(255) PRIMARY KEY,
        password_hash VARCHAR(255) NOT NULL
    )
    """ )

def hash_password(raw: str) -> bytes:
    if use_passlib:
        # passlib returns string; encode to bytes for storage consistency
        return passlib_bcrypt.hash(raw).encode()
    else:
        return bcrypt.hashpw(raw.encode(), bcrypt.gensalt())

def verify_password(raw: str, stored_hash: bytes) -> bool:
    if use_passlib:
        try:
            return passlib_bcrypt.verify(raw, stored_hash.decode())
        except Exception:
            return False
    else:
        return bcrypt.checkpw(raw.encode(), stored_hash)

def register(cursor, conn):
    username = input("Enter new username: ").strip()
    if not username:
        print("❌ Username cannot be empty.")
        return
    password = getpass.getpass(prompt='Enter new password: ').strip()
    if not password:
        print("❌ Password cannot be empty.")
        return
    hashed = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed.decode() if isinstance(hashed, bytes) else hashed))
        conn.commit()
        print("✅ Registration successful.")
    except mysql.connector.IntegrityError:
        print("❌ Username already exists.")

def login(cursor):
    username = input("Username: ").strip()
    if not username:
        print("❌ Username cannot be empty.")
        return
    password = getpass.getpass(prompt='Password: ').strip()
    cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    if not result:
        print("❌ User not found.")
        return
    stored_hash = result[0].encode() if isinstance(result[0], str) else result[0]
    if verify_password(password, stored_hash):
        print("✅ Login successful! Welcome, {}.".format(username))
    else:
        print("❌ Invalid credentials.")

def main():
    print("=== Simple Login System ===")
    conn = connect()
    cursor = conn.cursor()
    setup_table(cursor)
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choice: ").strip()
        if choice == '1':
            register(cursor, conn)
        elif choice == '2':
            login(cursor)
        elif choice == '3':
            break
        else:
            print("❌ Invalid option.")
    cursor.close()
    conn.close()
    print("Goodbye.")

if __name__ == '__main__':
    main()
