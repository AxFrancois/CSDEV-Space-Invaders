# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 15:47:45 2020

@author: Alexis Pincemin & Axel François
github : https://github.com/AxFrancois/Space-Invaders
"""

# %%----------------------Fonctions-------------------------------------------#

def fAuBoutDuBout(pListeDesEnnemis, pDirectionPrecedente):
    """Fonction qui détecte si les aliens sont proche d'un bord et doivent
    changer de dirrection. Elle prend comme entrèe pListeDesEnnemis qui est une
    liste dont chaque élément est une liste contenant tous les ennemis d'une
    ligne et pDirectionPrecedente qui vaut soit l soit r. La fonction retourne
    'l' ou 'r' qui est la direction vers laquelle les ennemis devrons se
    diriger au prochain mouvement.

    Parameters
    ----------
    pListeDesEnnemis : Liste de Liste de d'élement EntityEnnemiClassique
        Liste des ennemis en jeu
    pDirectionPrecedente : String
        'l' ou 'r', ancienne direction (permet de faire une direction par
                                        défaut)

    Returns
    -------
    Moove : String
        'l' ou 'r' selon la nouvelle direction.

    """

    Moove = pDirectionPrecedente
    for i,item in enumerate(pListeDesEnnemis): #Pour chacune des lignes
        if item != []:
            if item[0].Position[0] <= 50:
                #Si l'ennemi le plus a gauche est trop proche de la limite
                Moove = "r"
            elif item[-1].Position[0] >= 600:
                #Si l'ennemi le plus a droite est trop proche de la limite
                Moove = "l"
    return Moove

