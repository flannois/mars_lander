from data import *
import pickle
import pygame

import datetime

from vaisseau import Vaisseau
from jeu import Jeu
from affichage import Affichage
from surface import Surface
from ia_learning import IALearning


scenar = scenario0

# Initialisation des objets
v = Vaisseau()
v.init_vaisseau(scenar['vaisseau'])
s = Surface(scenar['surface_mars'])
a = Affichage()
j = Jeu(scenar)

toutes_actions_possible = j.toutes_actions_possibles(v)

ia = IALearning(scenar, toutes_actions_possible, alpha, gamma, epsilon, epsilon_decay, ia_active)

s.calcul_zone_atterissage(scenar)

clock = pygame.time.Clock()

# Boucle Pygame

while True:
    ia.recupere_historique()
    ia.supprimer_historique()
    clock.tick(img_par_sec)
    # Fermeture
    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            nom = f"{str(datetime.datetime.now()).replace(' ','_').replace(":","-")}.txt"
            with open(f"historique/{nom}", "wb") as f:
                pickle.dump(ia.q_table, f)
                
            
            pygame.quit()
    
    etat = ia.recupere_etat(v, s)
    

    actions_possibles = j.recup_actions_possibles(v)

    ia_action = ia.choisir_action(etat)
        
    # Gestion clavier
    keys = pygame.key.get_pressed()
    v = j.actions_clavier(keys, v, ia_action)

    # Actualisation de l'état et affichage
    j.actualisation(v, a, s, ia)

    j.affichage_du_jeu(a, v, s, ia)
    j.touche_mars(a, v, s)

    s.se_rapproche_de_la_zone(v)

    # Calcul de la récompense et mise à jour
    recompense = ia.recupere_recompense(a, v, s, j)
    ia.ajout_recompense_cumulative(recompense)
    next_etat = ia.recupere_etat(v, s)
    ia.update_q_table(etat, ia_action, recompense, next_etat)
    
    # Mise à jour d'exploration
    ia.decay_epsilon()

    v.peut_atterir()
    j.fin_du_jeu(v)

    

    if affiche_espion:
        espion = ""
        if v.en_dehors_de_la_zone(): espion += "en_dehors_de_la_zone "
        if v.peut_atterir(): espion += "peut_atterir "
        if s.est_a_droite_de_la_zone(v): espion += "est_a_droite_de_la_zone "
        if s.est_a_gauche_de_la_zone(v): espion += "est_a_gauche_de_la_zone "
        if s.est_dans_la_zone(v): espion += "est_dans_la_zone "
        if s.est_en_bas_de_la_zone(v): espion += "est_en_bas_de_la_zone "
        if s.est_en_haut_de_la_zone(v): espion += "est_en_haut_de_la_zone "
        if s.se_rapproche_de_la_zone(v): espion += "se_rapproche_de_la_zone "
        if s.va_a_droite(v): espion += "va_a_droite "
        if s.va_a_gauche(v): espion += "va_a_gauche "
        if s.va_en_bas(v): espion += "va_en_bas "
        if s.va_en_haut(v): espion += "va_en_haut "
        if v.detruit: espion += "detruit "
        if v.est_pose: espion += "pose "
        print(espion)
    
    # Vérifier fin du jeu et relancer si nécessaire
    if (v.detruit or v.est_pose) and ia_active:
    
        v = j.je_relance_le_jeu(v)



