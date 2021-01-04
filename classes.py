# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 15:47:45 2020

@author: Axel François
"""
from tkinter import *
import math
import random

def fAuBoutDuBout(pListeDesEnnemis, pDirectionPrecedente):  #Pour detecter si un alien a atteint un bord
    Moove = pDirectionPrecedente
    for i,item in enumerate(pListeDesEnnemis): #Pour chacune des lignes
        if item != []:
            if item[0].Position[0] <= 50: #Si l'ennemi le plus a gauche est trop proche de la limite
                Moove = "r"
            elif item[-1].Position[0] >= 600: #Si l'ennemi le plus a droite est trop proche de la limite
                Moove = "l"
    return Moove
        

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
        self.direction = "r"
        self.createSpecialEntities()
        self.spawnDelay = 0.6

    def createEntities(self):
        self.Joueur = EntitéJoueur([50,450],'Player.gif', 'Player_mort.gif')
        self.Aliens1 = [EntitéEnnemiClassique([50 + i*40,50],'Alien_1_frame1.gif', 'Alien_1_frame2.gif') for i in range(11)]
        self.Aliens2 = [[EntitéEnnemiClassique([50 + i*40, 70 + j*20],'Alien_2_frame1.gif', 'Alien_2_frame2.gif') for i in range(11)] for j in range(2)]
        self.Aliens3 = [[EntitéEnnemiClassique([50 + i*40, 110 + j*20],'Alien_3_frame1.gif', 'Alien_3_frame2.gif') for i in range(11)] for j in range(2)]

    def createSpecialEntities(self):
        self.Aliens4 = EntitéEnnemiSpeciale([50, 20], 'Alien_4.gif')
    
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
                kill = item.hitbox1(self.Canevas, [self.Aliens1, self.Aliens2[0], self.Aliens2[1], self.Aliens3[0], self.Aliens3[1]])
                if kill == True:
                    self.Projectile.remove(item)
                    self.Score += 10
                item.afficher(self.Window, self.Canevas)
        if pFrame > self.spawnDelay :
            self.Aliens4.afficherSpecial(self.Window, self.Canevas, 1)

    def position_ennemis_update(self):
        self.NouvelleDirection = fAuBoutDuBout([self.Aliens1, self.Aliens2[0], self.Aliens2[1], self.Aliens3[0], self.Aliens3[1]],self.direction)
        
        for item in self.Aliens1:
            item.sliding(self.direction,self.NouvelleDirection)
            
        for k,liste in enumerate(self.Aliens2):
            for i,item in enumerate(liste):
                item.sliding(self.direction,self.NouvelleDirection)
        
        for k,liste in enumerate(self.Aliens3):
            for i,item in enumerate(liste):
                item.sliding(self.direction,self.NouvelleDirection)
                
        self.direction = self.NouvelleDirection 
            
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

    
    def sliding(self, pAncienneDirection, pNouvelleDirection):
        if pNouvelleDirection != pAncienneDirection:
            self.Position = [self.Position[0], self.Position[1] + 30]  
        elif pNouvelleDirection == "r":
            self.Position = [self.Position[0] + 20, self.Position[1]]
        elif pNouvelleDirection == "l":
            self.Position = [self.Position[0] - 20, self.Position[1]]

class EntitéEnnemiSpeciale(Entité) :
    def afficherSpecial(self, pWindow, pCanevas, pX):
        self.PixelArt = PhotoImage(master=pWindow, file='PixelArts/' + self.Frame1)
        for i in range(0,20):
            pCanevas.create_image(50 + pX * i, 20, image=self.PixelArt)

    
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
        
    def hitbox1(self, pCanevas, pListeDesEnnemis):
        #collision = pCanevas.find_overlapping(self.Position[0]-5, self.Position[1]-5, self.Position[0]+5, self.Position[1]+5)
        for i,item in enumerate(pListeDesEnnemis): #Pour chacune des lignes
            for j,ennemi in enumerate(item):
                distance = math.sqrt((ennemi.Position[0]-self.Position[0]) ** 2 + (ennemi.Position[1]-self.Position[1]) ** 2 )
                if distance <= 10 : 
                    item.remove(ennemi)
                    return True
        return False        