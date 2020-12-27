# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 15:47:45 2020

@author: Axel François
"""
from tkinter import *

class Game:
    
    def __init__(self, pWindow, pCanevas):
        print("INIT")
        self.Vie = 3
        self.Score = 0
        self.Niveau = 1
        self.Window = pWindow
        self.Canevas = pCanevas
        self.TopScore = open('HighScore.txt', 'r')
        self.createEntities()
        self.Projectile = []
    
    def createEntities(self):
        self.Joueur = EntitéJoueur([50,450],'Player.gif', 'Player_mort.gif')
        self.Aliens1 = [EntitéEnnemiClassique([50 + i*40,50],'Alien_1_frame1.gif', 'Alien_1_frame2.gif') for i in range(11)]
        self.Aliens2 = [[EntitéEnnemiClassique([50 + i*40, 70 + j*20],'Alien_2_frame1.gif', 'Alien_2_frame2.gif') for i in range(11)] for j in range(2)]
        self.Aliens3 = [[EntitéEnnemiClassique([50 + i*40, 110 + j*20],'Alien_3_frame1.gif', 'Alien_3_frame2.gif') for i in range(11)] for j in range(2)]
    
    def clock_update(self, pFrame):
        self.Joueur.afficher(self.Window, self.Canevas)
        
        for item in self.Aliens1:
            item.afficher(self.Window, self.Canevas, pFrame)
            
        for k,liste in enumerate(self.Aliens2):
            for i,item in enumerate(liste):
                item.afficher(self.Window, self.Canevas, pFrame)
        
        for k,liste in enumerate(self.Aliens3):
            for i,item in enumerate(liste):
                item.afficher(self.Window, self.Canevas, pFrame)
        
        for item in self.Projectile:
            if isinstance(item, EntitéTirJoueur):
                item.Position = [item.Position[0], item.Position[1] - 10]
                if item.Position[1] < 0 : #Holala j'ai faillit faire un mémory leak en l'oubliant !!
                    self.Projectile.remove(item)
                item.afficher(self.Window, self.Canevas)
            
    def ActionJoueur(self, event):
        pKey = event.keysym
        #self.update()
        if pKey == "space":
            self.Projectile.append(EntitéTirJoueur([self.Joueur.getPos()[0],self.Joueur.getPos()[1] - 10], 'Projectile_joueur.gif'))
        elif pKey == "Right" or pKey == "Left":
            self.Joueur.Mouvement(pKey)
        #self.update()
        
class Entité:
    def __init__(self, pPositionInitiale, pImage1, pImage2 = None):
        self.Position =  pPositionInitiale
        self.Frame1 = pImage1
        self.Frame2 = pImage2
    
    def getPos(self):
        return self.Position
    
class EntitéEnnemiClassique(Entité):
     def afficher(self, pWindow, pCanevas, pFrame):
        if pFrame == 0:
            self.PixelArt = PhotoImage(master=pWindow, file='PixelArts/' + self.Frame1)
        else:
            self.PixelArt = PhotoImage(master=pWindow, file='PixelArts/' + self.Frame2)
        pCanevas.create_image(self.Position[0], self.Position[1], image=self.PixelArt)
    
class EntitéJoueur(Entité):
    def Mouvement(self, pKey):
        if pKey == "Right" and self.Position[0] < 600:
            self.Position[0] += 10
        elif pKey == "Left" and self.Position[0] > 50:
            self.Position[0] -= 10         
    def afficher(self, pWindow, pCanevas):
        #If player pas mort
        self.PixelArt = PhotoImage(master=pWindow, file='PixelArts/' + self.Frame1)
        pCanevas.create_image(self.Position[0], self.Position[1], image=self.PixelArt)
        #Else
        
class EntitéTirJoueur(Entité):        
    def afficher(self, pWindow, pCanevas):
        self.PixelArt = PhotoImage(master=pWindow, file='PixelArts/' + self.Frame1)
        pCanevas.create_image(self.Position[0], self.Position[1], image=self.PixelArt)   