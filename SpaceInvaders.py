# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 13:30:28 2020

@author: Alexis Pincemin & Axel François
github : https://github.com/AxFrancois/Space-Invaders
"""

# %%----------------------Import----------------------------------------------#

from tkinter import Menu, Canvas, Label, Tk, Button, Frame, StringVar
import time, math
from Classes.game import Game

# %%----------------------Fonctions de test-----------------------------------#

def key_pressed(event):
     print("Key Pressed:"+event.keysym)


class main:
    
    def __init__(self):
    # %%----------------------Constantes-----------------------------------------#
        self.width = 825
        self.height = 500
        self.backgroundColorGrey = '#A2A4AA'
        self.backgroundColorBlack = '#000000'
        self.foregroundColorWhite = '#FFFFFF'
        self.TaillePoliceInterface = 11
        self.TaillePoliceMessages = 20
        self.PositionTexteDebutLevelX = 320
        self.PositionTexteDebutLevelY = 300
    
    # %%----------------------Interface graphique---------------------------------#
        self.window = Tk()
        self.window.title('Space invaders')

        """on centre la fenêtre sur l'écran 
        on la rend non redimensionnable"""
        widthScreen = self.window.winfo_screenwidth()
        heightScreen = self.window.winfo_screenheight()
        x = (widthScreen // 2) - (self.width // 2)
        y = (heightScreen // 2) - (self.height // 2)
        self.window.geometry('{}x{}+{}+{}' .format(self.width, self.height, x, y))
        self.window.resizable(width = False, height = False)
        """fenêtre de couleur grise"""
        self.window.config(bg = self.backgroundColorGrey)

        """Frame à gauche noir qui va contenir le Canvas et
         les deux Labels (score et vies)"""
        self.leftFrame = Frame(self.window, bg = self.backgroundColorBlack)
        self.leftFrame.grid(row=0, column=0)

        """Frame à droite grise qui va contenir les deux bouttons (quitter et rejouer) """
        self.rightFrame = Frame(self.window, bg = self.backgroundColorGrey)
        self.rightFrame.grid(row = 0, column = 1)

        """Label qui indique les nombre de vies restantes police blanche sur fond noir
        situé à la première ligne de la Frame de gauche"""
        self.stayLife = StringVar()
        self.stayLife.set('LIVES')
        self.lifeLabel = Label(self.leftFrame, textvariable = self.stayLife, bg = self.backgroundColorBlack,
                          fg = self.foregroundColorWhite, font = ("Terminal", self.TaillePoliceInterface))
        self.lifeLabel.grid(row = 0, column = 0,padx = (550, 0))

        """Label qui indique le score et le meilleur score police blanche sur fond noir
        situé à la première ligne de la Frame de gauche"""
        self.myScore = StringVar()
        self.myScore.set('SCORE')
        self.scoreLabel = Label(self.leftFrame, textvariable = self.myScore, bg = self.backgroundColorBlack,
                           fg = self.foregroundColorWhite, font = ("Terminal", self.TaillePoliceInterface))
        self.scoreLabel.grid(row = 0, column = 0, padx = (0, 600))

        """Canvas de couleur noir qui contient tout les éléments du jeu"""
        self.Canevas = Canvas(self.leftFrame, width = 650, height = 480, bg = self.backgroundColorBlack,
                         highlightthickness = 0)
        self.Canevas.grid(row = 1, column = 0,)

        """Boutons situé dans la Frame de droite l'un en dessous de l'autre
        de couleur de fond identique à window et de police noir"""
        self.replayButton = Button(self.rightFrame, text = 'New game', bg = self.backgroundColorGrey,
                              fg = self.backgroundColorBlack, font = ('Terminal', self.TaillePoliceInterface), command = self.restart)
        self.replayButton.grid(row = 0, column = 0, pady = (0, 50), padx = (20, 0))
        
        self.quitButton = Button(self.rightFrame, text = 'Quitter', bg = self.backgroundColorGrey,
                            fg = self.backgroundColorBlack, font = ('Terminal', self.TaillePoliceInterface),
                            command = self.window.destroy)
        self.quitButton.grid(row = 1, column = 0, pady = (50, 0), padx = (20, 0))

        """Menu de window qui contient 3 commandes"""
        self.menuBar = Menu(self.window)
        self.menuGame = Menu(self.menuBar, tearoff=0)
        self.menuGame.add_command(label="Rejouer", command=self.restart)
        self.menuGame.add_command(label="Quitter", command=self.window.destroy)
        self.menuGame.add_command(label="A propos", command="")
        self.menuBar.add_cascade(label="Jeux", menu=self.menuGame)
        self.window.config(menu=self.menuBar)

    def reset(self):
    # %%----------------------Initialisations-------------------------------------#
        """Création de la partie"""
        self.Partie = Game(self.window,self.Canevas)
        
        self.frame_buffer = 0   #Permettra l'annimation des ennemis
        self.myScore.set('SCORE : {} (Record : {})'.format(str(self.Partie.Score), self.Partie.TopScore))       #Affichage du score et du Highscore
        self.start_time = time.time()   #Permet d'enregistrer le temps de début de la partie
        
        """Affichage du texte pour le début de la partie"""
        texteLigne1 = "Niveau {} GO ! Utilisez espace pour tirer et ".format(self.Partie.Niveau) #Textes pour le début du niveau
        texteLigne2 = "les fleches directionnelles pour vous deplacer"
        self.TextId1 = self.Canevas.create_text(self.PositionTexteDebutLevelX, self.PositionTexteDebutLevelY, 
                                               font = ("Terminal", self.TaillePoliceMessages), text = texteLigne1, fill = self.foregroundColorWhite)
        self.TextId2 = self.Canevas.create_text(self.PositionTexteDebutLevelX, self.PositionTexteDebutLevelY+25, 
                                               font = ("Terminal", self.TaillePoliceMessages), text = texteLigne2, fill = self.foregroundColorWhite)
        while time.time() - self.start_time < 3:    #Permet d'afficher le texte pendant 3 secondes
            self.window.update()
        self.Canevas.delete(self.TextId1)
        self.Canevas.delete(self.TextId2)    #Supprime les textes à la fin des 3 secondes
        self.Partie.Pause = False       #Enlève la pause du jeu pour qu'il puisse commencer   
    
    def start(self):
    # %%----------------------Boucle principale-----------------------------------#
        while self.Partie.Vie > 0:  #La condition d'arret du jeu est que le joueur n'ai plus de vie
            try:
                """Verification de level up"""
                if self.Partie.OnAGagneChef() == True:  #Permet de vérifier que le niveau n'est pas fini, auquel cas :
                    self.Partie.LevelUp()
                    """Texte de level up"""
                    texte = "Niveau {} GO !".format(self.Partie.Niveau )
                    self.TextId = self.Canevas.create_text(self.PositionTexteDebutLevelX, self.PositionTexteDebutLevelY,
                                                           font = ("Terminal", self.TaillePoliceMessages),
                                                           text = texte, fill = self.foregroundColorWhite)
                    self.pause_time = time.time()   #Sauvegarde du temps pour gerer l'affichage
                    while time.time() - self.pause_time < 3:    #Permet d'afficher le texte pendant 3 secondes
                        self.window.update()
                    self.Canevas.delete(self.TextId)    #Supprime le texte à la fin des 3 secondes  
                    self.Partie.Pause = False   #Enlève la pause pour le texte entre les niveaux
                    self.start_time = time.time()   #Enregistrement du temps du début du niveau, pour faire apparaitre l'ennemi rouge
                
                """Execution nomminale"""    
                self.InitframeTime = time.time()    #Enregistre le temps au début du l'execution de la boucle
                self.clock = self.InitframeTime  - self.start_time      #Temps depuis le début du niveau (pour faire apparaitre l'ennemi rouge)
                self.window.bind("<Key>", self.Partie.ActionJoueur)     #Detection des touches du clavier pour exectuer le méthode ActionJoueur)
                self.frame = abs((math.floor(self.clock*(self.Partie.Niveau/3))) % - 2) #Numéro de frame, pour savoir quelle image afficher pour les ennemis, dépend de self.Partie.Niveau pour rendre le jeu plus dur au fur et à mesure des niveaux
                if self.frame != self.frame_buffer :    #Lors d'un changement de frame, on change l'image des ennemis
                    self.Partie.position_ennemis_update()   #Pour déplacer et changer l'image des ennemis
                    self.Partie.fTirsEnnemi()   #Pour faire tirer les ennemis
                self.frame_buffer = self.frame  #Une fois le déplacement effectué, on enregistre quel était le numéro de frame précédent
                self.Partie.clock_update(self.frame,self.clock) #Update générale et afficahge de tous les éléments du jeu
                self.myScore.set('SCORE : {} (Record : {})'.format(str(self.Partie.Score), self.Partie.TopScore))   #Affichage du score et du Highscore
                self.stayLife.set('VIES : '  + str(self.Partie.Vie))
                
                """Verrou du taux de rafraichissement""" 
                frameTime = time.time() - self.InitframeTime #Enregistre le temps mis par le programme à être exécuté
                if frameTime < 0.03333: #0.033333ms, permet de limiter le taux de rafraichissement et de mise à jour du jeu à 30 images par secondes
                    time.sleep(0.03333 - frameTime)
                    
                """Mise à jour de l'affichage tkitner"""
                self.window.update()
                
            except:
                break
            
        """Fin de jeu"""    
        if int(self.Partie.Score) > int(self.Partie.TopScore):  #Enregistrement du HighScore s'il est battu
            open(self.Partie.texteFile, 'w').write(str(self.Partie.Score))
        self.Partie.Pause = True 
        self.Canevas.delete("all")  #On supprime tout les elements du canvas pour afficher le game over
        
        """Textes de fin de jeu"""
        texte1 = "Game Over ! Vous etes mort au niveau {}. Votre score est de {}.".format(self.Partie.Niveau,str(self.Partie.Score))
        texte2 = "Appuyez sur New Game pour relancer"
        TextId1 = self.Canevas.create_text(320,300, font = ("Terminal", self.TaillePoliceMessages),
                                           text = texte1, fill = self.foregroundColorWhite)
        TextId2 = self.Canevas.create_text(340,330, font = ("Terminal", self.TaillePoliceMessages),
                                           text = texte2, fill = self.foregroundColorWhite)
        self.window.mainloop()  #On boucle tant que le joueur ne quitte pas la fenêtre

    def restart(self):
        # %% Fonction pour rejouer
        try:
            
            self.Canevas.delete("all")  #On réinitialise les éléments affiché sur le canvas
            self.Partie.Pause = True    #On met le jeu en pause pour bloquer les actions du joueur
            play.reset()
            play.start()
        except:
           pass
        
try:
    play = main()
    play.reset()
    play.start()
except:
  pass