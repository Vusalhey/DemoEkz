import psycopg2

def connect_db():
    return psycopg2.connect(
        dbname="zachet",
        user="postgres",
        password="78987898",
        host="localhost",
        port="5432"
    )
