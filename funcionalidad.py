import sqlite3

def get_connection(db_path: str) -> sqlite3.Connection:
    #Abre conexión con integridad referencial garantizada.
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
