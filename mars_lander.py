from data import *

import pygame, random
import numpy as np

from time import sleep

from vaisseau import Vaisseau
from jeu import Jeu
from affichage import Affichage
from surface import Surface
from ia_learning import IALearning


scenar = scenario1

# Initialisation des objets
v = Vaisseau()
v.init_vaisseau(scenar['vaisseau'])
s = Surface(scenar['surface_mars'])
a = Affichage()
j = Jeu(scenar)

actions = j.actions_possibles()

ia = IALearning(actions, alpha, gamma, epsilon, epsilon_decay, ia_active)

s.calcul_zone_atterissage(scenar)

clock = pygame.time.Clock()

# Boucle Pygame

while True:
    clock.tick(img_par_sec)
    # Fermeture
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    etat = ia.recupere_etat(v, s)
    ia_action = ia.choisir_action(etat)
    
    # Gestion clavier
    keys = pygame.key.get_pressed()
    v = j.actions_clavier(keys, v, ia_action)

    # Actualisation de l'état et affichage
    j.actualisation(v, a, s, ia)
    j.touche_mars(a, v, s)

    s.se_rapproche_de_la_zone(v, scenar)

    # Calcul de la récompense et mise à jour
    recompense = ia.recupere_recompense(a, v, s)
    next_etat = ia.recupere_etat(v, s)
    ia.update_q_table(etat, ia_action, recompense, next_etat)
    
    # Mise à jour d'exploration
    ia.decay_epsilon()

    v.peut_atterir()
    j.fin_du_jeu(v)
    
    # Vérifier fin du jeu et relancer si nécessaire
    if (v.detruit or v.est_pose) and ia_active:
    
        v = j.je_relance_le_jeu(v, scenar)



