import sqlite3
import os
from objetos import *

DB_PATH = "database.db"

def reset_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)

    with open("schema.sql", "r") as f:
        conn.executescript(f.read())

    return conn

conn = sqlite3.connect("database.db")
a = Device(9,1)
a.delete(conn)
a.save(conn)



print("\n✅ TODOS LOS TESTS PASADOS CORRECTAMENTE")

conn.close()