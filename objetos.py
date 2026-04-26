class DeviceType:
    def __init__(self, device_type_id = None, device_type_name = None, manufacturer = None):
        self.device_type_id = device_type_id
        self.device_type_name = device_type_name
        self.manufacturer = manufacturer

    def __repr__(self):
        return f"DeviceType, Id {self.device_type_id}, {self.device_type_name}, {self.manufacturer}"

    def save(self, conn):
        c = conn.cursor()
        if self.device_type_id is None:
            
            with conn:
                c.execute("INSERT INTO device_types (device_type_name, manufacturer) VALUES (:device_type_name, :manufacturer)" ,
                            {"device_type_name": self.device_type_name, 
                            "manufacturer": self.manufacturer})
            self.device_type_id = c.lastrowid
            print(f"Insertado device_type con id {self.device_type_id}")

        else:
            with conn:
                c.execute("""UPDATE device_types SET device_type_name = :device_type_name, manufacturer = :manufacturer 
                            WHERE device_type_id  = :device_type_id""",
                            {"device_type_name": self.device_type_name, 
                            "manufacturer": self.manufacturer,
                            "device_type_id": self.device_type_id})
                if c.rowcount == 0:
                    print("No se ha encontrado un objeto con ese id")
                else:
                    print(f"Actualizado device_type con id {self.device_type_id}")
                        
                
        

    @classmethod
    def load(cls, conn, id):
        c = conn.execute(
            "SELECT * FROM device_types WHERE device_type_id = :id",
            {"id": id})
        
        row = c.fetchone()
        
        if row is None:
            print("No se ha encontrado la fila")
            return None
        
        return cls(row[0], row[1], row[2])

    @classmethod
    def load_all(cls, conn):
        c = conn.execute("SELECT * FROM device_types")
        rows = c.fetchall()
        
        return [cls(row[0], row[1], row[2]) for row in rows] 
    
    @classmethod
    def load_by_manufacturer(cls, conn, manufacturer):
        c = conn.execute(
            "SELECT * FROM device_types WHERE manufacturer = :manufacturer",
            {"manufacturer": manufacturer}
        )
        
        rows = c.fetchall()
        
        return [cls(row[0], row[1], row[2]) for row in rows]
    
    @classmethod
    #Comprueba que el id exite, util para test_template
    def exists(cls, conn, id):

        c = conn.cursor()
        c.execute("SELECT 1 FROM device_types WHERE device_type_id = :device_type_id",
                 {"device_type_id": id})
        row = c.fetchone()
        if row is None:
            return False
        else:
            return True
        

    def delete(self, conn):
         # Comprueba que el objeto tenga id, el resto de parametros dan igual
        if self.device_type_id is not None:

            with conn:
                cursor = conn.execute(
                    "DELETE FROM device_types WHERE device_type_id = :device_type_id",
                    {"device_type_id": self.device_type_id}
                )
            #Comprueba que el cursor ha modificado alguna fila, si no manda el mensaje
            #Esto es mas eficiente que comprobar si el objeto existe y luego eliminarlo porque solo se hace una query
            if cursor.rowcount == 0:
                print("No se ha encontrado un objeto con ese id")
            else:
                print(f"Borrado device_type con id {self.device_type_id}")
                self.device_type_id = None

        else:
            print("El objeto tiene una id nula, no se puede borrar")




    def change_devtype_name(self, device_type_name):
        self.device_type_name = device_type_name
    
    def change_devtype_manufacturer(self, manufacturer):
        self.manufacturer = manufacturer

class TestTemplate:
    def __init__(self, test_template_id = None, device_type_id = None, test_template_name = None, test_description = None):
        self.test_template_id = test_template_id
        self.device_type_id = device_type_id
        self.test_template_name = test_template_name
        self.test_description = test_description

    def __repr__(self):
        return f"TestTemplate, Id {self.test_template_id}, {self.device_type_id}, {self.test_template_name}, {self.test_description}"
    
    def save(self, conn):
        c = conn.cursor()
        if not DeviceType.exists(conn, self.device_type_id):
            print("El device al que se esta intentando relacionar este test no existe o no es valido")
            return
        else:
            if self.test_template_id is None:
                
                with conn:
                    c.execute("INSERT INTO test_templates (device_type_id, test_template_name, test_description) VALUES (:device_type_id, :test_template_name, :test_description)" ,
                                {"device_type_id": self.device_type_id, 
                                "test_template_name": self.test_template_name,
                                "test_description": self.test_description})
                self.test_template_id = c.lastrowid
                print(f"Insertado test_template con id {self.test_template_id}")

            else:
                with conn:
                    c.execute("""UPDATE test_templates SET device_type_id = :device_type_id, test_template_name = :test_template_name, test_description = :test_description 
                                WHERE test_template_id  = :test_template_id""",
                                {"device_type_id": self.device_type_id, 
                                "test_template_name": self.test_template_name,
                                "test_description": self.test_description,
                                "test_template_id": self.test_template_id})
                    if c.rowcount == 0:
                        print("No se ha encontrado un objeto con ese id")
                    else:
                        print(f"Actualizado test_template con id {self.test_template_id}")


    @classmethod
    def load(cls, conn, id):
        c = conn.execute(
            "SELECT * FROM test_templates WHERE test_template_id = :id",
            {"id": id})
        
        row = c.fetchone()
        
        if row is None:
            print("No se ha encontrado la fila")
            return None
        
        return cls(row[0], row[1], row[2], row[3])

    @classmethod
    def load_all(cls, conn):
        c = conn.execute("SELECT * FROM test_templates")
        rows = c.fetchall()
        
        return [cls(row[0], row[1], row[2], row[3]) for row in rows] 
    
    @classmethod
    def load_by_device(cls, conn, device_type_id):

        c = conn.execute(
            "SELECT * FROM test_templates WHERE device_type_id = :device_type_id",
            {"device_type_id": device_type_id}
        )
        
        rows = c.fetchall()
        
        return [cls(row[0], row[1], row[2], row[3]) for row in rows]
    
    @classmethod
    #Comprueba que el id exite, util para requirements_templates
    def exists(cls, conn, id):

        c = conn.cursor()
        c.execute("SELECT 1 FROM test_templates WHERE test_template_id = :test_template_id",
                 {"test_template_id": id})
        row = c.fetchone()
        if row is None:
            return False
        else:
            return True
        
    def delete(self, conn):
         # Comprueba que el objeto tenga id, el resto de parametros dan igual
        if self.test_template_id is not None:

            with conn:
                cursor = conn.execute(
                    "DELETE FROM test_templates WHERE test_template_id = :test_template_id",
                    {"test_template_id": self.test_template_id}
                )
            #Comprueba que el cursor ha modificado alguna fila, si no manda el mensaje
            #Esto es mas eficiente que comprobar si el objeto existe y luego eliminarlo porque solo se hace una query
            if cursor.rowcount == 0:
                print("No se ha encontrado un objeto con ese id")
            else:
                print(f"Borrado test_template con id {self.test_template_id}")
                self.test_template_id = None

        else:
            print("El objeto tiene una id nula, no se puede borrar")

    def change_device_type_id(self, conn, id):
        if not DeviceType.exists(conn, id):
            print("El device al que se esta intentando relacionar este test no existe o no es valido")
            return
        else:
            self.device_type_id = id
    
    def change_test_name(self, name):
        self.test_template_name = name

    def change_description(self, description):
        self.test_description = description

class RequirementTemplate:

    def __init__(self, requirement_template_id = None, test_template_id = None, requirement_name = None):
            
            self.requirement_template_id = requirement_template_id
            self.test_template_id = test_template_id
            self.requirement_name = requirement_name

    def __repr__(self):
        return f"RequirementTemplate, Id {self.requirement_template_id}, {self.test_template_id}, {self.requirement_name}"
    
    def save(self, conn):
        c = conn.cursor()
        if not TestTemplate.exists(conn, self.test_template_id):
            print("El test al que se esta intentando relacionar este test no existe o no es valido")
            return
        else:
            if self.requirement_template_id is None:
                
                with conn:
                    c.execute("INSERT INTO requirement_templates (test_template_id, requirement_name) VALUES (:test_template_id, :requirement_name)" ,
                                {"test_template_id": self.test_template_id, 
                                "requirement_name": self.requirement_name})
                self.requirement_template_id = c.lastrowid
                print(f"Insertado requirement_template con id {self.requirement_template_id}")

            else:
                with conn:
                    c.execute("""UPDATE requirement_templates SET test_template_id = :test_template_id, requirement_name = :requirement_name
                                WHERE requirement_template_id  = :requirement_template_id""",
                                {"test_template_id": self.test_template_id, 
                                "requirement_name": self.requirement_name,
                                "requirement_template_id": self.requirement_template_id})
                    if c.rowcount == 0:
                        print("No se ha encontrado un objeto con ese id")
                    else:
                        print(f"Actualizado requirement_template con id {self.requirement_template_id}")

    @classmethod
    def load(cls, conn, id):
        c = conn.execute(
            "SELECT * FROM requirement_templates WHERE requirement_template_id = :id",
            {"id": id})
        
        row = c.fetchone()
        
        if row is None:
            print("No se ha encontrado la fila")
            return None
        
        return cls(row[0], row[1], row[2])

    @classmethod
    def load_all(cls, conn):
        c = conn.execute("SELECT * FROM requirement_templates")
        rows = c.fetchall()
        
        return [cls(row[0], row[1], row[2]) for row in rows] 
    
    @classmethod
    def load_by_test(cls, conn, test_template_id):

        c = conn.execute(
            "SELECT * FROM requirement_templates WHERE test_template_id = :test_template_id",
            {"test_template_id": test_template_id}
        )
        
        rows = c.fetchall()
        
        return [cls(row[0], row[1], row[2]) for row in rows]
    
    @classmethod
    #Comprueba que el id exite, util para test
    def exists(cls, conn, id):

        c = conn.cursor()
        c.execute("SELECT 1 FROM requirement_templates WHERE requirement_template_id = :requirement_template_id",
                 {"requirement_template_id": id})
        row = c.fetchone()
        if row is None:
            return False
        else:
            return True
    
    def delete(self, conn):
         # Comprueba que el objeto tenga id, el resto de parametros dan igual
        if self.requirement_template_id is not None:

            with conn:
                cursor = conn.execute(
                    "DELETE FROM requirement_templates WHERE requirement_template_id = :requirement_template_id",
                    {"requirement_template_id": self.requirement_template_id}
                )
            #Comprueba que el cursor ha modificado alguna fila, si no manda el mensaje
            #Esto es mas eficiente que comprobar si el objeto existe y luego eliminarlo porque solo se hace una query
            if cursor.rowcount == 0:
                print("No se ha encontrado un objeto con ese id")
            else:
                print(f"Borrado requirement_template con id {self.requirement_template_id}")
                self.requirement_template_id = None

        else:
            print("El objeto tiene una id nula, no se puede borrar")

    def change_test_template_id(self, conn, id):
        if not TestTemplate.exists(conn, id):
            print("El test al que se esta intentando relacionar este requerimiento no existe o no es valido")
            return
        else:
            self.test_template_id = id

    def change_requirement_name(self, name):
        self.requirement_name = name

class Device:
    def __init__(self, device_id=None, device_type_id=None, device_name=None, serial_number=None, 
                 device_location=None, device_status=None, device_observations=None):

        self.device_id = device_id
        self.device_type_id = device_type_id
        self.device_name = device_name
        self.serial_number = serial_number
        self.device_location = device_location
        self.device_status = device_status
        self.device_observations = device_observations

    def __repr__(self):
        return f"Device(Id={self.device_id}, Type={self.device_type_id}, Name={self.device_name}, SN={self.serial_number}, Location={self.device_location}, Status={self.device_status})"
    #La idea es que los cambios se hagan con el objeto de aqui arriba, los datos a cambiar se meten en el con los metodos de ahora, y luego en el save
    #se hace un update de los valores que no son None, hay que cambir los templates luego

    def change_device_type_id(self, conn, id):
        #Para esto usamos el exist de antes, si no existe habria que meter una excepcion, problema de futuro
        if(DeviceType.exists(conn, id)):
            self.device_type_id = id
        else:
            print("Placeholder, meter exception aqui, device_type_id invalido")
    
    def change_name(self, name):
        self.device_name = name
    
    def change_serial_number(self, serial_number):
        self.serial_number = serial_number
    
    def change_location(self, device_location):
        self.device_location = device_location
    
    def update_status(self, conn):
        #Placeholder, device status dependera de test_status
        return
    
    def change_observations(self, observation):
        self.device_observations = observation

    def save(self, conn):
        c = conn.cursor()
        if self.device_type_id is not None and not DeviceType.exists(conn, self.device_type_id):
            print("El device_type no existe o no es valido")
            print("Placeholder jeje, meter excepcion")
            return
        else:
            if self.device_id is None:
                
                with conn:
                    c.execute("""INSERT INTO devices (device_name, device_type_id, serial_number, device_location, device_status, device_observations)
                                 VALUES (:device_name, :device_type_id, :serial_number, :device_location, :device_status, :device_observations)""" ,
                                {"device_name": self.device_name,
                                "device_type_id": self.device_type_id,
                                "serial_number": self.serial_number,
                                "device_location": self.device_location,
                                "device_status": self.device_status,
                                "device_observations": self.device_observations})
                self.device_id = c.lastrowid
                print(f"Insertado device con id {self.device_id}")

                for t in TestTemplate.load_by_device(conn, self.device_type_id):
                    a = Test(None, self.device_id, t.test_template_id, None, None)
                    a.save(conn)

            else:
                with conn:
                    c.execute("""UPDATE devices
                                SET 
                                    device_name = COALESCE(:device_name, device_name),
                                    serial_number = COALESCE(:serial_number, serial_number),
                                    device_location = COALESCE(:device_location, device_location),
                                    device_status = COALESCE(:device_status, device_status),
                                    device_observations = COALESCE(:device_observations, device_observations)
                                WHERE device_id = :device_id;""",
                                {"device_id": self.device_id,
                                "device_name": self.device_name,
                                "serial_number": self.serial_number,
                                "device_location": self.device_location,
                                "device_status": self.device_status,
                                "device_observations": self.device_observations})
                    if c.rowcount == 0:
                        print("No se ha encontrado un objeto con ese id")
                    else:
                        print(f"Actualizado device con id {self.device_id}")

    @classmethod
    def load(cls, conn, id):
        c = conn.execute("""SELECT device_id, device_type_id, device_name, serial_number,
                                device_location, device_status, device_observations
                            FROM devices WHERE device_id = :id""",
                        {"id": id})
        
        row = c.fetchone()
        
        if row is None:
            print("No se ha encontrado la fila")
            return None
        
        return cls(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
    
    @classmethod
    def load_all(cls, conn):
        c = conn.execute("""SELECT device_id, device_type_id, device_name, serial_number,
                                device_location, device_status, device_observations
                            FROM devices""")
        rows = c.fetchall()
        
        return [cls(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in rows] 
    
    @classmethod
    def load_by_type(cls, conn, id):
        if DeviceType.exists(conn, id):
            c = conn.execute("""SELECT device_id, device_type_id, device_name, serial_number,
                                    device_location, device_status, device_observations
                                FROM devices WHERE device_type_id = :device_type""",
                                {"device_type": id})
            rows = c.fetchall()

            return [cls(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in rows] 
        else:
            print("Placeholder, la id a cargar no es valida, meter excepcion")
            return
        
    @classmethod
    def load_by_location(cls, conn, location):
        c = conn.execute("""SELECT device_id, device_type_id, device_name, serial_number,
                                   device_location, device_status, device_observations
                            FROM devices WHERE device_location = :device_location""",
                             {"device_location": location})
        rows = c.fetchall()
        
        if not rows:
            print("Placeholder, No existe dispositivo en esa localizacion, meter excepcion")
            return
        else:
            return[cls(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in rows]
    
    @classmethod
    #Comprueba que el id exite, util para test
    def exists(cls, conn, id):

        c = conn.cursor()
        c.execute("SELECT 1 FROM devices WHERE device_id = :device_id",
                 {"device_id": id})
        row = c.fetchone()
        if row is None:
            return False
        else:
            return True
    
    def delete(self, conn):
         # [HECHO] Hay que ver si interesa meter aqui que borre sus tests y requiremets, primero haria falta el metodo para borrar los test
         # [REVIEW] Ya lo hacia solo el sql, no hace falta asi que lo borro
         # Comprueba que el objeto tenga id, el resto de parametros dan igual
        

        if self.device_id is not None:
        
            with conn:
                cursor = conn.execute(
                    "DELETE FROM devices WHERE device_id = :device_id",
                    {"device_id": self.device_id}
                )
            #Comprueba que el cursor ha modificado alguna fila, si no manda el mensaje
            #Esto es mas eficiente que comprobar si el objeto existe y luego eliminarlo porque solo se hace una query
            if cursor.rowcount == 0:
                print("No se ha encontrado un device con ese id")
            else:
                print(f"Borrado device con id {self.device_id}")
                self.device_id = None

        else:
            print("El device tiene una id nula, no se puede borrar")
    
    def get_template(self, conn):
        return DeviceType.load(conn, self.device_type_id)

class Test:
    def __init__(self, test_id = None, device_id = None, test_template_id = None, test_status = None, test_observations = None):
        
        self.test_id = test_id
        self.device_id = device_id
        self.test_template_id = test_template_id
        self.test_status = test_status
        self.test_observations = test_observations
    
    def __repr__(self):
        return f"Test(Id={self.test_id}, Device={self.device_id}, Template={self.test_template_id}, Status={self.test_status}, Obs={self.test_observations})"

    def change_device_id(self, conn, id):

        if Device.exists(conn, id):
            self.device_id = id
        else:
            print("Placeholder, meter excepcion, device_id invalido")

    def change_template_id(self,conn, template_id):
        if TestTemplate.exists(conn, template_id):
            self.test_template_id = template_id
        else:
            print("Placeholder, meter excepcion, test_template_id invalido")

    def update_status(self):
        #Dependera de los requirements, hacer despues
        return
    
    def change_observations(self, observations):
        self.test_observations = observations

    def save(self, conn):
        c = conn.cursor()
        if self.device_id is not None and not Device.exists(conn, self.device_id):
            print("El device no existe o no es valido")
            print("Placeholder jeje, meter excepcion")
            return
        elif self.test_template_id is not None and not TestTemplate.exists(conn, self.test_template_id):
            print("El test_template no existe o no es valido")
            print("Placeholder jeje, meter excepcion")
            return
        else:
            if self.test_id is None:
                
                with conn:
                    c.execute("""INSERT INTO tests (device_id, test_template_id, test_status, test_observations)
                                 VALUES (:device_id, :test_template_id, :test_status, :test_observations)""" ,
                                {"device_id": self.device_id,
                                "test_template_id": self.test_template_id,
                                "test_status": self.test_status,
                                "test_observations": self.test_observations})
                self.test_id = c.lastrowid
                print(f"Insertado test con id {self.test_id}")

                for r in RequirementTemplate.load_by_test(conn, self.test_template_id):
                    a = Requirement(None, self.test_id, r.requirement_template_id, False)
                    a.save(conn)

            else:
                with conn:
                    c.execute("""UPDATE tests
                                SET
                                    test_status = COALESCE(:test_status, test_status),
                                    test_observations = COALESCE(:test_observations, test_observations)
                                WHERE test_id = :test_id;""",
                                {"test_id": self.test_id,
                                "test_status": self.test_status,
                                "test_observations": self.test_observations})
                    if c.rowcount == 0:
                        print("No se ha encontrado un objeto con ese id")
                    else:
                        print(f"Actualizado test con id {self.test_id}")

    @classmethod
    def load(cls, conn, id):
        c = conn.execute("""SELECT test_id, device_id, test_template_id, test_status, test_observations
                            FROM tests WHERE test_id = :id""",
                        {"id": id})
        
        row = c.fetchone()
        
        if row is None:
            print("No se ha encontrado la fila")
            return None
        
        return cls(row[0], row[1], row[2], row[3], row[4])
    
    @classmethod
    def load_all(cls, conn):
        c = conn.execute("""SELECT test_id, device_id, test_template_id, test_status, test_observations
                            FROM tests""")
        rows = c.fetchall()
        
        return [cls(row[0], row[1], row[2], row[3], row[4]) for row in rows] 
    
    @classmethod
    def load_by_device(cls, conn, id):
        if Device.exists(conn, id):
            c = conn.execute("""SELECT test_id, device_id, test_template_id, test_status, test_observations
                                FROM tests WHERE device_id = :device_id""",
                                {"device_id": id})
            rows = c.fetchall()

            return [cls(row[0], row[1], row[2], row[3], row[4]) for row in rows] 
        else:
            print("Placeholder, la id a cargar no es valida, meter excepcion")
            return

    @classmethod
    #Comprueba que el id exite, util para test
    def exists(cls, conn, id):

        c = conn.cursor()
        c.execute("SELECT 1 FROM tests WHERE test_id = :test_id",
                 {"test_id": id})
        row = c.fetchone()
        if row is None:
            return False
        else:
            return True
        
    def delete(self, conn):
         # Comprueba que el objeto tenga id, el resto de parametros dan igual
        if self.test_id is not None:

            with conn:

                cursor = conn.execute(
                    "DELETE FROM tests WHERE test_id = :test_id",
                    {"test_id": self.test_id}
                )
            #Comprueba que el cursor ha modificado alguna fila, si no manda el mensaje
            #Esto es mas eficiente que comprobar si el objeto existe y luego eliminarlo porque solo se hace una query
            if cursor.rowcount == 0:
                print("No se ha encontrado un test con ese id")
            else:
                print(f"Borrado test con id {self.test_id}")
                self.test_id = None

        else:
            print("El test tiene una id nula, no se puede borrar")

    @classmethod
    def delete_by_device(cls, conn, device_id):
        # Comprueba que el device exista
        if Device.exists(conn, device_id):

            with conn:
                cursor = conn.execute(
                    "DELETE FROM tests WHERE device_id = :device_id",
                    {"device_id": device_id}
                )

            # Comprueba si se ha borrado algo
            if cursor.rowcount == 0:
                print("No había tests para ese device")
            else:
                print(f"Borrados tests del device con id {device_id}")

        else:
            print("device_id inválido")

    def get_device(self, conn):
        return Device.load(conn, self.device_id)
    
    def get_template(self, conn):
        return TestTemplate.load(conn, self.test_template_id)

class Requirement:
    def __init__(self, requirement_id = None, test_id = None, requirement_template_id = None, requirement_status = False):
        
        self.requirement_id = requirement_id 
        self.test_id = test_id
        self.requirement_template_id = requirement_template_id
        self.requirement_status = requirement_status

    def __repr__(self):
        return f"Requirement(Id={self.requirement_id}, Template={self.requirement_template_id}, Test={self.test_id}, Status={self.requirement_status})"
    
    def change_test_id(self,conn, test_id):
        if Test.exists(conn, test_id):
            self.test_id = test_id
        else:
            print("Placeholder, meter excepcion, test_id invalido")
        
    def change_requirement_template_id(self, conn, requirement_template_id):
        if RequirementTemplate.exists(conn, requirement_template_id):
            self.requirement_template_id = requirement_template_id
        else:
            print("Placeholder, meter excepcion, requirement_template_id invalido")

    def change_status(self, status):
        self.requirement_status = status

    def save(self, conn):
        c = conn.cursor()
        if self.test_id is not None and not Test.exists(conn, self.test_id):
            print("El test no existe o no es valido")
            print("Placeholder jeje, meter excepcion")
            return
        elif self.requirement_template_id is not None and not RequirementTemplate.exists(conn, self.requirement_template_id):
            print("El requirement_template no existe o no es valido")
            print("Placeholder jeje, meter excepcion")
            return
        else:
            if self.requirement_id is None:
                
                with conn:
                    c.execute("""INSERT INTO requirements (test_id, requirement_template_id, requirement_status)
                                 VALUES (:test_id, :requirement_template_id, :requirement_status)""" ,
                                {"test_id": self.test_id,
                                "requirement_template_id": self.requirement_template_id,
                                "requirement_status": self.requirement_status})
                self.requirement_id = c.lastrowid
                print(f"Insertado requirement con id {self.requirement_id}")

            else:
                with conn:
                    c.execute("""UPDATE requirements
                                SET
                                    requirement_status = COALESCE(:requirement_status, requirement_status)                             
                                WHERE requirement_id = :requirement_id;""",
                                {"requirement_id": self.requirement_id,
                                "requirement_status": self.requirement_status})
                    if c.rowcount == 0:
                        print("No se ha encontrado un objeto con ese id")
                    else:
                        print(f"Actualizado requirement con id {self.requirement_id}")

    @classmethod
    def load(cls, conn, id):
        c = conn.execute("""SELECT requirement_id, test_id, requirement_template_id, requirement_status
                            FROM requirements WHERE requirement_id = :id""",
                        {"id": id})
        
        row = c.fetchone()
        
        if row is None:
            print("No se ha encontrado la fila")
            return None
        
        return cls(row[0], row[1], row[2], row[3])
    
    @classmethod
    def load_all(cls, conn):
        c = conn.execute("""SELECT requirement_id, test_id, requirement_template_id, requirement_status
                            FROM requirements""")
        rows = c.fetchall()
        
        return [cls(row[0], row[1], row[2], row[3]) for row in rows] 

    @classmethod
    def load_by_test(cls, conn, id):
        if Test.exists(conn, id):
            c = conn.execute("""SELECT requirement_id, test_id, requirement_template_id, requirement_status
                            FROM requirements WHERE test_id = :test_id""",
                                {"test_id": id})
            rows = c.fetchall()

            return [cls(row[0], row[1], row[2], row[3]) for row in rows] 
        else:
            print("Placeholder, la id a cargar no es valida, meter excepcion")
            return
        
    def delete(self, conn):
            # Comprueba que el objeto tenga id, el resto de parametros dan igual
            if self.requirement_id is not None:

                with conn:
                    cursor = conn.execute(
                        "DELETE FROM requirements WHERE requirement_id = :requirement_id",
                        {"requirement_id": self.requirement_id}
                    )
                #Comprueba que el cursor ha modificado alguna fila, si no manda el mensaje
                #Esto es mas eficiente que comprobar si el objeto existe y luego eliminarlo porque solo se hace una query
                if cursor.rowcount == 0:
                    print("No se ha encontrado un requirement con ese id")
                else:
                    print(f"Borrado requirement con id {self.requirement_id}")
                    self.requirement_id = None

            else:
                print("El requirement tiene una id nula, no se puede borrar")           

    @classmethod
    def delete_by_test(cls, conn, test_id):
        # Comprueba que el test exista
        if Test.exists(conn, test_id):

            with conn:
                cursor = conn.execute(
                    "DELETE FROM requirements WHERE test_id = :test_id",
                    {"test_id": test_id}
                )

            # Comprueba si se ha borrado algo
            if cursor.rowcount == 0:
                print("No había requirements para ese test")
            else:
                print(f"Borrados requirements del test con id {test_id}")

        else:
            print("test_id inválido")


    def get_test(self, conn):
        return Test.load(conn, self.test_id)

    def get_template(self, conn):
        return RequirementTemplate.load(conn, self.requirement_template_id)



