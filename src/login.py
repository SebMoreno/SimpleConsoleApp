from db import users_db


def login(welcome=None):
    if welcome:
        print(welcome)
    email = input("Indica el email: ")
    user = next((i for i in users_db.users if i["email"] == email), None)
    while not user:
        print("El usuario no existe, por favor ingrese el email de un usuario registrado")
        email = input("Indica el email: ")
        user = next((i for i in users_db.users if i["email"] == email), None)
    password = input("Indica la contraseña: ")
    while password != user["password"]:
        print("Contraseña incorrecta, intenta de nuevo")
        password = input("Indica la contraseña: ")
    return user
