import sqlite3
from funcionalidad import *
from objetos import DeviceType
# Crear / conectar a la base de datos
conn = sqlite3.connect("database.db")

# Leer el archivo SQL
with open("schema.sql", "r") as f:
    sql = f.read()

# Ejecutar el SQL (crear tablas)
conn.executescript(sql)


devtype1 = DeviceType(None , "7", "kok")
devtype1.save(conn)
#print(get_all_devtype(conn))
#delete_devtype_by_manufacturer(conn, "Adios")
print(get_all_devtype(conn))


conn.commit()
conn.close()

print("Base de datos creada ✅")
