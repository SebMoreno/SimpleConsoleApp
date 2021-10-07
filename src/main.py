import locale

import config
import covid_api
import game
import graphics
import login
from db import users_db


class Menu:
    def __init__(self, description, functions, exit_code):
        self.description = description
        self.functions = functions
        self.exit_code = exit_code

    def call_fun(self, option):
        if option in self.functions:
            self.functions[option]()
        else:
            print("Ingresa solo una de las opciones indicadas")


def start(menu):
    print(menu.description)
    option = input()
    while option != menu.exit_code:
        menu.call_fun(option)
        print(menu.description)
        option = input()


locale.setlocale(locale.LC_TIME, '')

welcome = """
============Bienvenido a SimpleConsoleApp============
A continuación inicia sesión con tu usuario
"""
if __name__ == "__main__":
    user = login.login(welcome)

    user_edit_self_menu = Menu("""
    a. Email
    b. Password
    c. Regresar
    """, {
        "a": lambda: config.edit("email", user),
        "b": lambda: config.edit("password", user)
    }, "c")

    admin_edit_user_menu = Menu("""
    a. Email
    b. Password
    c. Role
    d. Regresar""", {
        "a": lambda: config.edit("email"),
        "b": lambda: config.edit("password"),
        "c": lambda: config.edit("role")
    }, "d")

    user_config_menu = Menu("""
    a. Editar datos propios
    b. Regresar""", {
        "a": lambda: start(user_edit_self_menu)
    }, "b")

    admin_config_menu = Menu("""
    a. Agregar usuarios
    b. Editar
    c. Eliminar usuarios
    d. Regresar""", {
        "a": config.add,
        "b": lambda: start(admin_edit_user_menu),
        "c": config.delete
    }, "d")

    graphics_menu = Menu("""
    a. Ingreso per capita
    b. Expectativa de vida
    c. Emisiones de CO2
    d. Regresar""", {
        "a": graphics.per_capita,
        "b": graphics.life_expect,
        "c": graphics.co2_emissions
    }, "d")

    covid_api_menu = Menu("""
    a. Almacenar registros (csv)
    b. Estadísticos
    c. Regresar""", {
        "a": covid_api.save,
        "b": covid_api.stats
    }, "c")

    config_menu = admin_config_menu if user["role"] == "admin" else user_config_menu

    main_menu = Menu("""
    1. Configuración
    2. Gráficos
    3. Registros API Covid
    4. Juego
    5. Salir""", {
        "1": lambda: start(config_menu),
        "2": lambda: start(graphics_menu),
        "3": lambda: start(covid_api_menu),
        "4": lambda: game.play(user["email"]),
    }, "5")

    start(main_menu)

    users_db.save_users()
