import sqlite3
import os
from objetos import DeviceType, TestTemplate, RequirementTemplate, Device

DB_PATH = "database.db"

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)

with open("schema.sql", "r") as f:
    conn.executescript(f.read())

print("INICIO TESTS\n")

print("TEST 1: INSERT DeviceType (esperado: id asignado)")
dt = DeviceType(None, "Laptop", "Dell")
dt.save(conn)
print(dt)

print("\nTEST 2: LOAD DeviceType (esperado: mismo objeto)")
print(DeviceType.load(conn, dt.device_type_id))

print("\nTEST 3: UPDATE DeviceType (esperado: nombre cambiado)")
dt.change_devtype_name("Laptop Pro")
dt.save(conn)
print(DeviceType.load(conn, dt.device_type_id))

print("\nTEST 4: INSERT TestTemplate (esperado: creado)")
tt = TestTemplate(None, dt.device_type_id, "Test CPU", "Check CPU")
tt.save(conn)
print(tt)

print("\nTEST 5: LOAD TestTemplate (esperado: mismo)")
print(TestTemplate.load(conn, tt.test_template_id))

print("\nTEST 6: INSERT RequirementTemplate (esperado: creado)")
rt = RequirementTemplate(None, tt.test_template_id, "Temp < 80C")
rt.save(conn)
print(rt)

print("\nTEST 7: LOAD RequirementTemplate (esperado: mismo)")
print(RequirementTemplate.load(conn, rt.requirement_template_id))

print("\nTEST 8: INSERT Device (esperado: id asignado)")
device = Device(
    None,
    dt.device_type_id,
    "Mi Laptop",
    "SN123",
    "Oficina",
    "OK",
    "Sin problemas"
)
device.save(conn)
print(device.device_id)

print("\nTEST 9: LOAD Device (esperado: mismo contenido)")
print(Device.load(conn, device.device_id).__dict__)

print("\nTEST 10: UPDATE parcial Device (esperado: solo cambia nombre)")
device_update = Device(device.device_id)
device_update.change_name("Nuevo Nombre")
device_update.save(conn)
print(Device.load(conn, device.device_id).__dict__)

print("\nTEST 11: load_all (esperado: >=1)")
print(len(Device.load_all(conn)))

print("\nTEST 12: load_by_type (esperado: >=1)")
print(len(Device.load_by_type(conn, dt.device_type_id)))

print("\nTEST 13: load_by_location (esperado: lista con device)")
print(Device.load_by_location(conn, "Oficina"))

print("\nTEST 14: DELETE Device (esperado: None)")
device.delete(conn)
print(Device.load(conn, device.device_id))

print("\nFIN TESTS")

print("\nTEST 11: load_all con varios devices (esperado: >=3)")
d1 = Device(None, dt.device_type_id, "Device1", "SN1", "Oficina", "OK", None)
d2 = Device(None, dt.device_type_id, "Device2", "SN2", "Lab", "OK", None)
d3 = Device(None, dt.device_type_id, "Device3", "SN3", "Oficina", "FAIL", None)

d1.save(conn)
d2.save(conn)
d3.save(conn)

all_devices = Device.load_all(conn)
for devices in all_devices:
    print(devices)

print("\nTEST 12: load_by_type con varios (esperado: 3)")
by_type = Device.load_by_type(conn, dt.device_type_id)
print(by_type)

print("\nTEST 13: load_by_location con varios (esperado: solo 'Oficina' → 2)")
by_location = Device.load_by_location(conn, "Oficina")
print(len(by_location), "devices:", [d.device_name for d in by_location])

print("\nTEST 14: DELETE uno de varios (esperado: total-1)")
d1.delete(conn)
remaining = Device.load_all(conn)
print(len(remaining), "devices restantes:", [d.device_name for d in remaining])