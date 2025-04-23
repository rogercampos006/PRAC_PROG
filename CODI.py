import csv
import numpy as np
from abc import ABC, abstractmethod

class Recomanador(ABC):
    def __init__(self, dataset):
        self.dataset = dataset

class Simple(Recomanador):
    def __init__ (self, dataset, min_vots):
        super().__init__(dataset)
        self.min_vots = min_vots
        self.valoracions = None
    
    def get_valoracio (self):
        mask = self.dataset.ratings['rating'] > 0
        ratings_valides = self.dataset.ratings[mask]
        item_ids, num_vots = np.unique(ratings_valides['itemId'], return_counts=True)
        avg_items = [np.mean(ratings_valides[ratings_valides['itemId'] == item]['rating']) 
             for item in item_ids:
        valid_items = item_ids[num_vots >= self.min_vots]
        valid_avg = [avg_items[i] for i in range(len(item_ids)) if num_vots[i] >= self.min_vots]
        valid_vots = num_vots[num_vots >= self.min_vots]
        avg_global = np.mean(valid_avg)
        self.scores['score'] = ((valid_vots / (valid_vots + self.min_vots)) * valid_avg + (self.min_vots / (valid_vots + self.min_vots)) * avg_global)
        recomanacions = (
        self.scores[~self.scores['itemId'].isin(rated_items)].sort_values('score', ascending=False).head(k))
        return recomanacions[['itemId', 'score']].values.tolist()
   
    def recomana (self):
        if self.scores is None:
            self.calcular_scores()
        user_ratings = self.dataset.get_user_ratings(user_id)
        rated_items = user_ratings[user_ratings['rating'] > 0]['itemId']
        filtered_items = [(item, score) for item, score in zip(self.scores['itemId'], self.scores['score']) if item not in set(rated_items)]
class Colaboratiu(Recomanador):
    def __init__(self, dataset, k_similars):
        super().__init__(dataset)
        self.k_similars = k_similars
    
    def calcul_mitjana (self, id_usuari):
        valoracions = self.dataset.get_user_ratings(id_usuari)
        return n.mean(valoracions[valoracions['valoracio'] > 0]['valoracio'] )
    def recomana
class Dataset(ABC):
    """Classe abstracta base per a la gestió de conjunts de dades amb numpy"""
    
    def __init__(self):
        self.ratings = None  # Array estructurat: (userId, itemId, rating)
        self.items = None    # Array estructurat: (itemId, title, author, ...)
        
    @abstractmethod
    def load_data(self):
        pass
    
    def get_user_ratings(self, user_id):
        """Retorna les valoracions d'un usuari"""
        mask = self.ratings['userId'] == user_id
        return self.ratings[mask]
    
    def get_item_info(self, item_id):
        """Retorna informació completa d'un ítem"""
        mask = self.items['itemId'] == item_id
        return self.items[mask][0]  # Retorna la primera coincidència


class MovieLensDataset(Dataset):
    def load_data(self):
        # Lectura de ratings
        ratings_data = []
        with open("ratings.csv", 'r', encoding='utf8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                ratings_data.append((row[0], row[1], float(row[2])))
        
        self.ratings = np.array(
            ratings_data,
            dtype=[('userId', 'U15'), ('itemId', 'U15'), ('rating', 'f4')]
        )
        
        # Lectura de movies
        items_data = []
        with open(f"{self.data_path}/movies.csv", 'r', encoding='utf8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                items_data.append((row[0], row[1], row[2]))
        
        self.items = np.array(
            items_data,
            dtype=[('itemId', 'U15'), ('title', 'U150'), ('genres', 'U150')]
        )


class BookDataset(Dataset):
    def load_data(self):
        # Lectura de Books.csv
        items_data = []
        with open("Books.csv", 'r', encoding='latin1') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                # ISBN, Títol, Autor, Any, Editorial
                items_data.append((
                    row[0].strip(),       # ISBN
                    row[1].strip(),       # Títol
                    row[2].strip(),       # Autor
                    row[3].strip(),       # Any 
                    row[4].strip()        # Editorial
                ))
        
        self.items = np.array(
            items_data,
            dtype=[
                ('itemId', 'U15'), 
                ('title', 'U200'), 
                ('author', 'U100'), 
                ('year', 'U10'), 
                ('publisher', 'U100')
            ]
        )
        
        # Lectura de Ratings.csv
        ratings_data = []
        with open("Ratings.csv", 'r', encoding='utf8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                # User-ID, ISBN, Book-Rating
                if row[2] != '0':  # Ignorem valoracions 0 (segons especificacions)
                    ratings_data.append((row[0], row[1], float(row[2])))
        
        self.ratings = np.array(
            ratings_data,
            dtype=[('userId', 'U15'), ('itemId', 'U15'), ('rating', 'f4')]
        )
        
