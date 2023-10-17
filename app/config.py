import os

APP_ENV = os.getenv('APP_ENV', 'close')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME', 'root')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'dona')
DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'ge0d4t')
TEST_DATABASE_NAME = os.getenv('DATABASE_NAME', 'ge0d4t')

# APP_ENV = os.getenv('APP_ENV', 'hplant')
# DATABASE_USERNAME = os.getenv('DATABASE_USERNAME', 'hpl4nt_user')
# DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'PVF4DPWGjIGZJpnsd6PYDNLDGFqCKWYj')
# DATABASE_HOST = os.getenv('DATABASE_HOST', 'dpg-chcmjdqk728tp9evjbh0-a.oregon-postgres.render.com')
# DATABASE_NAME = os.getenv('DATABASE_NAME', 'hpl4nt')
# TEST_DATABASE_NAME = os.getenv('DATABASE_NAME', 'hplantest')