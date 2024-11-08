
import random
import numpy as np
from data import *
import os
import pickle

class IALearning:
    def __init__(self, scenar, toutes_les_actions, alpha, gamma, epsilon, epsilon_decay, ia_active):
        self.scenar = scenar
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.q_table = {}
        self.recompense = 0
        self.recompenses_cumulees = []
        self.ia_active = ia_active
        self.toutes_les_actions = toutes_les_actions

    def recupere_historique(self):
        if charger_historique and len(self.q_table) == 0:
            fichiers = os.listdir("historique")
            if len(fichiers) > 0:
                fichier_historique = fichiers[-1]
                with open(f"historique/{fichier_historique}", "rb") as f:
                    self.q_table = pickle.load(f)

    def supprimer_historique(self):
        if vider_historique:
            fichiers = os.listdir("historique")
            if len(fichiers) > 0:
                for f in fichiers:
                    os.remove(f"historique/{f}")

    def choisir_action(self, etat):
        if self.ia_active:
            if random.uniform(0, 1) < self.epsilon:
                return random.choice(self.toutes_les_actions)  # Exploration
            else:
                return self.meilleure_action(etat)  # Exploitation

    def meilleure_action(self, etat):
        if self.ia_active:
            if etat not in self.q_table:
                self.q_table[etat] = np.zeros(len(self.toutes_les_actions))
            
            return self.toutes_les_actions[np.argmax(self.q_table[etat])]

    def update_q_table(self, etat, action, recompense, next_etat):
        if self.ia_active:
            if etat not in self.q_table:
                self.q_table[etat] = np.zeros(len(self.toutes_les_actions))
            if next_etat not in self.q_table:
                self.q_table[next_etat] = np.zeros(len(self.toutes_les_actions))
                
           
            action_index = self.toutes_les_actions.index(action)
            best_future_q = np.max(self.q_table[next_etat])
            
            # Equation de mise à jour Q-learning
            self.q_table[etat][action_index] += self.alpha * (recompense + self.gamma * best_future_q - self.q_table[etat][action_index])

    def recupere_etat(self, v, s):
        if self.ia_active:
           
            return (
                #v.en_dehors_de_la_zone(),
                v.peut_atterir(),
                s.est_a_droite_de_la_zone(v),
                s.est_a_gauche_de_la_zone(v),
                s.est_dans_la_zone(v),
                s.est_en_bas_de_la_zone(v),
                s.est_en_haut_de_la_zone(v),
                s.se_rapproche_de_la_zone(v),
                s.va_a_droite(v),
                s.va_a_gauche(v),
                s.va_en_bas(v),
                s.va_en_haut(v),
                #v.detruit,
                #v.est_pose,
                #v.a_plus_dessence,
                v.est_droit(),
                v.detruit,
                v.va_trop_vite_h(),
                v.va_trop_vite_v(),
                
            )
                        
            # Version avant idée BOOLEEN
            """
                return (int(v.x), 
                        int(v.y), 
                        round(v.h_speed,1), 
                        round(v.v_speed,1),
                        float(v.angle), 
                        float(v.fuel),
                        s.est_dans_la_zone(v), 
                        s.se_rapproche_de_la_zone(v), 
                        s.atterissage[0][1],
                        s.atterissage[1][1],
                        v.detruit, v.peut_atterir(), 
                        v.est_pose,
                        )
            """
                 

    def recupere_recompense(self, a, v, s, j):
        if self.ia_active:
            
            self.recompense = 0

            # ChatGPT
            #if not v.detruit:
            #    self.recompense += 2 if not v.est_pose else 100  
            #self.recompense += 3 if v.peut_atterir() else -1
            #self.recompense += 3 if -30 <= abs(v.angle) <= 30 else -1
            #self.recompense += 1 if abs(v.h_speed) < max_h_speed else 0
            #self.recompense += 1 if abs(v.v_speed) < max_v_speed else 0
            #self.recompense += 10 if s.est_dans_la_zone(v) else -10
            #self.recompense += 5 if s.se_rapproche_de_la_zone(v) else -5

            # Flo
            #self.recompense += 1     if not v.detruit and not v.est_pose else -1
            #self.recompense += 100   if not v.detruit and v.est_pose else 0
            #self.recompense += 10    if v.detruit and v.est_pose else 0
            #self.recompense += 7     if v.peut_atterir() else -3
            #self.recompense += 5     if -30 <= abs(v.angle) <= 30 else -1
            #self.recompense += 3     if abs(v.h_speed) < max_h_speed else -2
            #self.recompense += 3     if abs(v.v_speed) < max_v_speed else -2
            #self.recompense += 30    if s.est_dans_la_zone(v) else -1
            #self.recompense += 20    if s.se_rapproche_de_la_zone(v) else -1

            #Flo booleen mode
            
            rec_pos = 3
            


            self.recompense += rec_pos     if s.est_a_droite_de_la_zone(v) and s.va_a_gauche(v) and not s.est_dans_la_zone(v) else 0
            self.recompense += rec_pos     if s.est_a_gauche_de_la_zone(v) and s.va_a_droite(v) and not s.est_dans_la_zone(v) else 0
            self.recompense += rec_pos     if s.est_en_bas_de_la_zone(v) and s.va_en_haut(v) else 0
            self.recompense += rec_pos     if s.est_en_haut_de_la_zone(v) and s.va_en_bas(v) else 0
            self.recompense += rec_pos     if s.se_rapproche_de_la_zone(v) else 0
            self.recompense += rec_pos  if not v.va_trop_vite_h() else 0
            self.recompense += rec_pos  if not v.va_trop_vite_v() else 0
            
            if s.est_dans_la_zone(v):
                self.recompense += 5

                if s.va_en_bas(v):
                    self.recompense += rec_pos

                if v.est_droit():
                    self.recompense += 2
                elif v.est_parfaitement_droit():
                    self.recompense += 5
                else:
                    self.recompense += 0

                if v.peut_atterir():
                    self.recompense += 10
            
            
            self.recompense += rec_pos    if s.est_dans_la_zone(v) else 0
            
            if j.touche_mars(a, v, s):
                self.recompense += 15
                self.recompense += 10       if v.peut_atterir else -10
            
                self.recompense += 3        if v.est_droit() else 0
                self.recompense += 30       if not v.detruit else -30
                self.recompense += 5  if v.h_speed > max_h_speed else -1
                self.recompense += 5  if v.v_speed > max_v_speed else -1
                
                self.recompense += 10       if s.est_dans_la_zone(v) and v.detruit else -10
                self.recompense += 100       if v.est_pose else -10
                
            
            return self.recompense

    def decay_epsilon(self):
        if self.ia_active:
            self.epsilon = max(0.01, self.epsilon * self.epsilon_decay)

    def ajout_recompense_cumulative(self, recompense):
        if self.ia_active:
            if not self.recompenses_cumulees:
                self.recompenses_cumulees.append(recompense)
            else:
                self.recompenses_cumulees.append(self.recompenses_cumulees[-1] + recompense)
    
    def recup_recompense(self):
        return self.recompenses_cumulees[-1] if self.recompenses_cumulees else 0

    def ia_appui(self, key):
        if self.ia_active:
            return key
