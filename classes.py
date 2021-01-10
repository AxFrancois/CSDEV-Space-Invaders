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
        """
        

        Returns
        -------
        IsEmpty : TYPE
            DESCRIPTION.

        """
        listeEnnemis = [self.Aliens1, self.Aliens2[0], self.Aliens2[1], 
                        self.Aliens3[0], self.Aliens3[1]]
        IsEmpty = True
        
        for liste in listeEnnemis:
            if len(liste) != 0:
                IsEmpty = False
            
        return IsEmpty 
    
    def PlayAgain(self, pNiveau):
        """
        

        Parameters
        ----------
        pNiveau : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
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
        
        self.Joueur = EntitéJoueur([330, 450],'Player.gif', self.Window, self.Canevas,'Player_mort.gif')
        self.Aliens1 = [EntitéEnnemiClassique([50 + i*40,50],
                        'Alien_1_frame1.gif', self.Window, self.Canevas, 'Alien_1_frame2.gif') for i in range(11)]
        self.Aliens2 = [[EntitéEnnemiClassique([50 + i*40, 70 + j*20],
                        'Alien_2_frame1.gif', self.Window, self.Canevas,'Alien_2_frame2.gif') for i in range(11)] for j in range(2)]
        self.Aliens3 = [[EntitéEnnemiClassique([50 + i*40, 110 + j*20],
                        'Alien_3_frame1.gif', self.Window, self.Canevas,'Alien_3_frame2.gif') for i in range(11)] for j in range(2)]
        self.AliensRouge = []

    def createSpecialEntities(self, pdirectionRouge):
        """
        

        Parameters
        ----------
        pdirectionRouge : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        if pdirectionRouge == 'r':
            Coordonnee = [0,30]
        elif pdirectionRouge == 'l':
            Coordonnee = [700,30]
        self.AliensRouge = [EntitéEnnemiSpecial(Coordonnee, 'Alien_4.gif', self.Window, self.Canevas)]


    def createProtection(self):
        """
        

        Returns
        -------
        None.

        """
        self.Protect = [Protection([67 + i*160,380], self.Window, self.Canevas) for i in range(4)]
        

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
        #  self.Canevas.delete("all")
        self.Joueur.afficher(self.Window, self.Canevas)     
        """
        for item in self.Protect:
            item.afficherProtection(self.Window, self.Canevas)
        """
        if pTimer >= self.RandomTimer:
            self.RandomTimer += random.randint(20,30)
            self.directionRouge = random.choice(['r','l'])
            self.createSpecialEntities(self.directionRouge)
            
        for item in self.AliensRouge:
            item.slidingSpecial(self.directionRouge, self.Canevas)
            if item.Position[0] < 0 or item.Position[0] > 700:
                self.AliensRouge.remove(item)
    
        for item in self.Aliens1:
            item.afficherClassique(self.Window, self.Canevas, pFrame)
            
        for k,liste in enumerate(self.Aliens2):
            for i,item in enumerate(liste):
                item.afficherClassique(self.Window, self.Canevas, pFrame)
        
        for k,liste in enumerate(self.Aliens3):
            for i,item in enumerate(liste):
                item.afficherClassique(self.Window, self.Canevas, pFrame)
        

        for item in self.Projectile:
            """projectiles du joueur -> dégat aux aliens et aux protections"""
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
            """projectiles des aliens -> dégat au joueur et aux protections"""    
            if isinstance(item, EntitéTirEnnemi):
                item.Position = [item.Position[0], item.Position[1] + 7]
                if item.Position[1] % 2 == 0:
                    self.Alternateur = 1
                else:
                    self.Alternateur = 2
                item.afficher(self.Window, self.Canevas, self.Alternateur)
                self.Canevas.move(item.imageOnCanvas, 0, 7) 
                if item.Position[1] > 500 : 
                    self.Projectile.remove(item)
                    
        for item in self.Projectile:
            for defense in self.Protect:
                ADetruit = defense.ProtectionDestruction(item.Position)
                if ADetruit == True:
                    self.Projectile.remove(item)
                    break
                
        for item in self.Protect:
            item.affichageProtection(self.Window, self.Canevas)
            
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
            item.slidingClassique(self.direction,self.NouvelleDirection, self.Canevas)
            
        for k,liste in enumerate(self.Aliens2):
            for i,item in enumerate(liste):
                item.slidingClassique(self.direction,self.NouvelleDirection, self.Canevas)
        
        for k,liste in enumerate(self.Aliens3):
            for i,item in enumerate(liste):
                item.slidingClassique(self.direction,self.NouvelleDirection, self.Canevas)
                
        self.direction = self.NouvelleDirection

            
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
                                                   'Projectile_joueur.gif', 
                                                   self.Window, self.Canevas))
        elif pKey == "Right" or pKey == "Left":
            self.Joueur.Mouvement(pKey)

    def fTirsEnnemi(self):
        NombreTir = random.randint(self.difficulte - 1, self.difficulte + 3)
        
        listeEnnemis = [self.Aliens1, self.Aliens2[0], self.Aliens2[1], 
                        self.Aliens3[0], self.Aliens3[1]]
        
        for numeroTir in range(NombreTir):
            LigneTir = random.randint(0, len(listeEnnemis) -1)
            if len(listeEnnemis[LigneTir]) != 0 :
                EnnemiTir = random.randint(0, len(listeEnnemis[LigneTir]) -1)
                PositionTir = listeEnnemis[LigneTir][EnnemiTir].getPos()
                TypeProjectile = random.randint(1,2)
                if TypeProjectile == 1:
                    self.Projectile.append(EntitéTirEnnemi([PositionTir[0], PositionTir[1] + 10], 'Projectile_alien1_frame1.gif', self.Window, self.Canevas, 'Projectile_alien1_frame2.gif'))
                else:
                    self.Projectile.append(EntitéTirEnnemi([PositionTir[0], PositionTir[1] + 10], 'Projectile_alien2_frame1.gif', self.Window, self.Canevas, 'Projectile_alien2_frame2.gif'))
                    
class Entité:
    """Classe qui défini toutes les entités du jeu"""
    
    def __init__(self, pPositionInitiale, pImage1, pWindow, pCanevas, pImage2 = None):
        """
        Méthode de création d'une entité. Elle a pour parametre 
        pPositionInitiale, une liste de 2 entiers, pImage1 et pImage2 qui sont 
        des str et qui indique les images de l'entité.
        
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
        self.PixelArt = PhotoImage(master = pWindow, file = 'PixelArts/' + self.Frame1)
        self.imageOnCanvas = pCanevas.create_image(self.Position[0], self.Position[1], image = self.PixelArt)
        
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
        pCanevas.itemconfig(self.imageOnCanvas, image = self.PixelArt)
    
    def slidingClassique(self, pAncienneDirection, pNouvelleDirection, pCanevas):
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
            pCanevas.move(self.imageOnCanvas, 0, 30) 
            self.Position = [self.Position[0], self.Position[1] + 30]
        elif pNouvelleDirection == "r":
            pCanevas.move(self.imageOnCanvas, 20, 0) 
            self.Position = [self.Position[0] + 20, self.Position[1]]
        elif pNouvelleDirection == "l":
            pCanevas.move(self.imageOnCanvas, -20, 0)
            self.Position = [self.Position[0] - 20, self.Position[1]]
            
class EntitéEnnemiSpecial(Entité) :
  
    def slidingSpecial(self, pDirection, pCanevas):
        """
        

        Parameters
        ----------
        pDirection : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        if pDirection == 'r':
            pCanevas.move(self.imageOnCanvas, 5, 0) 
            self.Position = [self.Position[0] + 5, self.Position[1]]
        else:
            pCanevas.move(self.imageOnCanvas, -5, 0) 
            self.Position = [self.Position[0] - 5, self.Position[1]]
        
class Protection:#TO DO

    def __init__(self, pCoordonne, pWindow, pCanevas):
        self.Position = pCoordonne
        self.bloc1 = EntitéPartieProtection([pCoordonne[0], pCoordonne[1] + 23], 1, pWindow, pCanevas)            #Bloc bas gauche
        self.bloc2 = EntitéPartieProtection([pCoordonne[0] + 43 , pCoordonne[1] + 23], 1, pWindow, pCanevas)      #Bloc bas droite
        self.bloc3 = EntitéPartieProtection([pCoordonne[0], pCoordonne[1]+6], 2, pWindow, pCanevas)               #Bloc haut gauche
        self.bloc4 = EntitéPartieProtection([pCoordonne[0] + 43 , pCoordonne[1]+6], 3, pWindow, pCanevas)         #Bloc haut droite
        self.bloc5 = EntitéPartieProtection([pCoordonne[0] + 15 , pCoordonne[1]], 4, pWindow, pCanevas)           #Bloc milieu haut gauche
        self.bloc6 = EntitéPartieProtection([pCoordonne[0] + 29 , pCoordonne[1]], 4, pWindow, pCanevas)           #Bloc milieu haut droite
        self.bloc7 = EntitéPartieProtection([pCoordonne[0] + 15 , pCoordonne[1] + 11], 5, pWindow, pCanevas)      #Bloc milieu bas droite
        self.bloc8 = EntitéPartieProtection([pCoordonne[0] + 29 , pCoordonne[1] + 11], 6, pWindow, pCanevas)      #Bloc milieu bas gauche
        self.listeBloc = [self.bloc1, self.bloc2, self.bloc3, self.bloc4, 
                          self.bloc5, self.bloc6, self.bloc7, self.bloc8]
                
    def ProtectionDestruction(self, pCoordProjectile):
        for element in self.listeBloc:
            distance = math.sqrt((element.Position[0]-pCoordProjectile[0]) ** 2 + (element.Position[1]-pCoordProjectile[1]) ** 2 )
            if distance <= 10 : 
                element.DegatSubit += 1               
                return True
        return False
    
    def affichageProtection(self, pWindow, pCanevas) : 
        for element in self.listeBloc:
            if element.DegatSubit == 5:
                self.listeBloc.remove(element)
                pCanevas.delete(element.imageOnCanvas)
            else:
                element.AffichageBloc(pWindow, pCanevas)
            
                
            
class EntitéPartieProtection(Entité):
    def __init__(self, pCoordonne, pNumero, pWindow, pCanevas):
        self.Position = pCoordonne
        self.Image0 = 'Protection{}-D0.gif'.format(pNumero)
        self.Image1 = 'Protection{}-D1.gif'.format(pNumero)
        self.Image2 = 'Protection{}-D2.gif'.format(pNumero)
        self.Image3 = 'Protection{}-D3.gif'.format(pNumero)
        self.Image4 = 'Protection{}-D4.gif'.format(pNumero)
        self.DegatSubit = 0
        
        self.PixelArt = PhotoImage(master = pWindow,
                                       file = 'PixelArts/Protections/' + self.Image0)
        self.imageOnCanvas = pCanevas.create_image(self.Position[0], self.Position[1],
                                  image = self.PixelArt)
        
    def AffichageBloc(self, pWindow, pCanevas):
            if self.DegatSubit == 0:
                self.Image = self.Image0
            if self.DegatSubit == 1:
                self.Image = self.Image1
            elif self.DegatSubit == 2:
                self.Image = self.Image2
            elif self.DegatSubit == 3:
                self.Image = self.Image3
            elif self.DegatSubit == 4:
                self.Image = self.Image4
                   
            self.PixelArt = PhotoImage(master = pWindow,
                                      file = 'PixelArts/Protections/' + self.Image)
            pCanevas.itemconfig(self.imageOnCanvas, image = self.PixelArt) 
        
        
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
        if pKey == "Right" and self.Position[0] < 630:
            self.Position[0] += 10
        elif pKey == "Left" and self.Position[0] > 30:
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
            True si un le projectile du joueur à touché un ennemi (pour le 
                                                                   supprimer)

        """        
        for i,item in enumerate(pListeDesEnnemis): #Pour chacune des lignes
            for j,ennemi in enumerate(item):
                distance = math.sqrt((ennemi.Position[0]-self.Position[0]) ** 2 +
                                     (ennemi.Position[1]-self.Position[1]) ** 2 )
                if distance <= 10 : 
                    item.remove(ennemi)
                    
                    if i == 0:
                        Points = 40
                    elif i in [1,2]:
                        Points = 20
                    elif i in [3,4]:
                        Points = 10
                    elif i == 5:
                        Points = random.choice([50,100,150,200])
                        
                    return True, Points
        return False, None
    
class EntitéTirEnnemi(Entité):   
    
    def afficher(self, pWindow, pCanevas, pAlternateur):
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

        if pAlternateur == 1:
            self.PixelArt = PhotoImage(master = pWindow, file = 'PixelArts/' + self.Frame1)
        elif pAlternateur == 2:
            self.PixelArt = PhotoImage(master = pWindow, file = 'PixelArts/' + self.Frame2)
        pCanevas.itemconfig(self.imageOnCanvas, image = self.PixelArt)
    
    def hitbox2(self, pListeDesEnnemis):
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
            True si un le projectile du joueur à touché un ennemi (pour le 
                                                                   supprimer)

        """        
        for i,item in enumerate(pListeDesEnnemis): #Pour chacune des lignes
            for j,ennemi in enumerate(item):
                distance = math.sqrt((ennemi.Position[0]-self.Position[0]) ** 2 +
                                     (ennemi.Position[1]-self.Position[1]) ** 2 )
                if distance <= 10 : 
                    item.remove(ennemi)
                    
                    if i == 0:
                        Points = 40
                    elif i in [1,2]:
                        Points = 20
                    elif i in [3,4]:
                        Points = 10
                    elif i == 5:
                        Points = random.choice([50,100,150,200])
                        
                    return True, Points
        return False, None
    
    