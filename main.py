from Recomana import *
from Dataset import *
from abc import ABC, abstractmethod
import csv
import numpy as np


def main():
    # Crear una instància de Dataset
    dataset = Dataset(
    "/Users/bielp/Desktop/UAB/Assignatures/Programació Avançada/Projecte/Datasets/book_rating_prova.csv",
    "/Users/bielp/Desktop/UAB/Assignatures/Programació Avançada/Projecte/Datasets/book_prova.csv",
    Book) 

    # Carregar les dades
    items = dataset.load_data()

    # Veure el resultat
    print(items)
    print("Diccionari d'items: ")
    print(dataset.load_data())
    print("Matriu Valoracions: ")
    print(dataset.load_ratings()[0])

main()