from tkinter import PhotoImage
import random
import time
from entityEnnemiSpecial import EntityEnnemiSpecial
from entityEnnemiClassique import EntityEnnemiClassique
from protection import Protection
from entityJoueur import EntityJoueur
from entityTirJoueur import EntityTirJoueur
from entityTirEnnemi import EntityTirEnnemi
from fonction import fAuBoutDuBout


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
        self.RandomTimer = random.randint(15, 20)
        self.Pause = False

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

        if self.Vie < 3:
            self.Vie += 1
        self.Score += 1000

        self.RandomTimer = random.randint(15, 25)
        self.Niveau += 1
        self.Projectile = []
        self.direction = "r"
        self.createEntities()
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
                        i in range(11)]
        self.Aliens2 = [[EntityEnnemiClassique([50 + i * 40, 70 + j * 20],
                                               'Alien_2_frame1.gif', self.Window, self.Canevas, 'Alien_2_frame2.gif')
                         for i in range(11)] for j in range(2)]
        self.Aliens3 = [[EntityEnnemiClassique([50 + i * 40, 110 + j * 20],
                                               'Alien_3_frame1.gif', self.Window, self.Canevas, 'Alien_3_frame2.gif')
                         for i in range(11)] for j in range(2)]
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
                    item.Position = [item.Position[0], item.Position[1] - 10]
                    if item.Position[1] < 0:  # Holala j'ai faillit faire un mémory leak en l'oubliant !!
                        self.Projectile.remove(item)
                    kill, points = item.hitbox1([self.Aliens1, self.Aliens2[0],
                                                 self.Aliens2[1], self.Aliens3[0],
                                                 self.Aliens3[1],
                                                 self.AliensRouge])  # Vérifie si le projectile touche un alien
                    if kill == True:
                        self.Projectile.remove(item)  # Si c'est le cas on l'enlève
                        self.Score += points

                    item.afficherTirJoueur(self.Window, self.Canevas)

                """projectiles des aliens -> dégat au joueur"""
                if isinstance(item, EntityTirEnnemi):
                    item.Position = [item.Position[0], item.Position[1] + 7]
                    tué = item.hitbox2(self.Joueur.Position, item.Position)
                    if tué == True:
                        self.Vie = self.Vie - 1
                        self.Pause = True
                        self.Joueur.afficherMort(self.Window, self.Canevas, self.Pause)
                        debutPause = time.time()
                        while time.time() - debutPause < 3:
                            self.Window.update()
                        self.Pause = False
                        self.Joueur.afficherMort(self.Window, self.Canevas, self.Pause)
                        self.Projectile = []

                    if item.Position[1] % 2 == 0:
                        self.Alternateur = 1
                    else:
                        self.Alternateur = 2
                    item.afficherTirEnnemi(self.Window, self.Canevas, self.Alternateur)
                    self.Canevas.move(item.imageOnCanvas, 0, 7)
                    if item.Position[1] > 500:
                        self.Projectile.remove(item)
                """tous les projectiles :  dégats aux protections"""
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

        if self.Pause == False:
            self.NouvelleDirection = fAuBoutDuBout([self.Aliens1, self.Aliens2[0],
                                                    self.Aliens2[1], self.Aliens3[0],
                                                    self.Aliens3[1]], self.direction)

            for item in self.Aliens1:
                if len(self.Aliens1) != 0:
                    if item.Position[1] > 420:
                        self.Vie = 0
                    item.slidingClassique(self.direction, self.NouvelleDirection, self.Canevas)

            for k, liste in enumerate(self.Aliens2):
                if len(liste) != 0:
                    if liste[0].Position[1] > 420:
                        self.Vie = 0
                    for i, item in enumerate(liste):
                        item.slidingClassique(self.direction, self.NouvelleDirection, self.Canevas)

            for k, liste in enumerate(self.Aliens3):
                if len(liste) != 0:
                    if liste[0].Position[1] > 420:
                        self.Vie = 0
                    for i, item in enumerate(liste):
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

        if self.Pause == False:
            pKey = event.keysym
            if pKey == "space":
                self.Projectile.append(EntityTirJoueur([self.Joueur.getPos()[0],
                                                        self.Joueur.getPos()[1] - 10],
                                                       'Projectile_joueur.gif',
                                                       self.Window, self.Canevas))
            elif pKey == "Right" or pKey == "Left":
                self.Joueur.Mouvement(pKey, self.Canevas)

    def fTirsEnnemi(self):
        NombreTir = random.randint(0, 4)

        listeEnnemis = [self.Aliens1, self.Aliens2[0], self.Aliens2[1],
                        self.Aliens3[0], self.Aliens3[1]]

        for numeroTir in range(NombreTir):
            LigneTir = random.randint(0, len(listeEnnemis) - 1)
            if len(listeEnnemis[LigneTir]) != 0:
                EnnemiTir = random.randint(0, len(listeEnnemis[LigneTir]) - 1)
                PositionTir = listeEnnemis[LigneTir][EnnemiTir].getPos()
                TypeProjectile = random.randint(1, 2)
                if TypeProjectile == 1:
                    self.Projectile.append(
                        EntityTirEnnemi([PositionTir[0], PositionTir[1] + 10], 'Projectile_alien1_frame1.gif',
                                        self.Window, self.Canevas, 'Projectile_alien1_frame2.gif'))
                else:
                    self.Projectile.append(
                        EntityTirEnnemi([PositionTir[0], PositionTir[1] + 10], 'Projectile_alien2_frame1.gif',
                                        self.Window, self.Canevas, 'Projectile_alien2_frame2.gif'))



