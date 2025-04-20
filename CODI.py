import csv
import numpy as np

from abc import ABC

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

class Dataset:
    def __init__(self, arxiu):
        self.dades = np.matrix()
        self.arxiu = arxiu

    def import_data(self):
        #Llegir Dades i Afegir a la matriu


