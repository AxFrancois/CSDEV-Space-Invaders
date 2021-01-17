# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 13:30:28 2020

@author: Alexis Pincemin & Axel François
github : https://github.com/AxFrancois/Space-Invaders
"""

# %%----------------------Import----------------------------------------------#

from tkinter import PhotoImage
import random
import time
from Classes.entityEnnemiSpecial import EntityEnnemiSpecial
from Classes.entityEnnemiClassique import EntityEnnemiClassique
from Classes.protection import Protection
from Classes.entityJoueur import EntityJoueur
from Classes.entityTirJoueur import EntityTirJoueur
from Classes.entityTirEnnemi import EntityTirEnnemi
from Classes.fonction import fAuBoutDuBout


class Game:
    """Classe qui gère la partie."""

    def __init__(self, pWindow, pCanevas):
        """
        Méthode de création de la partie. Les parametres pWindow et pCanevas
        sont respectivement la fenêtre et le canvas de tkinter.
        
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
        
        self.Vie = 3
        self.Score = 0
        self.Niveau = 1
        self.Window = pWindow
        self.Canevas = pCanevas
        self.texteFile = 'HighScore.txt'
        self.TopScore = open(self.texteFile, 'r').read().replace('\n', '')
        self.createEntities()
        self.Projectile = []
        self.direction = "r"    #Pour le déplacement des ennemis classiques
        self.createProtection()
        self.RandomTimer = random.randint(15, 20)   #permet l'apparition aléatoire de l'ennemi rouge
        self.Pause = True

    def OnAGagneChef(self):
        """
        Méthode permettant de vérifier si le joueur à gagné le niveau.
        
        Returns
        -------
        IsEmpty : Booléen
            False s'il reste des ennemis classique à l'écran.
			True dans le cas contraire.
        """

        listeEnnemis = [self.Aliens1, self.Aliens2[0], self.Aliens2[1],
                        self.Aliens3[0], self.Aliens3[1]]
        IsEmpty = True

        for liste in listeEnnemis:
            if len(liste) != 0:
                IsEmpty = False

        return IsEmpty

    def LevelUp(self):
        """
        Méthode permettant de level Up.
        
        Returns
        -------
        None.
        """

        if self.Vie < 3:    #Si le joueur n'a pas 3 vies, il en gagne une
            self.Vie += 1
        self.Score += 1000  #Nombre de point qu'on rajoute quand on gagne un niveau

        self.RandomTimer = random.randint(15, 25)   #permet l'apparition aléatoire de l'ennemi rouge
        self.Niveau += 1
        self.Projectile = []    #On réinitialise les projectiles du jeu
        self.direction = "r"    #On réinitialise le sens de déplacement des ennemis classiques
        self.createEntities()   #On recrée les aliens
        self.Pause = True

    def createEntities(self):
        """
        Méthode qui créée les Entitys du jeu, à savoir les ennemis et le
        joueur
        
        Returns
        -------
        None.
        """

        self.Joueur = EntityJoueur([330, 450], 'Player.gif', self.Window, self.Canevas, 'Player_mort.gif')
        self.Aliens1 = [EntityEnnemiClassique([50 + i * 40, 50],
                                              'Alien_1_frame1.gif', self.Window, self.Canevas, 'Alien_1_frame2.gif') for
                        i in range(11)] #EST UNE LISTE d'EntityEnnemiClassique
        self.Aliens2 = [[EntityEnnemiClassique([50 + i * 40, 70 + j * 20],
                                               'Alien_2_frame1.gif', self.Window, self.Canevas, 'Alien_2_frame2.gif')
                         for i in range(11)] for j in range(2)] #EST UNE LISTE DE LISTE d'EntityEnnemiClassique
        self.Aliens3 = [[EntityEnnemiClassique([50 + i * 40, 110 + j * 20],
                                               'Alien_3_frame1.gif', self.Window, self.Canevas, 'Alien_3_frame2.gif')
                         for i in range(11)] for j in range(2)] #EST UNE LISTE DE LISTE d'EntityEnnemiClassique
        self.AliensRouge = []  # On créé une liste vide car c'est plus simple pour la manipulation.

    def createSpecialEntities(self, pdirectionRouge):
        """
        Méthode qui permet de créer l'ennemi spécial grâce à la classe EntityEnnemiSpecial.
        
        Parameters
        ----------
        pdirectionRouge : String
			'l' ou 'r'. Comme son nom l'indique, droite ou gauche.
        Returns
        -------
        None.
        """

        if pdirectionRouge == 'r':
            Coordonnee = [0, 30]
        elif pdirectionRouge == 'l':
            Coordonnee = [700, 30]
        self.AliensRouge = [EntityEnnemiSpecial(Coordonnee, 'Alien_4.gif', self.Window, self.Canevas)]

    def createProtection(self):
        """
        Méthode pour créer les protections grâce à la classe Protection.

        Returns
        -------
        None.
        """

        self.Protect = [Protection([67 + i * 160, 380], self.Window, self.Canevas) for i in range(4)]

    def clock_update(self, pFrame, pTimer):
        """
        Méthode qui affiche les Entitys du jeu et gére les projectiles. Le
        parametre pFrame, qui vaut 0 ou 1, indique s'il faut déplacer et
        changer l'image des aliens.
        
        Parameters
        ----------
        pFrame : Entier/int
            Vaut '1' ou '0'. Il permet d'indiquer lorsqu'il faut changer
            l'image d'un ennemi.

        pTimer : float
            Valeur du temps depuis le début du niveau.
            
        Returns
        -------
        None.
        """

        if self.Pause == False:  # Si le jeu est en pause, l'update ne doit pas se faire
            if pTimer >= self.RandomTimer:  # Pour créer l'ennemi special
                self.RandomTimer += random.randint(15, 25)
                self.directionRouge = random.choice(['r', 'l'])
                self.createSpecialEntities(self.directionRouge)

            for item in self.AliensRouge:  # Pour actualiser la position de l'ennemi special
                item.slidingSpecial(self.directionRouge, self.Canevas)
                if item.Position[0] < 0 or item.Position[0] > 700:  # S'il sort de l'écran
                    self.AliensRouge.remove(item)

            for item in self.Aliens1:  # Pour actualiser la première (plus haute) ligne d'ennemi
                item.afficherClassique(self.Window, self.Canevas, pFrame)

            for k, liste in enumerate(self.Aliens2):  # Pour actualiser la position de la 2nd et 3ème ligne d'ennemi
                for i, item in enumerate(liste):
                    item.afficherClassique(self.Window, self.Canevas, pFrame)

            for k, liste in enumerate(self.Aliens3):  # Pour actualiser la position de la 4ème et 5ème ligne d'ennemi
                for i, item in enumerate(liste):
                    item.afficherClassique(self.Window, self.Canevas, pFrame)

            for item in self.Projectile:  # Pour tout les calculs de projectile
                """projectiles du joueur -> dégat aux aliens"""
                if isinstance(item, EntityTirJoueur):
                    item.Position = [item.Position[0], item.Position[1] - 10]   #Déplacement du projectile de 10 pixels vers le haut
                    if item.Position[1] < 0:  # Holala j'ai faillit faire un mémory leak en l'oubliant !!
                        self.Projectile.remove(item)
                    kill, points = item.hitbox1([self.Aliens1, self.Aliens2[0],
                                                 self.Aliens2[1], self.Aliens3[0],
                                                 self.Aliens3[1],
                                                 self.AliensRouge])  # Vérifie si le projectile touche un alien
                    if kill == True:
                        self.Projectile.remove(item)  # Si c'est le cas on l'enlève
                        self.Score += points

                    item.afficherTirJoueur(self.Window, self.Canevas)   #On update son affichage

                """projectiles des aliens -> dégat au joueur"""
                if isinstance(item, EntityTirEnnemi):   
                    item.Position = [item.Position[0], item.Position[1] + 7]    #Déplacement du projectile de 7 pixels vers le bas
                    tue = item.hitbox2(self.Joueur.Position, item.Position)     # Vérifie si le projectile touche le joueur
                    if tue == True:     #Si le projectile tu le joueur
                        self.Vie = self.Vie - 1 #il perd une vie
                        self.Pause = True   #On met le jeu en pause pour le laisser contempler son erreur
                        self.Joueur.afficherMort(self.Window, self.Canevas, self.Pause) #On affiche l'image du joueur mort
                        debutPause = time.time()    #Pour afficher 3 secondes de pause
                        while time.time() - debutPause < 3: 
                            self.Window.update()
                        self.Pause = False  #On reprend le jeu
                        self.Joueur.afficherMort(self.Window, self.Canevas, self.Pause) #On réaffiche l'image normale du joueur
                        self.Projectile = []    #On supprime tout les projectiles du jeu pour eviter que le joueur reperde une vie instantanément

                    if item.Position[1] % 2 == 0:   #Permet de générer les 1 et des 2 pour alterner l'image du projectile
                        self.Alternateur = 1
                    else:
                        self.Alternateur = 2
                        
                    item.afficherTirEnnemi(self.Window, self.Canevas, self.Alternateur)     #Affichage de la bonne image grâce à l'alternateur
                    self.Canevas.move(item.imageOnCanvas, 0, 7) #déplacement sur le canvas de 7 pixels
                    if item.Position[1] > 500:  #Si les projectile dépace 500 pixels verticalement, c'est qu'il est sorti de l'image et doit être supprimé
                        self.Projectile.remove(item)
                        
                """tous les projectiles :  dégats aux protections"""
                for defense in self.Protect:
                    ADetruit = defense.ProtectionDestruction(item.Position) #Pour les dégats aux protections
                    if ADetruit == True:    #Si la protection est totalement détruit, on la supprime pour economiser des ressources
                        self.Projectile.remove(item)
                        break

            for item in self.Protect:   #Affichage des protections
                item.affichageProtection(self.Window, self.Canevas)

    def position_ennemis_update(self):
        """
        Méthode qui change la position des ennemis à chaque appel.
        
        Returns
        -------
        None.
        """

        if self.Pause == False: #Si le jeu est en pause, les ennemis ne doivent pas se déplacer
            self.NouvelleDirection = fAuBoutDuBout([self.Aliens1, self.Aliens2[0],
                                                    self.Aliens2[1], self.Aliens3[0],
                                                    self.Aliens3[1]], self.direction)   #Permet de savoir si les aliens doivent changer de direction (fichier fonction.py)

            for item in self.Aliens1:   #Affichage des ennemis de la dernière ligne
                if len(self.Aliens1) != 0:  #Pour eviter la liste vide
                    if item.Position[1] > 420:  #Pour vérifier que les ennemis n'ont pas atteint la limite basse de l'écran pour la game over
                        self.Vie = 0
                    item.slidingClassique(self.direction, self.NouvelleDirection, self.Canevas) #Pour les déplacer

            for k, liste in enumerate(self.Aliens2):    #Affichage des ennemis de la 4ème et 3ème ligne 
                if len(liste) != 0:
                    if liste[0].Position[1] > 420:  #idem
                        self.Vie = 0
                    for i, item in enumerate(liste):    #Comme il s'agit ici d'une liste de liste, le traitement est légèrement différent ici
                        item.slidingClassique(self.direction, self.NouvelleDirection, self.Canevas)

            for k, liste in enumerate(self.Aliens3): #Affichage des ennemis de la 2nde et 1ère ligne 
                if len(liste) != 0:
                    if liste[0].Position[1] > 420:  #idem
                        self.Vie = 0
                    for i, item in enumerate(liste):    #idem
                        item.slidingClassique(self.direction, self.NouvelleDirection, self.Canevas)

            self.direction = self.NouvelleDirection

    def ActionJoueur(self, event):
        """
        Méthode qui détecte les pressions des touches du clavier pour
        executer les commandes.
        
        Parameters
        ----------
        event : tkinter event.
            Contient la valeur d'un event tkinter, ici une pression sur le
            clavier.
            
        Returns
        -------
        None.
        """

        if self.Pause == False:     #Si le jeu est en pause il faut bloquer les actions du joueur
            pKey = event.keysym     #Detecte les pressions du clavier
            if pKey == "space":     #Espace = tirer
                self.Projectile.append(EntityTirJoueur([self.Joueur.getPos()[0],
                                                        self.Joueur.getPos()[1] - 10],
                                                       'Projectile_joueur.gif',
                                                       self.Window, self.Canevas))  #Pour créer le tir du joueur
                
            elif pKey == "Right" or pKey == "Left": #Pour déplacer le joueur (flèches directionnelles)
                self.Joueur.Mouvement(pKey, self.Canevas)

    def fTirsEnnemi(self):
        """
        Méthode pour faire tirer les ennemis

        Returns
        -------
        None.

        """
        NombreTir = random.randint(0, 4)    #Nombre aléatoire du tir

        listeEnnemis = [self.Aliens1, self.Aliens2[0], self.Aliens2[1],
                        self.Aliens3[0], self.Aliens3[1]]   #Liste des ennemis classique en jeu, pour les faire tirer

        for numeroTir in range(NombreTir):  #Pour chacun des tirs
            LigneTir = random.randint(0, len(listeEnnemis) - 1) #On chosit une ligne aléatoire
            if len(listeEnnemis[LigneTir]) != 0:    #Si cette ligne n'est pas vide, un des aliens tire
                EnnemiTir = random.randint(0, len(listeEnnemis[LigneTir]) - 1)  #On choisit l'alien qui tire aléatoirement
                PositionTir = listeEnnemis[LigneTir][EnnemiTir].getPos()    #On récupère se position pour créer le projectile
                TypeProjectile = random.choice([1, 2])   #On choisit aléatoirement le type de projectile
                if TypeProjectile == 1: #On créé le projectile choisit
                    self.Projectile.append(
                        EntityTirEnnemi([PositionTir[0], PositionTir[1] + 10], 'Projectile_alien1_frame1.gif',
                                        self.Window, self.Canevas, 'Projectile_alien1_frame2.gif'))
                else:
                    self.Projectile.append(
                        EntityTirEnnemi([PositionTir[0], PositionTir[1] + 10], 'Projectile_alien2_frame1.gif',
                                        self.Window, self.Canevas, 'Projectile_alien2_frame2.gif'))
