import re

from src.db import users_db


def add():
    print("A continuación se le pedirán los datos del nuevo usuario\n")
    new_user = {k: v() for k, v in user_functions.items()}
    users_db.add_user(new_user)
    print("Usuario agregado con éxito")


def edit(field, user=None):
    if not user:
        user = get_user("Ingresa el email del usuario que deseas editar: ")
    user[field] = user_functions[field]()
    users_db.save_users()
    print("Cambio realizado con éxito")


def delete():
    users_db.delete_user(get_user("Ingresa el email del usuario que deseas eliminar: "))
    print("Usuario borrado con éxito")


def get_user(input_message):
    email = input(input_message)
    user = next((u for u in users_db.users if u["email"] == email), None)
    while not user:
        print("El usuario ingresado no existe")
        email = input(input_message)
        user = next((u for u in users_db.users if u["email"] == email), None)
    return user


def get_id():
    next_id = len(users_db.users) + 1
    exist = next((u for u in users_db.users if u["id"] == str(next_id)), None)
    while exist:
        next_id += 1
        exist = next((u for u in users_db.users if u["id"] == str(next_id)), None)
    return str(next_id)


def get_email():
    email = input("El email debe contener un @ y terminar en '.com' o '.co'\nIngrésalo a continuación: ")
    while not email_re.match(email) and "," in email:
        print("Formato incorrecto")
        email = input("El email debe contener un @ y terminar en '.com' o '.co'\nIngrésalo a continuación: ")
    while next((i for i in users_db.users if i["email"] == email), None):
        print("El email ingresado ya ha sido usado, por favor usa uno diferente")
        email = input("Ingrésalo a continuación: ")
    return email


def get_password():
    accepted = False
    print("La contraseña debe tener mínimo 6 caracteres, un número y un carácter especial (!#$=%.)")
    password = "0000"
    while not accepted:
        password = input("Ingresa la contraseña a continuación: ")
        if not password_char_re.match(password):
            print("La contraseña debe tener mínimo 6 caracteres")
        elif not password_digit_re.search(password):
            print("La contraseña debe tener mínimo 1 número")
        elif not password_special_chars_re.search(password):
            print("La contraseña de tener mínimo un carácter especial (!#$=%.)")
        else:
            accepted = True
    return password


def get_role():
    is_admin = input("¿Este usuario es administrador? (S/N): ")
    while not role_re.match(is_admin):
        print("Escribe 'S' o 'N' para responder")
        is_admin = input("¿Este usuario es administrador? (S/N): ")
    return "admin" if is_admin == "S" or is_admin == "s" else "user"


email_re = re.compile(r"\w+@\w+\.com?")
password_char_re = re.compile(r"(.*[a-zA-Z].*){6,}")
password_digit_re = re.compile(r"\d")
password_special_chars_re = re.compile(r"[!#$=%.]")
role_re = re.compile("[SsNn]")
user_functions = {
    "id": get_id,
    "email": get_email,
    "password": get_password,
    "role": get_role
}
