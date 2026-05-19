import sqlite3
import os
from objetos import DeviceType, Device, TestTemplate, Test, RequirementTemplate, Requirement
from excepciones import DeviceManagerError, NotFoundError, InvalidReferenceError, InvalidStatusError

DB_PATH = "device_testing_manager.db"
SCHEMA_PATH = "schema.sql"


# ─────────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────────

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_database():
    """Creates the database from schema.sql and seeds initial data if it doesn't exist."""
    if os.path.exists(DB_PATH):
        return

    print("Database not found. Creating from schema...")

    with open(SCHEMA_PATH, "r") as f:
        schema = f.read()

    conn = get_connection()
    conn.executescript(schema)
    conn.commit()

    seed_data(conn)
    conn.close()

    print("Database created successfully.\n")


def seed_data(conn):
    """Populates the database with initial device types and templates."""

    # Device type
    washing_machine = DeviceType(None, "Washing Machine", "Generic")
    washing_machine.save(conn)

    # Test templates
    visual = TestTemplate(None, washing_machine.device_type_id, "Visual Inspection", "Check physical condition of the device")
    visual.save(conn)

    electrical = TestTemplate(None, washing_machine.device_type_id, "Electrical Safety Test", "Verify electrical safety of the device")
    electrical.save(conn)

    # Requirement templates — Visual Inspection
    RequirementTemplate(None, visual.test_template_id, "No visible damage on casing").save(conn)
    RequirementTemplate(None, visual.test_template_id, "Labels and serial number readable").save(conn)

    # Requirement templates — Electrical Safety Test
    RequirementTemplate(None, electrical.test_template_id, "Ground connection verified").save(conn)
    RequirementTemplate(None, electrical.test_template_id, "No exposed wiring").save(conn)

    print("Seed data loaded.")


# ─────────────────────────────────────────────
# DISPLAY HELPERS
# ─────────────────────────────────────────────

def print_header(title):
    print("\n" + "=" * 45)
    print(f"  {title}")
    print("=" * 45)


def print_separator():
    print("-" * 45)


def prompt(message):
    return input(f"  > {message}: ").strip()


def wait():
    input("\n  Press Enter to continue...")


# ─────────────────────────────────────────────
# DEVICE TYPE MENUS
# ─────────────────────────────────────────────

def menu_device_types(conn):
    while True:
        print_header("Device Types")
        print("  1. List all device types")
        print("  2. Create device type")
        print("  3. Delete device type")
        print("  0. Back")
        print_separator()

        choice = prompt("Select an option")

        if choice == "1":
            action_list_device_types(conn)
        elif choice == "2":
            action_create_device_type(conn)
        elif choice == "3":
            action_delete_device_type(conn)
        elif choice == "0":
            break
        else:
            print("  Invalid option.")


def action_list_device_types(conn):
    print_header("All Device Types")
    try:
        types = DeviceType.load_all(conn)
        for dt in types:
            print(f"  [{dt.device_type_id}] {dt.device_type_name} — {dt.manufacturer}")
    except NotFoundError:
        print("  No device types found.")
    wait()


def action_create_device_type(conn):
    print_header("Create Device Type")
    name = prompt("Name")
    manufacturer = prompt("Manufacturer")

    try:
        dt = DeviceType(None, name, manufacturer)
        dt.save(conn)
        print(f"\n  Device type '{name}' created successfully.")
    except DeviceManagerError as e:
        print(f"\n  Error: {e}")
    wait()


def action_delete_device_type(conn):
    print_header("Delete Device Type")
    try:
        types = DeviceType.load_all(conn)
        for dt in types:
            print(f"  [{dt.device_type_id}] {dt.device_type_name}")
    except NotFoundError:
        print("  No device types found.")
        wait()
        return

    print_separator()
    try:
        id_input = int(prompt("Enter device type ID to delete"))
        dt = DeviceType.load(conn, id_input)
        confirm = prompt(f"Delete '{dt.device_type_name}'? This will delete all associated devices and tests. (yes/no)")
        if confirm.lower() == "yes":
            dt.delete(conn)
            print("  Device type deleted.")
        else:
            print("  Cancelled.")
    except ValueError:
        print("  Invalid ID.")
    except DeviceManagerError as e:
        print(f"\n  Error: {e}")
    wait()


# ─────────────────────────────────────────────
# DEVICE MENUS
# ─────────────────────────────────────────────

def menu_devices(conn):
    while True:
        print_header("Devices")
        print("  1. List all devices")
        print("  2. List devices by type")
        print("  3. Create device")
        print("  4. Edit device")
        print("  5. Delete device")
        print("  0. Back")
        print_separator()

        choice = prompt("Select an option")

        if choice == "1":
            action_list_devices(conn)
        elif choice == "2":
            action_list_devices_by_type(conn)
        elif choice == "3":
            action_create_device(conn)
        elif choice == "4":
            action_edit_device(conn)
        elif choice == "5":
            action_delete_device(conn)
        elif choice == "0":
            break
        else:
            print("  Invalid option.")


def action_list_devices(conn):
    print_header("All Devices")
    try:
        devices = Device.load_all(conn)
        for d in devices:
            status = "PASS" if d.device_status else "PENDING"
            print(f"  [{d.device_id}] {d.device_name} | SN: {d.serial_number} | {d.device_location} | {status}")
    except NotFoundError:
        print("  No devices found.")
    wait()


def action_list_devices_by_type(conn):
    print_header("List Devices by Type")
    try:
        types = DeviceType.load_all(conn)
        for dt in types:
            print(f"  [{dt.device_type_id}] {dt.device_type_name}")
    except NotFoundError:
        print("  No device types found.")
        wait()
        return

    print_separator()
    try:
        id_input = int(prompt("Enter device type ID"))
        devices = Device.load_by_type(conn, id_input)
        print_header(f"Devices of type {id_input}")
        for d in devices:
            status = "PASS" if d.device_status else "PENDING"
            print(f"  [{d.device_id}] {d.device_name} | SN: {d.serial_number} | {status}")
    except ValueError:
        print("  Invalid ID.")
    except DeviceManagerError as e:
        print(f"\n  Error: {e}")
    wait()


def action_create_device(conn):
    print_header("Create Device")
    try:
        types = DeviceType.load_all(conn)
        for dt in types:
            print(f"  [{dt.device_type_id}] {dt.device_type_name}")
    except NotFoundError:
        print("  No device types available. Create a device type first.")
        wait()
        return

    print_separator()
    try:
        type_id = int(prompt("Device type ID"))
        name = prompt("Device name")
        serial = prompt("Serial number")
        location = prompt("Location")

        d = Device(None, type_id, name, serial, location, None, None)
        d.save(conn)
        print(f"\n  Device '{name}' created with {len(Test.load_by_device(conn, d.device_id))} tests.")
    except ValueError:
        print("  Invalid ID.")
    except DeviceManagerError as e:
        print(f"\n  Error: {e}")
    wait()


def action_edit_device(conn):
    print_header("Edit Device")
    try:
        device_id = int(prompt("Enter device ID to edit"))
        d = Device.load(conn, device_id)
    except ValueError:
        print("  Invalid ID.")
        wait()
        return
    except DeviceManagerError as e:
        print(f"\n  Error: {e}")
        wait()
        return

    print(f"\n  Editing: {d.device_name} (leave blank to keep current value)")
    print_separator()

    name = prompt(f"Name [{d.device_name}]")
    serial = prompt(f"Serial number [{d.serial_number}]")
    location = prompt(f"Location [{d.device_location}]")
    observations = prompt(f"Observations [{d.device_observations}]")

    if name:
        d.change_name(name)
    if serial:
        d.change_serial_number(serial)
    if location:
        d.change_location(location)
    if observations:
        d.change_observations(observations)

    try:
        d.save(conn)
        print("\n  Device updated.")
    except DeviceManagerError as e:
        print(f"\n  Error: {e}")
    wait()


def action_delete_device(conn):
    print_header("Delete Device")
    try:
        devices = Device.load_all(conn)
        for d in devices:
            print(f"  [{d.device_id}] {d.device_name} | SN: {d.serial_number}")
    except NotFoundError:
        print("  No devices found.")
        wait()
        return

    print_separator()
    try:
        id_input = int(prompt("Enter device ID to delete"))
        d = Device.load(conn, id_input)
        confirm = prompt(f"Delete '{d.device_name}'? This will delete all its tests and requirements. (yes/no)")
        if confirm.lower() == "yes":
            d.delete(conn)
            print("  Device deleted.")
        else:
            print("  Cancelled.")
    except ValueError:
        print("  Invalid ID.")
    except DeviceManagerError as e:
        print(f"\n  Error: {e}")
    wait()


# ─────────────────────────────────────────────
# TEST & REQUIREMENT MENUS
# ─────────────────────────────────────────────

def menu_tests(conn):
    while True:
        print_header("Tests & Requirements")
        print("  1. View tests for a device")
        print("  2. View requirements for a test")
        print("  3. Update requirement status")
        print("  0. Back")
        print_separator()

        choice = prompt("Select an option")

        if choice == "1":
            action_list_tests(conn)
        elif choice == "2":
            action_list_requirements(conn)
        elif choice == "3":
            action_update_requirement(conn)
        elif choice == "0":
            break
        else:
            print("  Invalid option.")


def action_list_tests(conn):
    print_header("Tests for a Device")
    try:
        device_id = int(prompt("Enter device ID"))
        d = Device.load(conn, device_id)
        tests = Test.load_by_device(conn, device_id)

        print_header(f"Tests — {d.device_name}")
        for t in tests:
            template = TestTemplate.load(conn, t.test_template_id)
            status = "PASS" if t.test_status else "PENDING"
            print(f"  [{t.test_id}] {template.test_template_name} | {status}")
    except ValueError:
        print("  Invalid ID.")
    except DeviceManagerError as e:
        print(f"\n  Error: {e}")
    wait()


def action_list_requirements(conn):
    print_header("Requirements for a Test")
    try:
        test_id = int(prompt("Enter test ID"))
        t = Test.load(conn, test_id)
        requirements = Requirement.load_by_test(conn, test_id)
        template = TestTemplate.load(conn, t.test_template_id)

        print_header(f"Requirements — {template.test_template_name}")
        for r in requirements:
            req_template = RequirementTemplate.load(conn, r.requirement_template_id)
            status = "PASS" if r.requirement_status else "PENDING"
            print(f"  [{r.requirement_id}] {req_template.requirement_name} | {status}")
    except ValueError:
        print("  Invalid ID.")
    except DeviceManagerError as e:
        print(f"\n  Error: {e}")
    wait()


def action_update_requirement(conn):
    print_header("Update Requirement Status")
    try:
        test_id = int(prompt("Enter test ID"))
        requirements = Requirement.load_by_test(conn, test_id)

        for r in requirements:
            req_template = RequirementTemplate.load(conn, r.requirement_template_id)
            status = "PASS" if r.requirement_status else "PENDING"
            print(f"  [{r.requirement_id}] {req_template.requirement_name} | {status}")

        print_separator()
        req_id = int(prompt("Enter requirement ID to update"))
        r = Requirement.load(conn, req_id)
        req_template = RequirementTemplate.load(conn, r.requirement_template_id)

        print(f"\n  Requirement: {req_template.requirement_name}")
        print(f"  Current status: {'PASS' if r.requirement_status else 'PENDING'}")
        new_status = prompt("New status (pass/fail)")

        if new_status.lower() == "pass":
            r.change_status(conn, True)
            print("  Status updated to PASS.")
        elif new_status.lower() == "fail":
            r.change_status(conn, False)
            print("  Status updated to FAIL.")
        else:
            print("  Invalid status. Use 'pass' or 'fail'.")

    except ValueError:
        print("  Invalid ID.")
    except DeviceManagerError as e:
        print(f"\n  Error: {e}")
    wait()


# ─────────────────────────────────────────────
# TEMPLATE MENUS
# ─────────────────────────────────────────────

def menu_templates(conn):
    while True:
        print_header("Templates")
        print("  1. Test Templates")
        print("  2. Requirement Templates")
        print("  0. Back")
        print_separator()

        choice = prompt("Select an option")

        if choice == "1":
            menu_test_templates(conn)
        elif choice == "2":
            menu_requirement_templates(conn)
        elif choice == "0":
            break
        else:
            print("  Invalid option.")


def menu_test_templates(conn):
    while True:
        print_header("Test Templates")
        print("  1. List by device type")
        print("  2. Create")
        print("  3. Delete")
        print("  0. Back")
        print_separator()

        choice = prompt("Select an option")

        if choice == "1":
            action_list_test_templates(conn)
        elif choice == "2":
            action_create_test_template(conn)
        elif choice == "3":
            action_delete_test_template(conn)
        elif choice == "0":
            break
        else:
            print("  Invalid option.")


def action_list_test_templates(conn):
    print_header("Test Templates by Device Type")
    try:
        types = DeviceType.load_all(conn)
        for dt in types:
            print(f"  [{dt.device_type_id}] {dt.device_type_name}")
    except NotFoundError:
        print("  No device types found.")
        wait()
        return

    print_separator()
    try:
        id_input = int(prompt("Enter device type ID"))
        templates = TestTemplate.load_by_device(conn, id_input)
        dt = DeviceType.load(conn, id_input)
        print_header(f"Test Templates — {dt.device_type_name}")
        for t in templates:
            print(f"  [{t.test_template_id}] {t.test_template_name} — {t.test_description}")
    except ValueError:
        print("  Invalid ID.")
    except DeviceManagerError as e:
        print(f"\n  Error: {e}")
    wait()


def action_create_test_template(conn):
    print_header("Create Test Template")
    try:
        types = DeviceType.load_all(conn)
        for dt in types:
            print(f"  [{dt.device_type_id}] {dt.device_type_name}")
    except NotFoundError:
        print("  No device types found. Create a device type first.")
        wait()
        return

    print_separator()
    try:
        type_id = int(prompt("Device type ID"))
        name = prompt("Template name")
        description = prompt("Description")

        t = TestTemplate(None, type_id, name, description)
        t.save(conn)
        print(f"\n  Test template '{name}' created successfully.")
    except ValueError:
        print("  Invalid ID.")
    except DeviceManagerError as e:
        print(f"\n  Error: {e}")
    wait()


def action_delete_test_template(conn):
    print_header("Delete Test Template")
    try:
        types = DeviceType.load_all(conn)
        for dt in types:
            print(f"  [{dt.device_type_id}] {dt.device_type_name}")
    except NotFoundError:
        print("  No device types found.")
        wait()
        return

    print_separator()
    try:
        type_id = int(prompt("Enter device type ID to filter templates"))
        templates = TestTemplate.load_by_device(conn, type_id)
        print()
        for t in templates:
            print(f"  [{t.test_template_id}] {t.test_template_name}")

        print_separator()
        id_input = int(prompt("Enter test template ID to delete"))
        t = TestTemplate.load(conn, id_input)
        confirm = prompt(f"Delete '{t.test_template_name}'? This will delete all associated requirement templates. (yes/no)")
        if confirm.lower() == "yes":
            t.delete(conn)
            print("  Test template deleted.")
        else:
            print("  Cancelled.")
    except ValueError:
        print("  Invalid ID.")
    except DeviceManagerError as e:
        print(f"\n  Error: {e}")
    wait()


def menu_requirement_templates(conn):
    while True:
        print_header("Requirement Templates")
        print("  1. List by test template")
        print("  2. Create")
        print("  3. Delete")
        print("  0. Back")
        print_separator()

        choice = prompt("Select an option")

        if choice == "1":
            action_list_requirement_templates(conn)
        elif choice == "2":
            action_create_requirement_template(conn)
        elif choice == "3":
            action_delete_requirement_template(conn)
        elif choice == "0":
            break
        else:
            print("  Invalid option.")


def action_list_requirement_templates(conn):
    print_header("Requirement Templates by Test Template")
    try:
        types = DeviceType.load_all(conn)
        for dt in types:
            print(f"  [{dt.device_type_id}] {dt.device_type_name}")
    except NotFoundError:
        print("  No device types found.")
        wait()
        return

    print_separator()
    try:
        type_id = int(prompt("Enter device type ID"))
        templates = TestTemplate.load_by_device(conn, type_id)
        print()
        for t in templates:
            print(f"  [{t.test_template_id}] {t.test_template_name}")

        print_separator()
        template_id = int(prompt("Enter test template ID"))
        tt = TestTemplate.load(conn, template_id)
        req_templates = RequirementTemplate.load_by_test(conn, template_id)

        print_header(f"Requirements — {tt.test_template_name}")
        for r in req_templates:
            print(f"  [{r.requirement_template_id}] {r.requirement_name}")
    except ValueError:
        print("  Invalid ID.")
    except DeviceManagerError as e:
        print(f"\n  Error: {e}")
    wait()


def action_create_requirement_template(conn):
    print_header("Create Requirement Template")
    try:
        types = DeviceType.load_all(conn)
        for dt in types:
            print(f"  [{dt.device_type_id}] {dt.device_type_name}")
    except NotFoundError:
        print("  No device types found.")
        wait()
        return

    print_separator()
    try:
        type_id = int(prompt("Enter device type ID"))
        templates = TestTemplate.load_by_device(conn, type_id)
        print()
        for t in templates:
            print(f"  [{t.test_template_id}] {t.test_template_name}")

        print_separator()
        template_id = int(prompt("Enter test template ID"))
        name = prompt("Requirement name")

        r = RequirementTemplate(None, template_id, name)
        r.save(conn)
        print(f"\n  Requirement template '{name}' created successfully.")
    except ValueError:
        print("  Invalid ID.")
    except DeviceManagerError as e:
        print(f"\n  Error: {e}")
    wait()


def action_delete_requirement_template(conn):
    print_header("Delete Requirement Template")
    try:
        types = DeviceType.load_all(conn)
        for dt in types:
            print(f"  [{dt.device_type_id}] {dt.device_type_name}")
    except NotFoundError:
        print("  No device types found.")
        wait()
        return

    print_separator()
    try:
        type_id = int(prompt("Enter device type ID"))
        templates = TestTemplate.load_by_device(conn, type_id)
        print()
        for t in templates:
            print(f"  [{t.test_template_id}] {t.test_template_name}")

        print_separator()
        template_id = int(prompt("Enter test template ID"))
        req_templates = RequirementTemplate.load_by_test(conn, template_id)
        print()
        for r in req_templates:
            print(f"  [{r.requirement_template_id}] {r.requirement_name}")

        print_separator()
        id_input = int(prompt("Enter requirement template ID to delete"))
        r = RequirementTemplate.load(conn, id_input)
        confirm = prompt(f"Delete '{r.requirement_name}'? (yes/no)")
        if confirm.lower() == "yes":
            r.delete(conn)
            print("  Requirement template deleted.")
        else:
            print("  Cancelled.")
    except ValueError:
        print("  Invalid ID.")
    except DeviceManagerError as e:
        print(f"\n  Error: {e}")
    wait()


# ─────────────────────────────────────────────
# MAIN MENU
# ─────────────────────────────────────────────

def main():
    init_database()
    conn = get_connection()

    print("\n  Welcome to DeviceTestingManager")

    while True:
        print_header("Main Menu")
        print("  1. Device Types")
        print("  2. Devices")
        print("  3. Tests & Requirements")
        print("  4. Templates")
        print("  0. Exit")
        print_separator()

        choice = prompt("Select an option")

        if choice == "1":
            menu_device_types(conn)
        elif choice == "2":
            menu_devices(conn)
        elif choice == "3":
            menu_tests(conn)
        elif choice == "4":
            menu_templates(conn)
        elif choice == "0":
            print("\n  Goodbye.\n")
            conn.close()
            break
        else:
            print("  Invalid option.")


if __name__ == "__main__":
    main()
