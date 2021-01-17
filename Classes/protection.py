# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 13:30:28 2020

@author: Alexis Pincemin & Axel François
github : https://github.com/AxFrancois/Space-Invaders
"""

# %%----------------------Import----------------------------------------------#

import math
from Classes.entityPartieProtection import EntityPartieProtection

class Protection:
    """classe pour les protections"""

    def __init__(self, pCoordonne, pWindow, pCanevas):
        """
        Méthode de création des protections.
        
        Les nombres magiques utilisé ici sont dût à la taille des images des blocs qui constitue les protections,
        à savoir 23, 6, 43, 15, 19 et 11

        Parameters
        ----------
        pCoordonne : Liste
            Liste de 2 entier. Coordonnée de la portection.
        pWindow : tkinter window
            Nécessaire pour l'interface graphique.
        pCanevas : tkinter canevas
            Idem.

        Returns
        -------
        None.

        """

        self.Position = pCoordonne
        
        self.bloc1 = EntityPartieProtection([pCoordonne[0], pCoordonne[1] + 23], 1, pWindow,
                                            pCanevas)  # Bloc bas gauche
        self.bloc2 = EntityPartieProtection([pCoordonne[0] + 43, pCoordonne[1] + 23], 1, pWindow,
                                            pCanevas)  # Bloc bas droite
        self.bloc3 = EntityPartieProtection([pCoordonne[0], pCoordonne[1] + 6], 2, pWindow,
                                            pCanevas)  # Bloc haut gauche
        self.bloc4 = EntityPartieProtection([pCoordonne[0] + 43, pCoordonne[1] + 6], 3, pWindow,
                                            pCanevas)  # Bloc haut droite
        self.bloc5 = EntityPartieProtection([pCoordonne[0] + 15, pCoordonne[1]], 4, pWindow,
                                            pCanevas)  # Bloc milieu haut gauche
        self.bloc6 = EntityPartieProtection([pCoordonne[0] + 29, pCoordonne[1]], 4, pWindow,
                                            pCanevas)  # Bloc milieu haut droite
        self.bloc7 = EntityPartieProtection([pCoordonne[0] + 15, pCoordonne[1] + 11], 5, pWindow,
                                            pCanevas)  # Bloc milieu bas droite
        self.bloc8 = EntityPartieProtection([pCoordonne[0] + 29, pCoordonne[1] + 11], 6, pWindow,
                                            pCanevas)  # Bloc milieu bas gauche
        self.listeBloc = [self.bloc1, self.bloc2, self.bloc3, self.bloc4,
                          self.bloc5, self.bloc6, self.bloc7, self.bloc8]

    def ProtectionDestruction(self, pCoordProjectile):
        """
        Méthode pour la destruction des éléments de la protection.

        Parameters
        ----------
        pCoordProjectile : Liste
            Liste de 2 entier. Coordonnée du projectile

        Returns
        -------
        bool
            Booléen pour savoir si le tir à détruit/endommagé un bloc.

        """

        for element in self.listeBloc:
            distance = math.sqrt((element.Position[0] - pCoordProjectile[0]) ** 2
                                 + (element.Position[1] - pCoordProjectile[1]) ** 2)    #norme entre le centre projectile et le centre bloc pour calculer la distance 
            if distance <= 10:  #La taille minimale des blocs est de 12x14 pixels donc si la distance est inférieure à 10 pixels le bloc doit être détruit
                element.DegatSubit += 1
                return True
        return False

    def affichageProtection(self, pWindow, pCanevas):
        """
        Méthode pour l'affichage des protections.

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

        for element in self.listeBloc:
            if element.DegatSubit >= 5: #Un bloc à 4 points de vie maxium, s'il a subit plus de 5 dégats on l'enlève
                self.listeBloc.remove(element)
                pCanevas.delete(element.imageOnCanvas)
            else:
                element.AffichageBloc(pWindow, pCanevas)