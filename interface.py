from tkinter import *
import classes as cl
import random

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

Alien1 = PhotoImage(master=window, file='PixelArts/Alien_1.gif')
Alien2 = PhotoImage(master=window, file='PixelArts/Alien_2.gif')
Alien3 = PhotoImage(master=window, file='PixelArts/Alien_3.gif')
Alien4 = PhotoImage(master=window, file='PixelArts/Alien_4.gif')
Explosion = PhotoImage(master=window, file='PixelArts/Explosion.gif')
Player = PhotoImage(master=window, file='PixelArts/Player.gif')
Protection = PhotoImage(master=window, file='PixelArts/Protection.gif')


Partie = cl.Game()
myScore.set('SCORE : ' + str(Partie.Score))
Partie.createEntities()
Partie.update(window,Canevas)

"""
for items in Partie.update(window,Canevas):
    print(items)
    PixelArt = PhotoImage(master=window, file='PixelArts/' + items.afficher()[1])
    Canevas.create_image(items.afficher()[0][0], items.afficher()[0][1], image=PixelArt)
    """

"""
Canevas.create_image(50, 400, image=Alien1)
Canevas.create_image(50, 450, image=Alien1)
"""
"""
class Game:
    def __int__(self,Alien1):
        self.Alien1 = Alien1

    def alienDispplay(self,Alien1):
        for i in range(1,16):
            Canevas.create_image(50*i, 50, image=Alien1)
"""

menuBar = Menu(window)
menuGame = Menu(menuBar, tearoff=0)
menuGame.add_command(label="Rejouer", command="")
menuGame.add_command(label="Quitter", command=window.quit)
menuGame.add_command(label="A propos", command="")
menuBar.add_cascade(label="Jeux", menu=menuGame)
window.config(menu=menuBar)

window.mainloop()