from entity import Entity


class EntityEnnemiSpecial(Entity):
    """Sous-classe pour les ennemis speciaux"""

    def slidingSpecial(self, pDirection, pCanevas):
        """
        Méthode permettant le déplacement des ennemis spéciaux.
        Parameters
        ----------
        pDirection : String
            'l' ou 'r' selon la direction choisie par createSpecialEntities.
        pCanevas : tkinter canevas
            Nécessaire pour l'interface graphique.
        Returns
        -------
        None.
        """

        if pDirection == 'r':
            pCanevas.move(self.imageOnCanvas, 5, 0)
            self.Position = [self.Position[0] + 5, self.Position[1]]
        else:
            pCanevas.move(self.imageOnCanvas, -5, 0)
            self.Position = [self.Position[0] - 5, self.Position[1]]