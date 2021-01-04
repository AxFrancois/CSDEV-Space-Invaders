# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 15:47:45 2020

@author: Alexis Pincemin & Axel François
github : https://github.com/AxFrancois/Space-Invaders
"""
from tkinter import *
import math
import random

def fAuBoutDuBout(pListeDesEnnemis, pDirectionPrecedente):
    """Fonction qui détecte si les aliens sont proche d'un bord et doivent 
    changer de dirrection. Elle prend comme entrèe pListeDesEnnemis qui est une
    liste dont chaque élément est une liste contenant tous les ennemis d'une
    ligne et pDirectionPrecedente qui vaut soit l soit r. La fonction retourne 
    'l' ou 'r' qui est la direction vers laquelle les ennemis devrons se 
    diriger au prochain mouvement.

    Parameters
    ----------
    pListeDesEnnemis : TYPE
        DESCRIPTION.
    pDirectionPrecedente : TYPE
        DESCRIPTION.

    Returns
    -------
    Moove : TYPE
        DESCRIPTION.

    """
    
    Moove = pDirectionPrecedente
    for i,item in enumerate(pListeDesEnnemis): #Pour chacune des lignes
        if item != []:
            if item[0].Position[0] <= 50: 
                #Si l'ennemi le plus a gauche est trop proche de la limite
                Moove = "r"
            elif item[-1].Position[0] >= 600: 
                #Si l'ennemi le plus a droite est trop proche de la limite
                Moove = "l"
    return Moove
        

class Game:
    """Classe qui gère la partie."""
    
    def __init__(self, pWindow, pCanevas):
        """
        Méthode de création de la partie. Les parametres pWindow et pCanevas
        sont respectivement la fenêtre et le canvas de tkinter

        Parameters
        ----------
        pWindow : TYPE
            DESCRIPTION.
        pCanevas : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
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
        self.createProtection()

    def createEntities(self):
        """
        Méthode qui créée les entités du jeu, à savoir les ennemis et le 
        joueur

        Returns
        -------
        None.

        """
        
        self.Joueur = EntitéJoueur([50,450],'Player.gif', 'Player_mort.gif')
        self.Aliens1 = [EntitéEnnemiClassique([50 + i*40,50],
                        'Alien_1_frame1.gif', 'Alien_1_frame2.gif') for i in range(11)]
        self.Aliens2 = [[EntitéEnnemiClassique([50 + i*40, 70 + j*20],
                        'Alien_2_frame1.gif', 'Alien_2_frame2.gif') for i in range(11)] for j in range(2)]
        self.Aliens3 = [[EntitéEnnemiClassique([50 + i*40, 110 + j*20],
                        'Alien_3_frame1.gif', 'Alien_3_frame2.gif') for i in range(11)] for j in range(2)]

    def createSpecialEntities(self):
        self.Aliens4 = EntitéEnnemiSpeciale([50, 20], 'Alien_4.gif')

    def createProtection(self):
        self.Protect = [EntitéProtection([140 + i*120,400], 'Protection.gif') for i in range(4)]

    def clock_update(self, pFrame):
        """
        Méthode qui affiche les entités du jeu et gére les projectiles. Le 
        parametre pFrame, qui vaut 0 ou 1, indique s'il faut déplacer et 
        changer l'image des aliens.

        Parameters
        ----------
        pFrame : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """        
        
        self.Joueur.afficher(self.Window, self.Canevas)

        for item in self.Protect:
            item.afficherProtection(self.Window, self.Canevas)

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
                kill = item.hitbox1([self.Aliens1, self.Aliens2[0],
                                     self.Aliens2[1], self.Aliens3[0],
                                     self.Aliens3[1]])
                if kill == True:
                    self.Projectile.remove(item)
                    self.Score += 10
                item.afficher(self.Window, self.Canevas)
        if pFrame > self.spawnDelay :
            self.Aliens4.afficherSpecial(self.Window, self.Canevas, 1)

    def position_ennemis_update(self):
        """
        Méthode qui change la position des ennemis à chaque appel.

        Returns
        -------
        None.

        """
        
        self.NouvelleDirection = fAuBoutDuBout([self.Aliens1, self.Aliens2[0], 
                                                self.Aliens2[1], self.Aliens3[0],
                                                self.Aliens3[1]],self.direction)
        
        for item in self.Aliens1:
            item.sliding(self.direction,self.NouvelleDirection)
            
        for k,liste in enumerate(self.Aliens2):
            for i,item in enumerate(liste):
                item.sliding(self.direction,self.NouvelleDirection)
        
        for k,liste in enumerate(self.Aliens3):
            for i,item in enumerate(liste):
                item.sliding(self.direction,self.NouvelleDirection)
                
        self.direction = self.NouvelleDirection

    # def protection_update(self):

            
    def ActionJoueur(self, event):
        """
        Méthode qui détecte les pressions des touches du clavier pour 
        executer les commandes.

        Parameters
        ----------
        event : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
        pKey = event.keysym
        #self.update()
        if pKey == "space":
            self.Projectile.append(EntitéTirJoueur([self.Joueur.getPos()[0], 
                                                    self.Joueur.getPos()[1] - 10],
                                                   'Projectile_joueur.gif'))
        elif pKey == "Right" or pKey == "Left":
            self.Joueur.Mouvement(pKey)
        #self.update()


        
class Entité:
    """Classe qui défini toutes les entités du jeu"""
    
    def __init__(self, pPositionInitiale, pImage1, pImage2 = None):
        """
        Méthode de création d'une entité. Elle a pour parametre 
        pPositionInitiale, une liste de 2 entiers, pImage1 et pImage2 qui sont 
        des str et qui indique les images de l'entité

        Parameters
        ----------
        pPositionInitiale : TYPE
            DESCRIPTION.
        pImage1 : TYPE
            DESCRIPTION.
        pImage2 : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        """
        
        self.Position =  pPositionInitiale
        self.Frame1 = pImage1
        self.Frame2 = pImage2
    
    def getPos(self):
        """
        Méthode getteur pour récuperer la position de l'entité

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        
        return self.Position
    
class EntitéEnnemiClassique(Entité):
    """Sous-classe pour les ennemis classiques"""
    
    def afficher(self, pWindow, pCanevas, pFrame):        
        """
        Méthode d'affichage des entités. Les parametres pWindow et pCanevas
        sont respectivement la fenêtre et le canvas, et pFrame, qui vaut 0 ou
        1, indique quelle image afficher

        Parameters
        ----------
        pWindow : TYPE
            DESCRIPTION.
        pCanevas : TYPE
            DESCRIPTION.
        pFrame : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
        if pFrame == 0:
            self.PixelArt = PhotoImage(master = pWindow, 
                                       file = 'PixelArts/' + self.Frame1)
        else:
            self.PixelArt = PhotoImage(master = pWindow,
                                       file = 'PixelArts/' + self.Frame2)
        pCanevas.create_image(self.Position[0], self.Position[1],
                              image = self.PixelArt)

    
    def sliding(self, pAncienneDirection, pNouvelleDirection):
        """
        Méthode pour le déplacement des ennemis. pAncienneDirection et 
        pNouvelleDirection, qui valent 'l' ou 'r' indique quel a été la 
        direction du précédent déplacement et de celui qui doit avoir lieu

        Parameters
        ----------
        pAncienneDirection : TYPE
            DESCRIPTION.
        pNouvelleDirection : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
        if pNouvelleDirection != pAncienneDirection:
            self.Position = [self.Position[0], self.Position[1] + 30]  
        elif pNouvelleDirection == "r":
            self.Position = [self.Position[0] + 20, self.Position[1]]
        elif pNouvelleDirection == "l":
            self.Position = [self.Position[0] - 20, self.Position[1]]

class EntitéEnnemiSpeciale(Entité) :
    def afficherSpecial(self, pWindow, pCanevas, pX):
        """
        

        Parameters
        ----------
        pWindow : TYPE
            DESCRIPTION.
        pCanevas : TYPE
            DESCRIPTION.
        pX : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.PixelArt = PhotoImage(master = pWindow,
                                   file = 'PixelArts/' + self.Frame1)
        for i in range(0,20):
            pCanevas.create_image(50 + pX * i, 20, image = self.PixelArt)

class EntitéProtection(Entité):
    def afficherProtection(self, pWindow, pCanevas):
        """
        

        Parameters
        ----------
        pWindow : TYPE
            DESCRIPTION.
        pCanevas : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.PixelArt = PhotoImage(master = pWindow,
                                   file = 'PixelArts/' + self.Frame1)
        pCanevas.create_image(self.Position[0], self.Position[1],
                              image = self.PixelArt)

class EntitéJoueur(Entité):
    """Sous-classe pour le joueur"""
    
    def Mouvement(self, pKey):
        """
        Méthode pour le déplacement du joueur. Le parametre pKey est la touche pressé sur le clavier.  

        Parameters
        ----------
        pKey : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        if pKey == "Right" and self.Position[0] < 600:
            self.Position[0] += 10
        elif pKey == "Left" and self.Position[0] > 50:
            self.Position[0] -= 10         

    def afficher(self, pWindow, pCanevas):
        """
        Méthode d'affichage du joueur. Les parametres pWindow et pCanevas sont 
        respectivement la fenêtre et le canvas,

        Parameters
        ----------
        pWindow : TYPE
            DESCRIPTION.
        pCanevas : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        #If player pas mort
        self.PixelArt = PhotoImage(master = pWindow,
                                   file = 'PixelArts/' + self.Frame1)
        pCanevas.create_image(self.Position[0], self.Position[1],
                              image = self.PixelArt)
        #Else


class EntitéTirJoueur(Entité):        
    """Sous-classe pour les tirs du joueur"""
    
    def afficher(self, pWindow, pCanevas):
        """
        Méthode d'affichage des entités. Les parametres pWindow et pCanevas 
        sont respectivement la fenêtre et le canvas.

        Parameters
        ----------
        pWindow : TYPE
            DESCRIPTION.
        pCanevas : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.PixelArt = PhotoImage(master = pWindow,
                                   file = 'PixelArts/' + self.Frame1)
        pCanevas.create_image(self.Position[0], self.Position[1],
                              image = self.PixelArt)
        
    def hitbox1(self, pListeDesEnnemis):
        """
        Méthode pour la détection des hitboxs. Le parametre pListeDesEnnemis 
        est une liste dont chaque élément est une liste contenant tous les 
        ennemis d'une ligne, EN COMMENCANT PAR LE LIGNE LA PLUS BASSE

        Parameters
        ----------
        pListeDesEnnemis : TYPE
            DESCRIPTION.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        for i,item in enumerate(pListeDesEnnemis): #Pour chacune des lignes
            for j,ennemi in enumerate(item):
                distance = math.sqrt((ennemi.Position[0]-self.Position[0]) ** 2 +
                                     (ennemi.Position[1]-self.Position[1]) ** 2 )
                if distance <= 10 : 
                    item.remove(ennemi)
                    return True
        return False        