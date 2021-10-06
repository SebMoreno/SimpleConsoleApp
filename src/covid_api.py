import os
from calendar import monthrange
from datetime import datetime, MAXYEAR, MINYEAR

import pandas as pd
import requests


def save():
    country = get_country()
    status = get_status()
    date = get_date()
    registers = requests.get(
        f"https://api.covid19api.com/country/{country}/status/{status}?from=2020-03-01T00:00:00Z&to={date.isoformat()}"
    ).json()
    filename = f"src/data/{country}/{date.date()}.csv"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    pd.DataFrame(registers).to_csv(filename, index=False)
    print("La carpeta del país con el registro se encuentra en la carpeta 'data'\nArchivo creado: " + filename)


def stats():
    country = get_country()
    registers = requests.get(f"https://api.covid19api.com/country/{country}").json()
    df = pd.DataFrame(registers)
    print(f"""
Total de muertos: {df["Deaths"].sum()}
Total de contagiados: {df["Confirmed"].sum()}
Total de recuperados: {df["Recovered"].sum()}
Día de mayor contagio: {datetime.fromisoformat(df[df["Confirmed"] == df["Confirmed"].max()]["Date"].iloc[0][:-1])
          .strftime("%d de %B de %Y")}
Día de mayor mortandad: {datetime.fromisoformat(df[df["Deaths"] == df["Deaths"].max()]["Date"].iloc[0][:-1])
          .strftime("%d de %B de %Y")}""")


def get_country(multi=False):
    if multi:
        count = input("¿Cuántos países desea ingresar? (máximo 5): ")
        while not (count.isnumeric() and 1 <= int(count) <= 5):
            print("Ingresa un número entre 1 y 5")
            count = input("¿Cuántos países desea ingresar? (máximo 5): ")
    else:
        count = 1
    count = int(count)
    countries = sorted(requests.get("https://api.covid19api.com/countries").json(), key=lambda co: co["Country"])
    print("=================================")
    for i, c in enumerate(countries, 1):
        print(f"{i}. {c['Country']}")
    print("=================================")
    country_selection = []
    for _ in range(count):
        country = input("Ingresa el número de un país de la lista anterior: ")
        while not (country.isnumeric() and 1 <= int(country) <= len(countries)):
            country = input("Ingresa un número válido de la lista de países: ")
        country_selection.append(int(country) - 1)
    country_selection = list(map(lambda co: countries[co]["Slug"], country_selection))
    return country_selection if multi else country_selection[0]


def get_status():
    status_options = ["confirmed", "recovered", "deaths"]
    print("Elige uno de los siguientes estados posibles para consultar")
    for i, s in enumerate(status_options, 1):
        print(f"{i}. {s}")
    return status_options[int(input()) - 1]


def get_date():
    print("Se guardarán registros desde el 1 de marzo de 2020.")
    print("Ingresa la fecha hasta la cual quieres guardar los registros\n")
    year = input("Ingresa el año: ")
    while not (year.isnumeric() and MINYEAR <= int(year) <= MAXYEAR):
        year = input("Ingresa un año válido: ")

    month = input("Ingresa el mes: ")
    while not (month.isnumeric() and 1 <= int(month) <= 12):
        month = input("Ingresa un mes válido: ")

    day = input("Ingresa el día: ")
    while not (day.isnumeric() and 1 <= int(day) <= monthrange(int(year), int(month))[1]):
        day = input("Ingresa un día válido: ")

    return datetime(int(year), int(month), int(day))
