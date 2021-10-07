from time import time
from unicodedata import normalize

import pandas as pd


def play(email):
    df = pd.read_csv("data/paisesYCapitales.csv", usecols=[1, 2], sep=";", index_col=0)
    countries2play = df.sample(8, random_state=1)
    countries2play["CAPITAL"] = countries2play["CAPITAL"].apply(normalize_string)
    start = time()
    answers = countries2play.apply(ask_capital, axis=1)
    end = time()
    lapse = end - start
    points = len(answers[answers["CAPITAL"] == answers["ANSWER"]])
    best = pd.read_csv("data/game_info.csv").sort_values(by=["points", "time"],
                                                         key=lambda x: x if x.name == "points" else -x,
                                                         ascending=False).iloc[0]
    if best.empty:
        best_msg = "Tu puntuación es la primera obtenida en este juego."
    else:
        best_msg = f"La mejor puntuación obtenida ha sido {best['points']}.\n\t" \
                   f"Fue obtenida por el usuario {best['email']} en {best['time']} segundos."
    print(best)
    print(f"""
    Usuario: {email}
    Puntuación: {points}
    Tiempo: {lapse} segundos

    {best_msg}
    """)
    # with open("data/game_info.csv", "a") as f:
    #     f.write(f"{email},{lapse},{points}")


def ask_capital(row):
    print(f"¿Cuál es la capital de {row.name}?")
    row["ANSWER"] = normalize_string(input("R/ "))
    return row


def normalize_string(string):
    return normalize("NFKD", string).encode('ASCII', 'ignore').decode("ASCII").strip().lower()
