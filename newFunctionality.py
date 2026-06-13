import sqlite3
import os
from objetos import DeviceType, Device, TestTemplate, Test, RequirementTemplate, Requirement
from excepciones import DeviceManagerError, NotFoundError, InvalidReferenceError, InvalidStatusError

LINE_LENGTH = 75
DB_PATH = "database.db"
SCHEMA_PATH = "schema.sql"

def get_connection(db_path: str) -> sqlite3.Connection:
    #Abre conexión con integridad referencial garantizada.
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_database(db_path, schema_path):

    if os.path.exists(db_path):
        print("The database already exist")
        return
    
    conn = get_connection(db_path)

    with open(schema_path, "r") as f:
        schema = f.read()
    
    try:
        conn.executescript(schema)
        conn.commit()
        print("Database created successfully")
    finally:
        conn.close()


    #Aqui podria ponerse algo para meterle unos valores predefinidos o algo asi

def reset_database(schema_path):
    check = prompt("This will delete all data permanently. Are you sure? [Y/N]").lower()
    
    if check not in ["yes", "ye", "y"]:
        print("  Reset cancelled.")
        return

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("  Database deleted.")

    with open(schema_path, "r") as f:
        schema = f.read()

    conn = get_connection(DB_PATH)
    try:
        conn.executescript(schema)
        conn.commit()
        print("  Database recreated successfully.")
    finally:
        conn.close()  

def print_header(text):
    aux = int((LINE_LENGTH - len(text) - 4)/2)
    n = "=" * LINE_LENGTH
    i = "-" * aux + "  " + text + "  " + "-" * aux
    if len(i) < LINE_LENGTH:
        i += "-"

    print(n)
    print(i)
    print(n)

def print_separator():
    n = "-" * LINE_LENGTH
    print(n)

#Pide un dato al usuario y lo toma como input sin espacios
def prompt(message):
    return input(f"  > {message}: ").strip()

def wait():
    input("\n  Press Enter to continue...")

def menu_device_types():
    while True:
        print_header("Templates Menu | Device Type")
        print("Device Type List")
        print_separator()
        list_device_type()
        print_separator()

        aux = prompt("Choose a device type to see its details").lower().strip()

        if aux.startswith("ex"):
            return
        elif aux.startswith("cr"):
            create_device_type()
            continue
        else:
            try:
                aux = int(aux)
            except ValueError:
                print("  Invalid option.")
                continue
            menu_test_template(aux)
            

def create_device_type():
    print_header("Create device type")

    deviceType = DeviceType()
    check = "NO"

    while check not in ["yes", "ye", "y"]:
        deviceType.device_type_name = prompt("Enter device type name")
        deviceType.manufacturer = prompt("Enter device manufacturer")

        print_separator() 
        print("  You are about to create a device type with the following information: ")
        print(f"  Name: {deviceType.device_type_name}\n  Manufacturer: {deviceType.manufacturer}" )
        print_separator()
        check = prompt("Are you sure? [Y/N/Back]").lower()

        if check in ["b", "ba", "bac", "back"]:
            print_separator()
            print(" Device Type creation cancelled")
            return
        
    conn = get_connection(DB_PATH)

    try:
        deviceType.save(conn)
        print("  Device Type saved successfully")
    finally:
        conn.close()
    wait()
    
    
def list_device_type():
    
    conn = get_connection(DB_PATH)
    try:
        deviceTypesList = DeviceType.load_all(conn)
        for t in deviceTypesList:
            print(f"  {t.device_type_id}. {t.device_type_name}, {t.manufacturer}")
    except NotFoundError:
        print("  No device types found")
    finally:
        conn.close()

        
def delete_device_type(device_type_id):

    print_header("Delete device type")         
            
    conn = get_connection(DB_PATH)
    try:
        device = DeviceType.load(conn, device_type_id)
    except NotFoundError:
        print("  Not found device type with that id")
        print_separator()
        wait()
        return
    finally:
        conn.close()
            
    print_separator() 
    print("  You are about to delete a device type with the following information: ")
    print(f"  Name: {device.device_type_name}\n  Manufacturer: {device.manufacturer}" )
    print_separator()
    check = prompt("Are you sure? [Y/N]").lower()

    if check not in ("yes", "ye", "y"):
        return
 
    conn = get_connection(DB_PATH)

    try:
        device.delete(conn)

    except NotFoundError as e:
        print(e)  #Esto nunca deberia ejecutarse
    finally:
        conn.close()
        return


def edit_device_type(device_type_id):

    print_header("Edit device type")         
    conn = get_connection(DB_PATH)
    try:
        device = DeviceType.load(conn, device_type_id)
    except NotFoundError:
        print("  Not found device type with that id")
        print_separator()
        wait()
        return
    finally:
        conn.close()

    device_edited = DeviceType(device.device_type_id)


    print_separator()

    #The user inputs the new info here
    device_edited.device_type_name = prompt("Enter device type name")

    #If the input is empty, the previous information is kept
    if device_edited.device_type_name == "":
        device_edited.device_type_name = device.device_type_name

    device_edited.manufacturer = prompt("Enter device manufacturer")

    if device_edited.manufacturer == "":
        device_edited.manufacturer = device.manufacturer

    print_separator() 

    #Final comprobation
    print(f"  You are about to modify device type {device.device_type_id} with the following information: ")
    print(f"  Name: {device_edited.device_type_name}\n  Manufacturer: {device_edited.manufacturer}" )
    print_separator()
    check = prompt("Are you sure? [Y/N]").lower()

    if check not in ("yes", "ye", "y"):
        return
 
    conn = get_connection(DB_PATH)

    try:
        device_edited.save(conn)

    except NotFoundError as e:
        print(e)  #Esto nunca deberia ejecutarse
    finally:
        conn.close()
        return


def print_device_type(device_type_id):
    conn = get_connection(DB_PATH)
    try:
        deviceType = DeviceType.load(conn, device_type_id)
        print(...)
    except NotFoundError:
        print("Device Type not found")
    finally:
        conn.close()


def menu_test_template(device_type_id):
     while True:
        print_header("Templates Menu | Test Template")
        print("Selected device:")
        print_device_type(device_type_id)
        print_separator()
        print("Test Template List")
        print_separator()
        list_test_template(device_type_id)
        print_separator()
        print("  > Write 'exit' to return to the previous menu")
        print("  > Write 'create' to create a new test")
        print("  > Write 'delete' to delete the selected device type")
        print("  > Write 'edit' to edit the selected device type")

        aux = prompt("Write a test template id to see its details").lower().strip()

        if aux.startswith("ex"):
            return
        elif aux.startswith("ed"):
            edit_device_type(device_type_id)
            continue
        elif aux.startswith("cr"):
            create_test_template(device_type_id)
            continue
        elif aux.startswith("de"):
            delete_device_type(device_type_id)
            return
        else:
            try:
                aux = int(aux)
            except ValueError:
                print("  Invalid option.")
                continue
            menu_requirement_template(aux)   


def list_test_template(device_type_id):

    conn = get_connection(DB_PATH)
    try:
        testTemplateList = TestTemplate.load_by_device(conn, device_type_id)
        for t in testTemplateList:
            print(f"  {t.test_template_id}. {t.test_template_name}, {t.test_description}")
    except NotFoundError:
        print("  No test templates found")
        
    finally:
        conn.close()


def create_test_template(device_type_id):

    print_header("Create test template")

    testTemplate = TestTemplate()
    testTemplate.device_type_id = device_type_id
    check = "NO"

    while check not in ["yes", "ye", "y"]:
        testTemplate.test_template_name = prompt("Enter test template name")
        testTemplate.test_description = prompt("Enter test description")

        print_separator() 
        print("  You are about to create a test template with the following information: ")
        print(f"  Name: {testTemplate.test_template_name}\n  Description: {testTemplate.test_description}" )
        print_separator()
        check = prompt("Are you sure? [Y/N/Back]").lower()

        if check in ["b", "ba", "bac", "back"]:
            print_separator()
            print(" Test Template creation cancelled")
            return
        
    conn = get_connection(DB_PATH)

    try:
        testTemplate.save(conn)
        print("  Test Template saved successfully")
    finally:
        conn.close()
    wait()





menu_test_template("8")