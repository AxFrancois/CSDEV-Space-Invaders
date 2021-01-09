# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 15:47:45 2020

@author: Alexis Pincemin & Axel François
github : https://github.com/AxFrancois/Space-Invaders
"""

# %%----------------------Import----------------------------------------------#

from tkinter import *
import math
import random

# %%----------------------Fonctions-------------------------------------------#

def fAuBoutDuBout(pListeDesEnnemis, pDirectionPrecedente):
    """Fonction qui détecte si les aliens sont proche d'un bord et doivent 
    changer de dirrection. Elle prend comme entrèe pListeDesEnnemis qui est une
    liste dont chaque élément est une liste contenant tous les ennemis d'une
    ligne et pDirectionPrecedente qui vaut soit l soit r. La fonction retourne 
    'l' ou 'r' qui est la direction vers laquelle les ennemis devrons se 
    diriger au prochain mouvement.

    Parameters
    ----------
    pListeDesEnnemis : Liste de Liste de d'élement EntitéEnnemiClassique
        Liste des ennemis en jeu
    pDirectionPrecedente : String
        'l' ou 'r', ancienne direction (permet de faire une direction par 
                                        défaut) 

    Returns
    -------
    Moove : String
        'l' ou 'r' selon la nouvelle direction.

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

# %%------------------------Classes-------------------------------------------#        

class Game:
    """Classe qui gère la partie."""
    
    def __init__(self, pWindow, pCanevas):
        """
        Méthode de création de la partie. Les parametres pWindow et pCanevas
        sont respectivement la fenêtre et le canvas de tkinter

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
        
        print("INIT")
        self.Vie = 3
        self.Score = 0
        self.Niveau = 1
        self.Window = pWindow
        self.Canevas = pCanevas
        self.texteFile = 'HighScore.txt'
        self.TopScore = open(self.texteFile, 'r').read().replace('\n', '')
            
        self.createEntities()
        self.Projectile = []
        self.direction = "r"
        self.createProtection()
        self.RandomTimer = random.randint(5,10)
        self.difficulte = 1
    
    def OnAGagneChef(self):
        listeEnnemis = [self.Aliens1, self.Aliens2[0], self.Aliens2[1], 
                        self.Aliens3[0], self.Aliens3[1]]
        IsEmpty = True
        
        for liste in listeEnnemis:
            if len(liste) != 0:
                IsEmpty = False
            
        return IsEmpty 
    
    def PlayAgain(self, pNiveau):
        if self.Vie < 3:
            self.Vie += 1
        self.Score += 1000
        
        self.RandomTimer = random.randint(5,10)
        self.difficulte = pNiveau
        self.Projectile = []
        self.direction = "r"
        self.createEntities()
                 
    def createEntities(self):
        """
        Méthode qui créée les entités du jeu, à savoir les ennemis et le 
        joueur

        Returns
        -------
        None.

        """
        
        self.Joueur = EntitéJoueur([320, 450],'Player.gif', 'Player_mort.gif')
        self.Aliens1 = [EntitéEnnemiClassique([50 + i*40,50],
                        'Alien_1_frame1.gif', 'Alien_1_frame2.gif') for i in range(11)]
        self.Aliens2 = [[EntitéEnnemiClassique([50 + i*40, 70 + j*20],
                        'Alien_2_frame1.gif', 'Alien_2_frame2.gif') for i in range(11)] for j in range(2)]
        self.Aliens3 = [[EntitéEnnemiClassique([50 + i*40, 110 + j*20],
                        'Alien_3_frame1.gif', 'Alien_3_frame2.gif') for i in range(11)] for j in range(2)]
        self.AliensRouge = []

    def createSpecialEntities(self, pdirectionRouge):
        if pdirectionRouge == 'r':
            Coordonnee = [0,30]
        elif pdirectionRouge == 'l':
            Coordonnee = [700,30]
        self.AliensRouge = [EntitéEnnemiSpecial(Coordonnee, 'Alien_4.gif')]

    def createProtection(self):
        self.Protect = [EntitéProtection([140 + i*120,400], 'Protection.gif') for i in range(4)]

    def clock_update(self, pFrame, pTimer):
        """
        Méthode qui affiche les entités du jeu et gére les projectiles. Le 
        parametre pFrame, qui vaut 0 ou 1, indique s'il faut déplacer et 
        changer l'image des aliens.

        Parameters
        ----------
        pFrame : Entier/int
            Vaut '1' ou '0'. Il permet d'indiquer lorsqu'il faut changer 
            l'image d'un ennemi.
            
        pTimer : float
            Valeur du temps depuis le début du niveau

        Returns
        -------
        None.

        """        
        
        self.Joueur.afficher(self.Window, self.Canevas)
        
        """tir ennemi"""
        
        for item in self.Protect:
            item.afficherProtection(self.Window, self.Canevas)
        
        if pTimer >= self.RandomTimer:
            self.RandomTimer += random.randint(20,30)
            self.directionRouge = random.choice(['r','l'])
            self.createSpecialEntities(self.directionRouge)
            
        for item in self.AliensRouge:
            item.slidingSpecial(self.directionRouge)
            
        for item in self.AliensRouge:
            item.afficherSpecial(self.Window, self.Canevas)
            if item.Position[0] < 0 or item.Position[0] > 700:
                self.AliensRouge.remove(item)
                print("CLEAR")
    
        for item in self.Aliens1:
            item.afficherClassique(self.Window, self.Canevas, pFrame)
            
        for k,liste in enumerate(self.Aliens2):
            for i,item in enumerate(liste):
                item.afficherClassique(self.Window, self.Canevas, pFrame)
        
        for k,liste in enumerate(self.Aliens3):
            for i,item in enumerate(liste):
                item.afficherClassique(self.Window, self.Canevas, pFrame)
        
        for item in self.Projectile:
            if isinstance(item, EntitéTirJoueur):
                item.Position = [item.Position[0], item.Position[1] - 10]
                if item.Position[1] < 0 : #Holala j'ai faillit faire un mémory leak en l'oubliant !!
                    self.Projectile.remove(item)
                kill,points = item.hitbox1([self.Aliens1, self.Aliens2[0],
                                     self.Aliens2[1], self.Aliens3[0],
                                     self.Aliens3[1], self.AliensRouge])
                if kill == True:
                    self.Projectile.remove(item)
                    self.Score += points
                item.afficher(self.Window, self.Canevas)            
        

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
            item.slidingClassique(self.direction,self.NouvelleDirection)
            
        for k,liste in enumerate(self.Aliens2):
            for i,item in enumerate(liste):
                item.slidingClassique(self.direction,self.NouvelleDirection)
        
        for k,liste in enumerate(self.Aliens3):
            for i,item in enumerate(liste):
                item.slidingClassique(self.direction,self.NouvelleDirection)
                
        self.direction = self.NouvelleDirection

    # def protection_update(self):

            
    def ActionJoueur(self, event):
        """
        Méthode qui détecte les pressions des touches du clavier pour 
        executer les commandes.

        Parameters
        ----------
        event : tkinter event
            contient la valeur d'un event tkinter, ici une pression sur le 
            clavier

        Returns
        -------
        None.

        """
        
        pKey = event.keysym
        if pKey == "space":
            self.Projectile.append(EntitéTirJoueur([self.Joueur.getPos()[0], 
                                                    self.Joueur.getPos()[1] - 10],
                                                   'Projectile_joueur.gif'))
        elif pKey == "Right" or pKey == "Left":
            self.Joueur.Mouvement(pKey)

        
class Entité:
    """Classe qui défini toutes les entités du jeu"""
    
    def __init__(self, pPositionInitiale, pImage1, pImage2 = None):
        """
        Méthode de création d'une entité. Elle a pour parametre 
        pPositionInitiale, une liste de 2 entiers, pImage1 et pImage2 qui sont 
        des str et qui indique les images de l'entité

        Parameters
        ----------
        pPositionInitiale : Liste de taille 2 contenant 2 entiers/int
            Contient les coordonnées de l'entité. Elle permet de le positionner
            sur le canvas
        pImage1 : String
            Nom de l'image 1 de l'entité
        pImage2 : String, optional
            Nom de l'image 2 de l'entité. Par défaut : None car certaines 
            entité n'ont qu'une seule image

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
         Liste de taille 2 contenant 2 entiers/int
            Coordonnées de l'entité

        """
        
        return self.Position
    
class EntitéEnnemiClassique(Entité):
    """Sous-classe pour les ennemis classiques"""
    
    def afficherClassique(self, pWindow, pCanevas, pFrame):        
        """
        Méthode d'affichage des entités. Les parametres pWindow et pCanevas
        sont respectivement la fenêtre et le canvas, et pFrame, qui vaut 0 ou
        1, indique quelle image afficher

        Parameters
        ----------
        pWindow : tkinter window
            Nécessaire pour l'interface graphique 
        pCanevas : tkinter canevas
            Idem
        pFrame : Entier/int
            Vaut '1' ou '0'. Il permet d'indiquer lorsqu'il faut changer 
            l'image d'un ennemi.

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

    
    def slidingClassique(self, pAncienneDirection, pNouvelleDirection):
        """
        Méthode pour le déplacement des ennemis. pAncienneDirection et 
        pNouvelleDirection, qui valent 'l' ou 'r' indique quel a été la 
        direction du précédent déplacement et de celui qui doit avoir lieu

        Parameters
        ----------
        pAncienneDirection : String
            'l' ou 'r', ancienne direction (permet de faire descendre les 
                                            ennemis)
        pNouvelleDirection : String
            'l' ou 'r', nouvelle direction(permet de faire descendre les 
                                           ennemis et de déplacer les ennemis à
                                           gauche ou à droite)

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

class EntitéEnnemiSpecial(Entité) :#TO DO
    def afficherSpecial(self, pWindow, pCanevas):
        """
        

        Parameters
        ----------
        pWindow : tkinter window
            Nécessaire pour l'interface graphique 
        pCanevas : tkinter canevas
            Idem
        pX : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.PixelArt = PhotoImage(master = pWindow,
                                   file = 'PixelArts/' + self.Frame1)
        pCanevas.create_image(self.Position[0], self.Position[1], 
                              image = self.PixelArt)
    
    def slidingSpecial(self, pDirection):
        if pDirection == 'r':
            self.Position = [self.Position[0] + 5, self.Position[1]]
        else:
            self.Position = [self.Position[0] - 5, self.Position[1]]
        
        
class EntitéProtection(Entité):#TO DO
    def afficherProtection(self, pWindow, pCanevas):
        """
        

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
        pKey : String,
            "Right" ou "Left", permet de savoir la touche que le joueur à pressé pour se déplacer

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
        respectivement la fenêtre et le canvas.

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
        pWindow : tkinter window
            Nécessaire pour l'interface graphique 
        pCanevas : tkinter canevas
            Idem

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
        ListeDesEnnemis : Liste de Liste de d'élement EntitéEnnemiClassique
            Liste des ennemis en jeu

        Returns
        -------
        bool
            True si un le projectile à touché un ennemi (pour le supprimer)

        """
        for i,item in enumerate(pListeDesEnnemis): #Pour chacune des lignes
            for j,ennemi in enumerate(item):
                distance = math.sqrt((ennemi.Position[0]-self.Position[0]) ** 2 +
                                     (ennemi.Position[1]-self.Position[1]) ** 2 )
                if distance <= 10 : 
                    item.remove(ennemi)
                    
                    if i == 0:
                        Points = 40
                    elif i == 1 or i == 2:
                        Points = 20
                    elif i == 3 or i == 4:
                        Points = 10
                    elif i == 5:
                        Points = random.choice([50,100,150,200])
                        
                    return True, Points
        return False, None