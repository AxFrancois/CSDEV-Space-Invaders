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
    # %%----------------------Interface graphique---------------------------------#
        self.window = Tk()
        
        self.window.title('Space invaders')
        width = 825
        height = 500
        """on centre la fenêtre sur l'écran 
        on la rend non redimensionnable"""
        widthScreen = self.window.winfo_screenwidth()
        heightScreen = self.window.winfo_screenheight()
        x = (widthScreen // 2) - (width // 2)
        y = (heightScreen // 2) - (height // 2)
        self.window.geometry('{}x{}+{}+{}' .format(width, height, x, y))
        self.window.resizable(width = False, height = False)
        """fenêtre de couleur grise"""
        self.window.config(bg = '#A2A4AA')

        """Frame à gauche noir qui va contenir le Canvas et
         les deux Labels (score et vies)"""
        self.leftFrame = Frame(self.window, bg = '#000000')
        self.leftFrame.grid(row=0, column=0)

        """Frame à droite grise qui va contenir les deux bouttons (quitter et rejouer) """
        self.rightFrame = Frame(self.window, bg = '#A2A4AA')
        self.rightFrame.grid(row = 0, column = 1)

        """Label qui indique les nombre de vies restantes police blanche sur fond noir
        situé à la première ligne de la Frame de gauche"""
        self.stayLife = StringVar()
        self.stayLife.set('LIVES')
        self.lifeLabel = Label(self.leftFrame, textvariable = self.stayLife, bg = '#000000',
                          fg='#FFFFFF', font = ("Terminal", 11))
        self.lifeLabel.grid(row = 0, column = 0,padx = (550, 0))

        """Label qui indique le score et le meilleur score police blanche sur fond noir
        situé à la première ligne de la Frame de gauche"""
        self.myScore = StringVar()
        self.myScore.set('SCORE')
        self.scoreLabel = Label(self.leftFrame, textvariable = self.myScore, bg = '#000000',
                           fg='#FFFFFF', font = ("Terminal", 11))
        self.scoreLabel.grid(row = 0, column = 0, padx = (0, 600))

        """Canvas de couleur noir qui contient tout les éléments du jeu"""
        self.Canevas = Canvas(self.leftFrame, width = 650, height = 479, bg = '#000000',
                         highlightthickness = 0)
        self.Canevas.grid(row = 1, column = 0,)

        """Boutons situé dans la Frame de droite l'un en dessous de l'autre
        de couleur de fond identique à window et de police noir"""
        self.replayButton = Button(self.rightFrame, text = 'New game', bg = '#A2A4AA',
                              fg = '#000000', font = ('Terminal', 10), command = self.restart)
        self.replayButton.grid(row = 0, column = 0, pady = (0, 50), padx = (20, 0))
        
        self.quitButton = Button(self.rightFrame, text = 'Quitter', bg = '#A2A4AA',
                            fg = '#000000', font = ('Terminal', 10),
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
        self.Partie = Game(self.window,self.Canevas)
        
        self.frame_buffer = 0
        self.myScore.set('SCORE : {} (Record : {})'.format(str(self.Partie.Score), self.Partie.TopScore))   
        self.start_time = time.time()
        texte = "Niveau {} GO !".format(self.Partie.Niveau)
        self.TextId = self.Canevas.create_text(320,300, font = ("Terminal", 20), text = texte, fill = '#FFFFFF')
        while time.time() - self.start_time < 3:
            self.window.update()
        self.Canevas.delete(self.TextId)
        self.Partie.Pause = False        
    
    def start(self):
    # %%----------------------Boucle principale-----------------------------------#
        while self.Partie.Vie > 0:
            try:
                if self.Partie.OnAGagneChef() == True:
                    self.Partie.LevelUp()
                    texte = "Niveau {} GO !".format(self.Partie.Niveau )
                    self.TextId = self.Canevas.create_text(320,300, font = ("Terminal", 20), text = texte, fill = '#FFFFFF')
                    self.pause_time = time.time()
                    while time.time() - self.pause_time < 3:
                        self.window.update()
                    self.Partie.Pause = False
                    self.Canevas.delete(self.TextId)
                    self.start_time = time.time()
                    
                self.InitframeTime = time.time()
                self.clock = self.InitframeTime  - self.start_time
                self.window.bind("<Key>", self.Partie.ActionJoueur)
                self.frame = abs((math.floor(self.clock*(self.Partie.Niveau/3))) % - 2)
                if self.frame != self.frame_buffer :
                    self.Partie.position_ennemis_update()  
                    self.Partie.fTirsEnnemi()
                self.frame_buffer = self.frame
                self.Partie.clock_update(self.frame,self.clock)
                self.myScore.set('SCORE : {} (Record : {})'.format(str(self.Partie.Score), self.Partie.TopScore))   
                frameTime = time.time() - self.InitframeTime
                self.stayLife.set('VIES : '  + str(self.Partie.Vie)) #str(round(1/frameTime))) # str(Partie.Vie))
                if frameTime < 0.03333:
                    time.sleep(0.03333 - frameTime)
                self.window.update()
            except:
                break
            
        if int(self.Partie.Score) > int(self.Partie.TopScore):
            open(self.Partie.texteFile, 'w').write(str(self.Partie.Score))
        self.Partie.Pause = True 
        self.Canevas.delete("all")
        texte1 = "Game Over ! Vous etes mort au niveau {}. Votre score est de {}.".format(self.Partie.Niveau,str(self.Partie.Score))
        texte2 = "Appuyez sur New Game pour relancer"
        TextId1 = self.Canevas.create_text(320,300, font = ("Terminal", 20), text = texte1, fill = '#FFFFFF')
        TextId2 = self.Canevas.create_text(340,330, font = ("Terminal", 20), text = texte2, fill = '#FFFFFF')
        self.window.mainloop()

    def restart(self):
        try:
            
            self.Canevas.delete("all")
            self.Partie.Pause = True 
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