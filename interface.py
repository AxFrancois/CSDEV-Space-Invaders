from tkinter import *

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
window.config(bg='#2D9484')

leftFrame = Frame(window, bg='#9C4044')
leftFrame.grid(row=0, column=0, padx=(0, 0))

stayLife = StringVar()
stayLife.set('')
lifeLabel = Label(leftFrame, textvariable=stayLife, fg='#FFFFFF')
lifeLabel.grid(row=0, column=1,)

myScore = StringVar()
myScore.set('')
scoreLabel = Label(leftFrame, textvariable=myScore, fg='#FFFFFF')
scoreLabel.grid(row=0, column=0,)

Canevas = Canvas(leftFrame, width=650, height=450, bg='#000000', highlightthickness=0)
Canevas.grid(row=1, column=0,)










menuBar = Menu(window)
menuGame = Menu(menuBar, tearoff=0)
menuGame.add_command(label="Rejouer", command="")
menuGame.add_command(label="Quitter", command=window.quit)
menuBar.add_cascade(label="Jeux", menu=menuGame)
window.config(menu=menuBar)

window.mainloop()