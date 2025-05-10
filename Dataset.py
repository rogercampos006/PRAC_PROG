from abc import ABC, abstractmethod
import csv
import numpy as np

class Dataset:
    def __init__(self, ratings_path, data_path, item_class):
        self.ratings_path = ratings_path
        self.data_path = data_path
        self.item_class = item_class


    def load_data(self):
        """ Carrega les dades de cada Ítem,les quals emmagatzema dins d'un 
        diccionari en el format { ID : Item (Objecte) } retorna doncs la 
        el diccionari dades"""

        items_dict = {}

        # Carregar dades des del fitxer
        with open(self.data_path, 'r') as data_file:
            csvreader = csv.DictReader(data_file)
            next(csvreader)
            for row in csvreader:
                # Crear l'ítem segons la classe detectada
                if self.item_class == Book:
                    ID = str(row['ISBN'])
                    title = row['Book-Title']
                    author = row['Book-Author']
                    any_publicacio = int(row['Year-Of-Publication'])
                    items_dict[ID] = Book(ID, title, author, any_publicacio)
                elif self.item_class == Movie:
                    ID = int(row['movieId'])
                    title = row['title']
                    genres = row['genres']
                    items_dict[ID] = Movie(ID, title, genres)
                else:
                    raise TypeError(f'L\'objecte de tipus {self.item_class} no és compatible')

        return items_dict

    def load_ratings(self):
        """Crea una matriu de valoracions on cada fila representa una pel·lícula
        i cada columna representa un usuari. Si no hi ha valoració, el valor serà 0.
        Retrona la matriu, un diccionari amb cada ID de l'usuari i el seu index a la matriu, 
        i un altre diccionari amb cada película, el seu id i el seu index a la matriu"""
    
        # Llegeix el fitxer de valoracions
        with open(self.ratings_path, 'r') as ratings_file:
            reader = csv.reader(ratings_file)
            header = next(reader)
        
            # Obtenim els IDs únics d'usuaris i pel·lícules
            user_ids = set()
            item_ids = set()
            ratings = []
        
            for row in reader:
                user_ids.add(int(row[0]))
                item_ids.add(str(row[1]))
                ratings.append((int(row[0]), str(row[1]), float(row[2])))
        
            # Ordenem els IDs per garantir consistència
            user_ids = sorted(user_ids)
            item_ids = sorted(item_ids)
        
            # Creem un diccionari per mapejar IDs a índexs
            user_index = {user_id: idx for idx, user_id in enumerate(user_ids)}
            item_index = {item_id: idx for idx, item_id in enumerate(item_ids)}
        
            # Inicialitzem la matriu de valoracions amb zeros
            ratings_matrix = np.zeros((len(item_ids), len(user_ids)))
        
            # Omplim la matriu amb les valoracions
            for user_id, movie_id, rating in ratings:
                row = item_index[movie_id]
                col = user_index[user_id]
                ratings_matrix[row, col] = rating
    
        return ratings_matrix, user_index, item_index



class Item(ABC):
    def __init__(self, ID, title):
        self.ID = ID
        self.title = title


class Book(Item):
    def __init__(self, ID, title, author, any_publicacio):
        super().__init__(ID, title)
        self.author = author
        self.any_publicacio = any_publicacio


class Movie(Item):
    def __init__(self, ID, title, genre):
        super().__init__(ID, title)
        self.genre = genre




