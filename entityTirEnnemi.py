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


class EntityTirEnnemi(Entity):
    """Sous-classe pour les tirs des aliens"""

    def afficherTirEnnemi(self, pWindow, pCanevas, pAlternateur):
        """
        Méthode d'affichage des Entités. Les parametres pWindow et pCanevas
        sont respectivement la fenêtre et le canvas.
        Parameters
        ----------
        pWindow : tkinter window
            Nécessaire pour l'interface graphique
        pCanevas : tkinter canevas
            Idem
        pAlternateur : Int
            1 ou 2 selon l'image à afficher. Permet l'annimation des
            projectiles ennemis.
        Returns
        -------
        None.
        """

        if pAlternateur == 1:
            self.PixelArt = PhotoImage(master=pWindow, file='PixelArts/' + self.Frame1)
        elif pAlternateur == 2:
            self.PixelArt = PhotoImage(master=pWindow, file='PixelArts/' + self.Frame2)
        pCanevas.itemconfig(self.imageOnCanvas, image=self.PixelArt)

    def hitbox2(self, pPositionJoueur, pTirPosition):
        """
        Méthode pour les hitbox du joueur. Permet de savoir si le joueur est
        touché par un tir

        Parameters
        ----------
        pPositionJoueur : Liste
            Liste de 2 entiers, renseigne les coordonnées du joueur.
        pTirPosition : Liste
             Liste de 2 entiers, renseigne les coordonnées du projectile alien.
        Returns
        -------
        bool
            True si le projectile a touché le joueur.
            False sinon.
        """

        distance = math.sqrt((pPositionJoueur[0] - pTirPosition[0]) ** 2 +
                             (pPositionJoueur[1] - pTirPosition[1]) ** 2)
        if distance <= 25:
            return True
        else:
            return False