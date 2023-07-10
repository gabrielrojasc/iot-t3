from peewee import PooledMySQLDatabase
from .models import create_tables

if __name__ == "__main__":
    # Connect to the database
    db = PooledMySQLDatabase(
        database="your_database_name",
        user="your_username",
        password="your_password",
        host="your_host",
        port=3306,
        max_connections=8,  # Adjust the value based on your needs
        stale_timeout=300,  # Adjust the value based on your needs
    )

    # Call the create_tables function to create the tables
    create_tables()
