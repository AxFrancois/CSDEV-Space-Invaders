# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 15:47:45 2020

@author: Axel François
"""
from tkinter import *

class Game:
    def __init__(self):
        self.Vie = 3
        self.Score = 0
        self.TopScore = open('HighScore.txt', 'r')
    
    def createEntities(self):
        self.Joueur = EntitéJoueur([50,450],'Player.gif', 'Player_mort.gif', True)
        self.Aliens1 = [Entité([50 + i*20,50],'Alien_1_frame1.gif', 'Alien_2_frame1.gif', True) for i in range(11)]
        self.Aliens2 = [[Entité([50 + i*20, 70 + j*20],'Alien_2_frame1.gif', 'Alien_2_frame1.gif', True) for i in range(11)] for j in range(2)]
        self.Aliens3 = [[Entité([50 + i*20, 110 + j*20],'Alien_3_frame1.gif', 'Alien_3_frame1.gif', True) for i in range(11)] for j in range(2)]
    
    def update(self, pWindow, pCanevas):
        self.Joueur.afficher(pWindow, pCanevas)
        for item in self.Aliens1:
            item.afficher(pWindow, pCanevas)
        for k,liste in enumerate(self.Aliens2):
            for i,item in enumerate(liste):
                item.afficher(pWindow, pCanevas)
        for k,liste in enumerate(self.Aliens3):
            for i,item in enumerate(liste):
                item.afficher(pWindow, pCanevas)
      


class Entité:
    def __init__(self, pPositionInitiale, pImage1, pImage2, pJoueur = False):
        self.Position =  pPositionInitiale
        self.Frame1 = pImage1
        self.Frame2 = pImage2
        self.IsJoueur = pJoueur
    
    def afficher(self, pWindow, pCanevas):
        #return self.Position, self.Frame1
        self.PixelArt = PhotoImage(master=pWindow, file='PixelArts/' + self.Frame1)
        pCanevas.create_image(self.Position[0], self.Position[1], image=self.PixelArt)
    
    
class EntitéJoueur(Entité):    
    def afficher(self, pWindow, pCanevas):
        #If player pas mort
        self.PixelArt = PhotoImage(master=pWindow, file='PixelArts/' + self.Frame2)
        pCanevas.create_image(self.Position[0], self.Position[1], image=self.PixelArt)
        #Else
        
        