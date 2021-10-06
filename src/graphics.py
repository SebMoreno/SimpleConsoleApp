from covid_api import get_country


def per_capita():
    countries = get_country(multi=True)
    print(countries)


def life_expect():
    countries = get_country(multi=True)
    print(countries)


def co2_emissions():
    countries = get_country(multi=True)
    print(countries)
