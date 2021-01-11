# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 13:30:28 2020

@author: Alexis Pincemin & Axel François
github : https://github.com/AxFrancois/Space-Invaders
"""

# %%----------------------Import----------------------------------------------#

from tkinter import *
import random, time, math, os, sys
import classes as cl

# %%----------------------Fonctions de test-----------------------------------#

def key_pressed(event):
     print("Key Pressed:"+event.keysym)


# %%----------------------Interface graphique---------------------------------#

class main:
    
    def __init__(self):
        self.window = Tk()
        
        self.window.title('Space invaders')
        width = 825
        height = 500
        #on centre la fenêtre sur l'écran
        widthScreen = self.window.winfo_screenwidth()
        heightScreen = self.window.winfo_screenheight()
        x = (widthScreen // 2) - (width // 2)
        y = (heightScreen // 2) - (height // 2)
        self.window.geometry('{}x{}+{}+{}' .format(width, height, x, y))
        self.window.resizable(width = False, height = False)
        self.window.config(bg = '#A2A4AA')
        
        leftFrame = Frame(self.window, bg = '#000000')
        leftFrame.grid(row=0, column=0)
        
        rightFrame = Frame(self.window, bg = '#A2A4AA')
        rightFrame.grid(row = 0, column = 1)
        
        stayLife = StringVar()
        stayLife.set('LIVES')
        lifeLabel = Label(leftFrame, textvariable = stayLife, bg = '#000000', 
                          fg = '#FFFFFF', font = ("Terminal", 11))
        lifeLabel.grid(row = 0, column = 0,padx = (550, 0))
        
        myScore = StringVar()
        myScore.set('SCORE')
        scoreLabel = Label(leftFrame, textvariable = myScore, bg = '#000000',
                           fg = '#FFFFFF', font = ("Terminal", 11))
        scoreLabel.grid(row = 0, column = 0, padx = (0, 600))
        
        Canevas = Canvas(leftFrame, width = 650, height = 479, bg = '#000000',
                         highlightthickness = 0)
        Canevas.grid(row = 1, column = 0,)
        
        replayButton = Button(rightFrame, text = 'New game', bg = '#A2A4AA',
                              fg = '#000000', font = ('Terminal', 10), command = self.restart)
        replayButton.grid(row = 0, column = 0, pady = (0, 50), padx = (20, 0))
        
        quitButton = Button(rightFrame, text = 'Quitter', bg = '#A2A4AA',
                            fg = '#000000', font = ('Terminal', 10),
                            command = self.window.destroy)
        quitButton.grid(row = 1, column = 0, pady = (50, 0), padx = (20, 0))
    
    
    # %%----------------------Initialisations-------------------------------------#
    
        Partie = cl.Game(self.window,Canevas)
        frame_buffer = 0
        myScore.set('SCORE : {} (Record : {})'.format(str(Partie.Score), Partie.TopScore))   
        start_time = time.time()
        texte = "Niveau {} GO !".format(Partie.Niveau)
        TextId = Canevas.create_text(320,300, font = ("Terminal", 20), text = texte, fill = '#FFFFFF')
        while time.time() - start_time < 3:
            self.window.update()
        Canevas.delete(TextId)
    
    # %%----------------------Boucle principale-----------------------------------#
    
        while Partie.Vie >= 0:
            #try:
                if Partie.OnAGagneChef() == True:
                    Partie.LevelUp()
                    texte = "Niveau {} GO !".format(Partie.Niveau )
                    TextId = Canevas.create_text(320,300, font = ("Terminal", 20), text = texte, fill = '#FFFFFF')
                    
                    pause_time = time.time()
                    while time.time() - pause_time < 3:
                        self.window.update()
                    Partie.Pause = False
                    Canevas.delete(TextId)
                    start_time = time.time()
                    
                InitframeTime = time.time()
                clock = InitframeTime  - start_time
                self.window.bind("<Key>", Partie.ActionJoueur)
                frame = abs((math.floor(clock*(Partie.Niveau/3))) % - 2)
                if frame != frame_buffer :
                    Partie.position_ennemis_update()  
                    Partie.fTirsEnnemi()
                frame_buffer = frame
                Partie.clock_update(frame,clock)
                myScore.set('SCORE : {} (Record : {})'.format(str(Partie.Score), Partie.TopScore))   
                frameTime = time.time() - InitframeTime
                stayLife.set('VIES : '  + str(Partie.Vie)) #str(round(1/frameTime))) # str(Partie.Vie))
                if frameTime < 0.03333:
                    time.sleep(0.03333 - frameTime)
                    #print("wait a minute")
                self.window.update()
            #except:
                """
                if int(Partie.Score) > int(Partie.TopScore):
                    open(Partie.texteFile, 'w').write(str(Partie.Score))"""
            #    break
            
        Canevas.delete("all")
        texte1 = "Game Over ! Vous etes mort au niveau {}. Votre score est de {}.".format(niveau,str(Partie.Score))
        texte2 = "Appuyez sur New Game pour relancer"
        TextId1 = Canevas.create_text(320,300, font = ("Terminal", 20), text = texte1, fill = '#FFFFFF')
        TextId2 = Canevas.create_text(340,330, font = ("Terminal", 20), text = texte2, fill = '#FFFFFF')
        self.window.mainloop()

    def restart(self):
        self.window.destroy()
        play = main()



play = main()