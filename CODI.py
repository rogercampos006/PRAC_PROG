import csv
import numpy as np
from abc import ABC, abstractmethod

class Recomanador(ABC):
    def __init__(self, dataset):
        self.dataset = dataset

class Simple(Recomana):
    def __init__ (self, dataset, min_vots):
        super().__init__(dataset)
        self.min_vots = min_vots
        self.valoracions = None
    
    def get_valoracio (self):
        valoracions_valides = self.dataset.caloracions[self.dataset.ratings['valoracio'] > 0]

class Colaboratiu(Recomana):

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



