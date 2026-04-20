
def insert_devtype(conn, device_type):
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO device_types (device_type_name, manufacturer) VALUES (:device_type_name, :manufacturer)" ,
                    {"device_type_name": device_type.device_type_name, 
                     "manufacturer": device_type.manufacturer})
        device_type.device_type_id = c.lastrowid
    print("Device_type insertado ✅")
    c.close()

def get_all_devtype(conn):
    c = conn.cursor()

    print(f" Datos de device_types")
    c.execute("SELECT * FROM device_types")
    results = c.fetchall()

    c.close()
    return results


def get_devtype_by_manufacturer(conn, manufacturer):
    c = conn.cursor()

    print(f" Datos que coinciden con {manufacturer}")
    c.execute("SELECT * FROM device_types WHERE manufacturer = :manufacturer", {"manufacturer": manufacturer})
    results = c.fetchall()

    c.close()
    return results

def get_devtype_by_name(conn, name):
    c = conn.cursor()

    print(f" Datos que coinciden con {name}")
    c.execute("SELECT * FROM device_types WHERE device_type_name = :device_type_name", {"device_type_name": name})
    results = c.fetchall()

    c.close()
    return results

def get_devtype_by_id(conn, id):
    c = conn.cursor()

    print(f" Datos que coinciden con {id}")
    c.execute("SELECT * FROM device_types WHERE device_type_id = :device_type_id", {"device_type_id": id})
    results = c.fetchone()

    c.close()
    return results

def delete_devtype_by_manufacturer(conn, manufacturer):
    c = conn.cursor()

    with conn:
        c.execute("DELETE FROM device_types WHERE manufacturer = :manufacturer", {"manufacturer": manufacturer})
        print("Devtype eliminado (si existia)")

    c.close() 

def delete_devtype_by_name(conn, name):
    c = conn.cursor()

    with conn:
        c.execute("DELETE FROM device_types WHERE device_type_name = :device_type_name", {"device_type_name": name})
        print("Devtype eliminado (si existia)")

    c.close() 

def delete_devtype_by_id(conn, id):
    c = conn.cursor()

    with conn:
        c.execute("DELETE FROM device_types WHERE device_type_id = :device_type_id", {"device_type_id": id})
        print("Devtype eliminado (si existia)")

    c.close() 

# El objeto tiene que venir con id previa!!!
def update_devtype(conn, device_type):
    c = conn.cursor()
    with conn:
        c.execute("""UPDATE device_types SET device_type_name = :device_type_name, manufacturer = :manufacturer 
                     WHERE device_type_id  = :device_type_id""",
                    {"device_type_name": device_type.device_type_name, 
                     "manufacturer": device_type.manufacturer,
                     "device_type_id": device_type.device_type_id})
             
    print("Device_type actualizado ✅")
    c.close()

def update_devtype_name(conn, name, manufacturer):
    c = conn.cursor()
    with conn:
        c.execute("""UPDATE device_types SET manufacturer = :manufacturer 
                     WHERE device_type_name  = :device_type_name""",
                    {"device_type_name": name, 
                     "manufacturer": manufacturer})
             
    print("Device_type actualizado ✅")
    c.close()

def update_devtype_manufacturer(conn, manufacturer, name):
    c = conn.cursor()
    with conn:
        c.execute("""UPDATE device_types SET device_type_name = :device_type_name
                     WHERE manufacturer  = :manufacturer""",
                    {"device_type_name": name, 
                     "manufacturer": manufacturer})
             
    print("Device_type actualizado ✅")
    c.close()