# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 13:30:28 2020

@author: Alexis Pincemin & Axel François
github : https://github.com/AxFrancois/Space-Invaders
"""

# %%----------------------Import----------------------------------------------#

from tkinter import *
import random, time, math
import classes as cl

# %%----------------------Fonctions de test-----------------------------------#

def key_pressed(event):
     print("Key Pressed:"+event.keysym)


# %%----------------------Interface graphique---------------------------------#

window = Tk()

window.title('Space invaders')
width = 750
height = 500
#on centre la fenêtre sur l'écran
widthScreen = window.winfo_screenwidth()
heightScreen = window.winfo_screenheight()
x = (widthScreen // 2) - (width // 2)
y = (heightScreen // 2) - (height // 2)
window.geometry('{}x{}+{}+{}' .format(width, height, x, y))
window.resizable(width = False, height = False)
window.config(bg = '#A2A4AA')

leftFrame = Frame(window, bg = '#000000')
leftFrame.grid(row=0, column=0)

rightFrame = Frame(window, bg = '#A2A4AA')
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
                      fg = '#000000', font = ('Terminal', 10), command = "")
replayButton.grid(row = 0, column = 0, pady = (0, 50), padx = (20, 0))

quitButton = Button(rightFrame, text = 'Quitter', bg = '#A2A4AA',
                    fg = '#000000', font = ('Terminal', 10),
                    command = window.destroy)
quitButton.grid(row = 1, column = 0, pady = (50, 0), padx = (20, 0))

menuBar = Menu(window)
menuGame = Menu(menuBar, tearoff = 0)
menuGame.add_command(label = "Rejouer", command = "")
menuGame.add_command(label = "Quitter", command = window.destroy)
menuGame.add_command(label = "A propos", command = "")
menuBar.add_cascade(label = "Jeux", menu = menuGame)
window.config(menu = menuBar)

# %%----------------------Initialisations-------------------------------------#

niveau = 1
Partie = cl.Game(window,Canevas)
myScore.set('SCORE : ' + str(Partie.Score))
Partie.clock_update(0,0)
frame_buffer = 0
start_time = time.time()
texte = "Niveau {} GO !".format(niveau)
TextId = Canevas.create_text(320,300, font = ("Terminal", 20), text = texte, fill = '#FFFFFF')


# %%----------------------Boucle principale-----------------------------------#

while Partie.Vie != 0:
    #try:
        """
        if TextId != None and frame_buffer != 0:
            time.sleep(2)
            Canevas.delete(TextId)
            TextId = None
            print("OUI")"""
        if Partie.OnAGagneChef() == True:
            niveau += 1
            texte = "Niveau {} GO !".format(niveau)
            TextId = Canevas.create_text(320,300, font = ("Terminal", 20), text = texte, fill = '#FFFFFF')
            time.sleep(2)
            Canevas.delete(TextId)
            Partie.PlayAgain(niveau)
            start_time = time.time()
            
        InitframeTime = time.time()
        clock = InitframeTime  - start_time
        window.bind("<Key>", Partie.ActionJoueur)
        frame = abs((math.floor(clock*(Partie.difficulte/2))) % - 2)
        if frame != frame_buffer :
            Partie.position_ennemis_update()  
        frame_buffer = frame
        Partie.clock_update(frame,clock)
        myScore.set('SCORE : ' + str(Partie.Score))
        #print("--- %s seconds ---" % (time.time() - InitframeTime))
        frameTime = time.time() - InitframeTime
        if frameTime < 0.03333:
            time.sleep(0.03333 - frameTime)
            #print("wait a minute")
        window.update()
    #except:
    #    break