from abc import ABC, abstractmethod
import csv
import numpy as np

class Dataset:
    def __init__(self, ratings_path, data_path, item_class):
        self.ratings_path = ratings_path
        self.data_path = data_path
        self.item_class = item_class


    def load_data(data_path, item_class):
        """ Carrega les dades de cada Ítem,les quals emmagatzema dins d'un 
        diccionari en el format { ID : Item (Objecte) } retorna doncs la 
        el diccionari dades"""

        items_dict = {}

        # Carregar dades des del fitxer
        with open(data_path, 'r') as data_file:
            csvreader = csv.reader(data_file)
            next(csvreader)
            for row in csvreader:
                # Crear l'ítem segons la classe detectada
                if item_class == Book:
                    ID = int(row['ISBN'])
                    title = row['Book-Title']
                    author = row['Book-Author']
                    any_publicacio = int(row['Year-Of-Publication'])
                    items_dict[ID] = Book(ID, title, author, any_publicacio)
                elif item_class == Movie:
                    ID = int(row['movieId'])
                    title = row['title']
                    genres = row['genres']
                    items_dict[ID] = Movie(ID, title, genres)
                else:
                    raise TypeError(f'L\'objecte de tipus {item_class} no és compatible')

        return items_dict

    def load_ratings(ratings_path, item_class):
        """Crea una matriu de valoracions on cada fila representa una pel·lícula
        i cada columna representa un usuari. Si no hi ha valoració, el valor serà 0."""
    
        # Llegeix el fitxer de valoracions
        with open(ratings_path, 'r') as ratings_file:
            reader = csv.reader(ratings_file)
            header = next(reader)
        
            # Obtenim els IDs únics d'usuaris i pel·lícules
            user_ids = set()
            movie_ids = set()
            ratings = []
        
            for row in reader:
                user_ids.add(int(row[0]))
                movie_ids.add(int(row[1]))
                ratings.append((int(row[0]), int(row[1]), float(row[2])))
        
            # Ordenem els IDs per garantir consistència
            user_ids = sorted(user_ids)
            movie_ids = sorted(movie_ids)
        
            # Creem un diccionari per mapejar IDs a índexs
            user_index = {user_id: idx for idx, user_id in enumerate(user_ids)}
            movie_index = {movie_id: idx for idx, movie_id in enumerate(movie_ids)}
        
            # Inicialitzem la matriu de valoracions amb zeros
            ratings_matrix = np.zeros((len(movie_ids), len(user_ids)))
        
            # Omplim la matriu amb les valoracions
            for user_id, movie_id, rating in ratings:
                row = movie_index[movie_id]
                col = user_index[user_id]
                ratings_matrix[row, col] = rating
    
        return ratings_matrix



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




