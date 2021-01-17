# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 13:30:28 2020

@author: Alexis Pincemin & Axel François
github : https://github.com/AxFrancois/Space-Invaders
"""

# %%----------------------Import----------------------------------------------#

from tkinter import PhotoImage
from Classes.entity import Entity


class EntityEnnemiClassique(Entity):
    """Sous-classe pour les ennemis classiques"""

    def afficherClassique(self, pWindow, pCanevas, pFrame):
        """
        Méthode pour le déplacement des ennemis. pAncienneDirection et
        pNouvelleDirection, qui valent 'l' ou 'r' indique quel a été la
        direction du précédent déplacement et de celui qui doit avoir lieu
        
        Parameters
        ----------
        pAncienneDirection : String
            'l' ou 'r', ancienne direction (permet de faire descendre les
                                            ennemis).
        pNouvelleDirection : String
            'l' ou 'r', nouvelle direction(permet de faire descendre les
                                           ennemis et de déplacer les ennemis à
                                           gauche ou à droite).
        pCanevas : tkinter canevas
            Nécessaire pour l'interface graphique.
            
        Returns
        -------
        None.
        """

        if pFrame == 0:
            self.PixelArt = PhotoImage(master=pWindow,
                                       file='PixelArts/' + self.Frame1)
        else:
            self.PixelArt = PhotoImage(master=pWindow,
                                       file='PixelArts/' + self.Frame2)
        pCanevas.itemconfig(self.imageOnCanvas, image=self.PixelArt)

    def slidingClassique(self, pAncienneDirection, pNouvelleDirection, pCanevas):
        """
        Méthode pour le déplacement des ennemis. pAncienneDirection et
        pNouvelleDirection, qui valent 'l' ou 'r' indique quel a été la
        direction du précédent déplacement et de celui qui doit avoir lieu
        
        Parameters
        ----------
        pAncienneDirection : String
            'l' ou 'r', ancienne direction (permet de faire descendre les
                                            ennemis).
        pNouvelleDirection : String
            'l' ou 'r', nouvelle direction(permet de faire descendre les
                                           ennemis et de déplacer les ennemis à
                                           gauche ou à droite).
        pCanevas : tkinter canevas
            Nécessaire pour l'interface graphique.
            
        Returns
        -------
        None.
        """

        if pNouvelleDirection != pAncienneDirection:
            pCanevas.move(self.imageOnCanvas, 0, 30)    #Déplacement des 30 pixels vers le bas
            self.Position = [self.Position[0], self.Position[1] + 30]   
        elif pNouvelleDirection == "r":
            pCanevas.move(self.imageOnCanvas, 20, 0)    #Déplacement des 30 pixels vers la droite
            self.Position = [self.Position[0] + 20, self.Position[1]]
        elif pNouvelleDirection == "l":
            pCanevas.move(self.imageOnCanvas, -20, 0)   #Déplacement des 30 pixels vers la gauche
            self.Position = [self.Position[0] - 20, self.Position[1]]