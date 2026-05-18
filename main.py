from objetos import *
from excepciones import *
from funcionalidad import *
from menusTerminal import *
#El estado es lo que le indica a la terminal en que pagina esta
state = 0 

#Iniciamos la conexion con la base de datos
conn = get_connection("database.db")

def update_state(conn, state):
    match state:
        case 0:
            update_state(mainMenu())

