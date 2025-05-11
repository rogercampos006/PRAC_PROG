import csv
import numpy as np
from abc import ABC, abstractmethod

import numpy as np
from math import sqrt
from abc import ABC

class Recomanador(ABC):
    def __init__(self, dataset):
        self.dataset = dataset



class RecomanadorSimple(Recomanador):
    """
    Es basa en calcular per cada ítem una valoració global basada en les puntuacions
    de tots els usuaris i ordenar els ítems encara no puntuats per l’usuari en funció
    d’aquesta valoració.
    """
    def __init__(self, dataset, min_vots=3):
        super().__init__(dataset)
        self.min_vots = min_vots

    def recomana(self, user_id):
        user_rated = set(self.dataset.get_user_ratings(user_id).keys())
        item_scores = []
        item_votes = {}
        item_avg = {}

        for item in self.dataset.items:
            if item in user_rated:
                continue
            votes = [r[item] for r in self.dataset.ratings.values() if item in r and r[item] > 0]
            if len(votes) >= self.min_vots:
                avg_item = np.mean(votes)
                item_votes[item] = len(votes)
                item_avg[item] = avg_item

        if not item_avg:
            return []

        avg_global = np.mean(list(item_avg.values()))

        for item, avg_item in item_avg.items():
            num_vots = item_votes[item]
            score = (num_vots / (num_vots + self.min_vots)) * avg_item + \
                    (self.min_vots / (num_vots + self.min_vots)) * avg_global
            item_scores.append((item, score))

        item_scores.sort(key=lambda x: -x[1])
        return item_scores


class RecomanadorColaboratiu(Recomanador):
    """"
    Es basa en trobar usuaris que hagin donat puntuacions similars als mateixos ítems
    que l’usuari pel que volem recomanar nous ítems.
    Les recomanacions a l’usuari es basaran en les puntuacions que hagin donat els
    usuaris més similars als ítems que el nou usuari encara no hagi valorat.
    """
    def __init__(self, dataset, k_similars=2):
        super().__init__(dataset)
        self.k_similars = k_similars

    def _sim_cosinus(self, u1, u2):
        common = set(u1.keys()) & set(u2.keys())
        if not common:
            return 0
        num = sum(u1[i] * u2[i] for i in common)
        den1 = sqrt(sum(u1[i] ** 2 for i in common))
        den2 = sqrt(sum(u2[i] ** 2 for i in common))
        return num / (den1 * den2) if den1 and den2 else 0

    def recomana(self, user_id):
        user_ratings = self.dataset.get_user_ratings(user_id)
        similars = []
        for other_id, ratings in self.dataset.ratings.items():
            if other_id == user_id:
                continue
            sim = self._sim_cosinus(user_ratings, ratings)
            if sim > 0:
                similars.append((other_id, sim))

        similars.sort(key=lambda x: -x[1])
        top_k = similars[:self.k_similars]

        mu_u = np.mean([r for r in user_ratings.values() if r > 0]) if user_ratings else 0
        pred = {}
        for item in self.dataset.items:
            if item in user_ratings:
                continue
            num, den = 0, 0
            for other_id, sim in top_k:
                other_ratings = self.dataset.get_user_ratings(other_id)
                if item in other_ratings:
                    mu_v = np.mean(list(other_ratings.values()))
                    num += sim * (other_ratings[item] - mu_v)
                    den += abs(sim)
            if den > 0:
                pred[item] = mu_u + num / den

        return sorted(pred.items(), key=lambda x: -x[1])

class Dataset:
    def __init__(self, data_route):
        self.data_route = data_route
        self.ratings = defaultdict(dict)  # userId -> {itemId: rating}
        self.items = {}  # itemId -> (title, genres)
        self.load_data()

    def load_data(self):
        with open(f"{self.data_route}/ratings.csv", 'r', encoding='utf8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user = int(row['userId'])
                item = int(row['movieId'])
                rating = float(row['rating'])
                self.ratings[user][item] = rating

        with open(f"{self.data_route}/movies.csv", 'r', encoding='utf8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                item = int(row['movieId'])
                title = row['title']
                genres = row['genres']
                self.items[item] = (title, genres)

    def get_user_ratings(self, user_id):
        return self.ratings.get(user_id, {})

class Item:
    def __init__(self, ID, titol, generes):
        self.ID = ID
        self.titol = titol
        self.generes = generes

    def __str__(self):
        return f"{self.titol} ({self.generes})"
    
class Movie(Item):
    def __init__(self, ID, titol, generes, director, any_estrena):
        super().__init__(ID, titol, generes)
        self.director = director
        self.any_estrena = any_estrena

    def __str__(self):
        return f"{self.titol} ({self.generes}) - Dir: {self.director}, {self.any_estrena}"

class Book (Item):
    def __init__(self, ID, titol, generes, autor, any_publicacio):
        super().__init__(ID, titol, generes)
        self.autor = autor
        self.any_publicacio = any_publicacio

    def __str__(self):
        return f"{self.titol} ({self.generes}) - {self.autor}, {self.any_publicacio}"

def main():
    print("=== SISTEMA DE RECOMANACIÓ ===")

    # Ruta del dataset
    data_dir = input("Introdueix la ruta del dataset (ex: ./ml-latest-small): ").strip()
    if not os.path.isdir(data_dir):
        print("Ruta no vàlida!")
        return

    # Carreguem dades
    dataset = Dataset(data_dir)

    # Triem recomanador
    tipus = input("Vols usar recomanador (s)imple o (c)ol·laboratiu? [s/c]: ").lower()
    if tipus == 's':
        min_vots = int(input("Introdueix el min_vots (nombre mínim de valoracions per ítem): "))
        recom = RecomanadorSimple(dataset, min_vots=min_vots)
    elif tipus == 'c':
        k = int(input("Introdueix el número k d'usuaris similars: "))
        recom = RecomanadorColaboratiu(dataset, k_similars=k)
    else:
        print("Opció no vàlida!")
        return

    # Triem usuari
    user_id = int(input("Introdueix l'ID de l'usuari: "))
    if user_id not in dataset.ratings:
        print("Usuari no trobat!")
        return

    # Obtenim recomanacions
    resultats = recom.recomana(user_id)

    # Mostrem resultats
    print(f"\nRecomanacions per a l'usuari {user_id}:")
    for item_id, score in resultats[:10]:  # Top 10
        titol, _ = dataset.get_item_info(item_id)
        print(f"{titol} → Puntuació estimada: {score:.2f}")

if __name__ == "__main__":
    main()
