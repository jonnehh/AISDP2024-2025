import psycopg2
import os

def get_db_connection():
    return psycopg2.connect(
        dbname="medicines",
        user="postgres",
        password=os.getenv("POSTGRES_PASSWORD"),
        host="postgres-service.my-app.svc.cluster.local",
        port=5432
    )


