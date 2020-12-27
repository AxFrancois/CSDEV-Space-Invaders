from tkinter import *
import classes as cl
import random, time, math


def key_pressed(event):
     print("Key Pressed:"+event.keysym)


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
window.resizable(width=False, height=False)
window.config(bg='#A2A4AA')

leftFrame = Frame(window, bg='#000000')
leftFrame.grid(row=0, column=0)

rightFrame = Frame(window, bg='#A2A4AA')
rightFrame.grid(row=0, column=1)

stayLife = StringVar()
stayLife.set('LIVES')
lifeLabel = Label(leftFrame, textvariable=stayLife, bg='#000000', fg='#FFFFFF', font=("Terminal", 11))
lifeLabel.grid(row=0, column=0,padx=(550, 0))

myScore = StringVar()
myScore.set('SCORE')
scoreLabel = Label(leftFrame, textvariable=myScore, bg='#000000', fg='#FFFFFF', font=("Terminal", 11))
scoreLabel.grid(row=0, column=0, padx=(0, 600))

Canevas = Canvas(leftFrame, width=650, height=479, bg='#000000', highlightthickness=0)
Canevas.grid(row=1, column=0,)

replayButton = Button(rightFrame, text='New game', bg='#A2A4AA', fg='#000000', font=('Terminal', 10), command="")
replayButton.grid(row=0, column=0, pady=(0, 50), padx=(20, 0))

quitButton = Button(rightFrame, text='Quitter', bg='#A2A4AA', fg='#000000', font=('Terminal', 10), command=window.quit)
quitButton.grid(row=1, column=0, pady=(50, 0), padx=(20, 0))

menuBar = Menu(window)
menuGame = Menu(menuBar, tearoff=0)
menuGame.add_command(label="Rejouer", command="")
menuGame.add_command(label="Quitter", command=window.quit)
menuGame.add_command(label="A propos", command="")
menuBar.add_cascade(label="Jeux", menu=menuGame)
window.config(menu=menuBar)


Partie = cl.Game(window,Canevas)
myScore.set('SCORE : ' + str(Partie.Score))
Partie.clock_update(0)

clock = 0
delay = round(1/60, 4)

while Partie.Vie != 0:
    window.bind("<Key>", Partie.ActionJoueur)
    clock = round(clock + delay,4)
    frame = abs((math.floor(clock*2)) % - 2)
    Partie.clock_update(frame)  
    time.sleep(delay) 
    window.update()
