# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 13:30:28 2020

@author: Alexis Pincemin & Axel François
github : https://github.com/AxFrancois/Space-Invaders
"""

# %%----------------------Import----------------------------------------------#

from tkinter import PhotoImage
from Classes.entity import Entity

class EntityPartieProtection(Entity):
    """Sous classe pour les blocs composant les protections"""

    def __init__(self, pCoordonne, pNumero, pWindow, pCanevas):
        """
        Méthode de création des blocs.

        Parameters
        ----------
        pCoordonne : Liste
            Liste de 2 entier. Coordonnée du bloc.
        pNumero : int
            Numéro de bloc. Permet de choisir quel texture afficher.
        pWindow : tkinter window
            Nécessaire pour l'interface graphique.
        pCanevas : tkinter canevas
            Idem.

        Returns
        -------
        None.

        """

        self.Position = pCoordonne
        self.Image0 = 'Protection{}-D0.gif'.format(pNumero) #Permet d'afficher chacune des 5 textures correspondant au dégats subbits
        self.Image1 = 'Protection{}-D1.gif'.format(pNumero)
        self.Image2 = 'Protection{}-D2.gif'.format(pNumero)
        self.Image3 = 'Protection{}-D3.gif'.format(pNumero)
        self.Image4 = 'Protection{}-D4.gif'.format(pNumero)
        self.DegatSubit = 0

        self.PixelArt = PhotoImage(master=pWindow,
                                   file='PixelArts/Protections/' + self.Image0)
        self.imageOnCanvas = pCanevas.create_image(self.Position[0], self.Position[1],
                                                   image=self.PixelArt) #Affichage sur le canevas

    def AffichageBloc(self, pWindow, pCanevas):
        """
        Méthode pour afficher les blocs avec l'image correspondant aux dégats qu'ils ont subit

        Parameters
        ----------
        pWindow : tkinter window
            Nécessaire pour l'interface graphique.
        pCanevas : tkinter canevas
            Idem.

        Returns
        -------
        None.

        """
        if self.DegatSubit == 0:    #Si le bloc a subit 0 dégat, etc...
            self.Image = self.Image0
        if self.DegatSubit == 1:
            self.Image = self.Image1
        elif self.DegatSubit == 2:
            self.Image = self.Image2
        elif self.DegatSubit == 3:
            self.Image = self.Image3
        elif self.DegatSubit == 4:
            self.Image = self.Image4

        self.PixelArt = PhotoImage(master=pWindow,
                                   file='PixelArts/Protections/' + self.Image)
        pCanevas.itemconfig(self.imageOnCanvas, image=self.PixelArt)