import matplotlib.pyplot as plt
import pandas as pd


def per_capita():
    countries = pd.read_csv("data/income_per_person_gdppercapita_ppp_inflation_adjusted.csv",
                            index_col=0).rename_axis("País")
    country_selection = get_country_selection(countries.index.to_list())
    countries.T[country_selection].plot(xlabel="Año", ylabel="Dólares", title="Ingreso per capita")
    plt.show()


def life_expect():
    countries = pd.read_csv("data/life_expectancy_years.csv", index_col=0)
    country_selection = get_country_selection(countries.index.to_list())
    countries.T[country_selection].plot.bar(
        xlabel="Tiempo de vida (Años)",
        ylabel="Dólares",
        title="Expectativa de vida",
        subplots=True
    )
    countries.columns = countries.columns.astype(int)
    years = countries.columns.to_list()
    out = pd.cut(years, 5)
    out.value_counts().plot.bar(rot=0).set_xticklabels(
        [f"{int(cat.left)} a {int(cat.right)}" for cat in out.categories])
    plt.show()


def co2_emissions():
    countries = pd.read_csv("data/co2_emissions_tonnes_per_person.csv")
    country_selection = get_country_selection(countries.index.to_list())
    print(countries[countries["country"].isin(country_selection)])
    countries[
        countries["country"].isin(country_selection)
    ].plot.scatter(0, "2018", xlabel="País", ylabel="CO2/persona", title="Emisiones de CO2 por persona")
    plt.show()


def get_country_selection(countries):
    print("=================================")
    for i, c in enumerate(countries, 1):
        print(f"{i}. {c}")
    print("=================================")

    count = input("¿Cuántos países desea ingresar? (máximo 5): ")
    while not (count.isnumeric() and 1 <= int(count) <= 5):
        print("Ingresa un número entre 1 y 5")
        count = input("¿Cuántos países desea ingresar? (máximo 5): ")

    country_selection = []
    for _ in range(int(count)):
        country = input("Ingresa el número de un país de la lista anterior: ")
        while not (country.isnumeric() and 1 <= int(country) <= len(countries)):
            country = input("Ingresa un número válido de la lista de países: ")
        country_selection.append(int(country) - 1)
    return list(map(lambda co: countries[co], country_selection))
