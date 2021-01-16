# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 13:30:28 2020

@author: Alexis Pincemin & Axel François
github : https://github.com/AxFrancois/Space-Invaders
"""

# %%----------------------Import----------------------------------------------#

from tkinter import PhotoImage


class Entity:
    """Classe qui défini toutes les Entitys du jeu"""

    def __init__(self, pPositionInitiale, pImage1, pWindow, pCanevas, pImage2=None):
        """
        Méthode de création d'une Entity. Elle a pour parametre
        pPositionInitiale, une liste de 2 entiers, pImage1 et pImage2 qui sont
        des str et qui indique les images de l'Entity.

        Parameters
        ----------
        pPositionInitiale : Liste de taille 2 contenant 2 entiers/int
            Contient les coordonnées de l'Entity. Elle permet de le positionner
            sur le canvas.
        pImage1 : String
            Nom de l'image 1 de l'Entity.
        pWindow : tkinter window
            Nécessaire pour l'interface graphique.
        pCanevas : tkinter canevas
            Idem.
        pImage2 : String, optional
            Nom de l'image 2 de l'Entity. Par défaut : None car certaines
            Entity n'ont qu'une seule image.
        Returns
        -------
        None.
        """

        self.Position = pPositionInitiale
        self.Frame1 = pImage1
        self.Frame2 = pImage2
        self.PixelArt = PhotoImage(master=pWindow, file='PixelArts/' + self.Frame1)
        self.imageOnCanvas = pCanevas.create_image(self.Position[0], self.Position[1], image=self.PixelArt)

    def getPos(self):
        """
        Méthode getteur pour récuperer la position de l'Entity
        Returns
        -------
         Liste de taille 2 contenant 2 entiers/int
            Coordonnées de l'Entity
        """

        return self.Position
