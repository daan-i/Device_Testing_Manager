-- Source - https://stackoverflow.com/a/5901100
-- Posted by Paul Lefebvre
-- Retrieved 2026-04-06, License - CC BY-SA 3.0

PRAGMA foreign_keys = ON;


CREATE TABLE device_types(
    device_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_type_name TEXT NOT NULL,
    manufacturer TEXT NOT NULL
);

CREATE TABLE test_templates(
    test_template_id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_type_id INTEGER,
    test_template_name TEXT NOT NULL,
    test_description TEXT NOT NULL,
    
    FOREIGN KEY (device_type_id) 
      REFERENCES device_types (device_type_id)
      ON DELETE CASCADE
);

CREATE TABLE requirement_templates(

    requirement_template_id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_template_id INTEGER,
    requirement_name TEXT,

    FOREIGN KEY (test_template_id) 
      REFERENCES test_templates (test_template_id)
      ON DELETE CASCADE
);

CREATE TABLE devices(

    device_id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_type_id INTEGER,
    device_name TEXT,
    serial_number TEXT,
    device_location TEXT,
    device_status TEXT,
    device_observations TEXT,

    FOREIGN KEY (device_type_id) 
      REFERENCES device_types (device_type_id)
    
);

CREATE TABLE tests(

    test_id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id INTEGER,
    test_template_id INTEGER, 
    test_status TEXT,
    test_observations TEXT,

    FOREIGN KEY (device_id) 
      REFERENCES devices (device_id)
      ON DELETE CASCADE,
    FOREIGN KEY (test_template_id) 
      REFERENCES test_templates (test_template_id),

    UNIQUE(device_id, test_template_id)
);

CREATE TABLE requirements(
    requirement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id INTEGER,
    requirement_template_id INTEGER,
    requirement_status TEXT,

    FOREIGN KEY (test_id) 
      REFERENCES tests (test_id)
      ON DELETE CASCADE,
    FOREIGN KEY (requirement_template_id) 
      REFERENCES requirement_templates (requirement_template_id),
    
    UNIQUE (test_id, requirement_template_id)
);