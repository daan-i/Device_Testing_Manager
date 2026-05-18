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

def DevManMenu(conn):
    aux = -1
    print(""" **Choose a menu**
1. Create a new device
2. Modify a device
3. Show all devices
4. Show all devices in a location
5. Show all devices of a type
    """)

    aux = int(input("Choose a menu (1-6): "))

    while aux not in [1, 2, 3, 4, 5, 6]:
        aux = int(input("Invalid selection, please choose one of the available options:"))
