from objetos import *
from funcionalidad import *

def mainMenu():
    aux = -1
    print(""" **Choose a menu**
1. Device Manager
2. Test Manager
3. Requirement Manager
4. Device Test Manager
5. Test Template Manager
6. Requirement Template Manager
    """)
    
    aux = int(input("Choose a menu (1-6): "))

    while aux not in [1, 2, 3, 4, 5, 6]:
        aux = int(input("Invalid selection, please choose one of the available options:"))


    return aux

def DevMainMenu(conn):
    aux = -1
    print(""" **Choose a menu**
1. Create a new device
2. Modify a device
3. Show all devices
4. Show all devices in a location
5. Show all devices of a type
6. Exit
    """)

    aux = int(input("Choose a menu (1-6): "))

    while aux not in [1, 2, 3, 4, 5, 6]:
        aux = int(input("Invalid selection, please choose one of the available options:"))


def ask_value(message):
    value = ""

    while not value.strip():
        value = input(message)

    return value


def createNewDevice(conn):
    device = Device()

    # Validación personalizada para el type id
    aux = None

    while aux is None:
        value = input("Choose a device type id: ")

        # Aquí puedes meter tu criterio personalizado
        if value.strip():
            aux = value

    device.device_type_id = aux

    device.device_name = ask_value("Choose a name for the device: ")
    device.serial_number = ask_value("Choose a serial number for the device: ")
    device.device_location = ask_value("Choose a location for the device: ")
    device.device_observations = ask_value("Write any observations for the device: ")

    device.save(conn)
    device.update_status(conn)
    print(device)


conn = get_connection("database.db")
createNewDevice(conn)