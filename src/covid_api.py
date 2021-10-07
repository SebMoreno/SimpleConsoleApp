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
    filename = f"data/{country}/{date.date()}.csv"
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


def get_country():
    countries = sorted(requests.get("https://api.covid19api.com/countries").json(), key=lambda co: co["Country"])
    print("=================================")
    for i, c in enumerate(countries, 1):
        print(f"{i}. {c['Country']}")
    print("=================================")
    country = input("\nDe la lista anterior ingresa el país que deseas usar: ")
    while not (country.isnumeric() and 1 <= int(country) <= len(countries)):
        country = input("Ingresa un número válido de la lista de países: ")
    return countries[int(country) - 1]["Slug"]


def get_status():
    status_options = ["confirmed", "recovered", "deaths"]
    print("Elige uno de los siguientes estados posibles para consultar")
    for i, s in enumerate(status_options, 1):
        print(f"{i}. {s}")
    status = input("Escribe un número de los disponibles: ")
    while not (status.isnumeric() and 1 <= int(status) <= len(status_options)):
        print("Opción incorrecta")
        status = input("Escribe un número de los disponibles: ")
    print(status_options[int(status) - 1])
    return status_options[int(status) - 1]


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
