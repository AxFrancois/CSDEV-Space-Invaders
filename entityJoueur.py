from tkinter import PhotoImage
from entity import Entity


class EntityJoueur(Entity):
    """Sous-classe pour le joueur"""

    def Mouvement(self, pKey, pCanevas):
        """
        Méthode pour le déplacement du joueur. Le parametre pKey est la touche
        pressé sur le clavier.

        Parameters
        ----------
        pKey : String,
            "Right" ou "Left", permet de savoir la touche que le joueur à
            pressé pour se déplacer

        Returns
        -------
        None.

        """
        if pKey == "Right" and self.Position[0] < 630:
            self.Position[0] += 10
            pCanevas.move(self.imageOnCanvas, 10, 0)
        elif pKey == "Left" and self.Position[0] > 30:
            self.Position[0] -= 10
            pCanevas.move(self.imageOnCanvas, -10, 0)

    def afficherMort(self, pWindow, pCanevas, pPause):
        """
        Méthode d'affichage du joueur lorsqu'il décède à cause du clavier car
        c'est jamais de sa faute. Les parametres pWindow et pCanevas sont
        respectivement la fenêtre et le canvas.

        Parameters
        ----------
        pWindow : tkinter window
            Nécessaire pour l'interface graphique.
        pCanevas : tkinter canevas
            Idem.

        Returns
        -------
        None.

        """
        if pPause == True:
            self.PixelArt = PhotoImage(master=pWindow,
                                       file='PixelArts/' + self.Frame2)
            pCanevas.itemconfig(self.imageOnCanvas, image=self.PixelArt)
        else:
            self.PixelArt = PhotoImage(master=pWindow,
                                       file='PixelArts/' + self.Frame1)
            pCanevas.itemconfig(self.imageOnCanvas, image=self.PixelArt)