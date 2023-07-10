from peewee import PooledMySQLDatabase

# Configure the database connection
db = PooledMySQLDatabase(
    database="your_database_name",
    user="your_username",
    password="your_password",
    host="your_host",
    port=3306,
    max_connections=8,  # Adjust the value based on your needs
    stale_timeout=300,  # Adjust the value based on your needs
)
