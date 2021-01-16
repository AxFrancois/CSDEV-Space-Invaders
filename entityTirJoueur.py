# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 13:30:28 2020

@author: Alexis Pincemin & Axel François
github : https://github.com/AxFrancois/Space-Invaders
"""

# %%----------------------Import----------------------------------------------#

from tkinter import PhotoImage
import math, random
from entity import Entity


class EntityTirJoueur(Entity):
    """Sous-classe pour les tirs du joueur"""

    def afficherTirJoueur(self, pWindow, pCanevas):
        """
        Méthode d'affichage des Entitys. Les parametres pWindow et pCanevas
        sont respectivement la fenêtre et le canvas.
        Parameters
        ----------
        pWindow : tkinter window
            Nécessaire pour l'interface graphique
        pCanevas : tkinter canevas
            Idem
        Returns
        -------
        None.
        """
        self.PixelArt = PhotoImage(master=pWindow,
                                   file='PixelArts/' + self.Frame1)
        pCanevas.create_image(self.Position[0], self.Position[1],
                              image=self.PixelArt)

    def hitbox1(self, pListeDesEnnemis):
        """
        Méthode pour la détection des hitboxs. Le parametre pListeDesEnnemis
        est une liste dont chaque élément est une liste contenant tous les
        ennemis d'une ligne, EN COMMENCANT PAR LE LIGNE LA PLUS BASSE
        Parameters
        ----------
        pListeDesEnnemis : Liste de Liste de d'élement EntityEnnemiClassique
            Liste des ennemis en jeu.
        Returns
        -------
        bool
            True si un le projectile du joueur à touché un ennemi (pour le
                                                                   supprimer).
        Int
            Nombre de point gagné lors du kill.
        """
        for i, item in enumerate(pListeDesEnnemis):  # Pour chacune des lignes
            for j, ennemi in enumerate(item):
                distance = math.sqrt((ennemi.Position[0] - self.Position[0]) ** 2 +
                                     (ennemi.Position[1] - self.Position[1]) ** 2)
                if distance <= 10:
                    item.remove(ennemi)

                    if i == 0:
                        Points = 40
                    elif i in [1, 2]:
                        Points = 20
                    elif i in [3, 4]:
                        Points = 10
                    elif i == 5:
                        Points = random.choice([50, 100, 150, 200])

                    return True, Points
        return False, 0