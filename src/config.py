import os

# Database
DB_NAME = os.getenv('DB_NAME', 'aiochat')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', '')
DB_HOST = os.getenv('DB_HOST', '0.0.0.0')
DB_PORT = os.getenv('DB_PORT', 5432)

DB_DSN = f'postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Web application
WEB_HOST = os.getenv('WEB_HOST', '0.0.0.0')
WEB_PORT = os.getenv('WEB_PORT', '8000')
