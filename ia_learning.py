import random
import numpy as np
from data import *

class IALearning:
    def __init__(self, scenar, actions, alpha, gamma, epsilon, epsilon_decay, ia_active):
        self.scenar = scenar
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.q_table = {}
        self.recompense = 0
        self.recompenses_cumulees = []
        self.ia_active = ia_active

    def recupere_etat(self, v, s, scenar):
        if self.ia_active:
            return (int(v.x), int(v.y), int(v.h_speed), int(v.v_speed), int(v.angle), int(v.fuel),
                    s.est_dans_la_zone(v), s.se_rapproche_de_la_zone(v), s.calcul_zone_atterissage(scenar))

    def choisir_action(self, etat):
        if self.ia_active:
            if random.uniform(0, 1) < self.epsilon:
                return random.choice(self.actions)  # Exploration
            else:
                return self.meilleure_action(etat)  # Exploitation

    def meilleure_action(self, etat):
        if self.ia_active:
            if etat not in self.q_table:
                self.q_table[etat] = np.zeros(len(self.actions))
            return self.actions[np.argmax(self.q_table[etat])]

    def update_q_table(self, etat, action, recompense, next_etat):
        if self.ia_active:
            if etat not in self.q_table:
                self.q_table[etat] = np.zeros(len(self.actions))
            if next_etat not in self.q_table:
                self.q_table[next_etat] = np.zeros(len(self.actions))

            action_index = self.actions.index(action)
            best_future_q = np.max(self.q_table[next_etat])
            
            # Equation de mise à jour Q-learning
            self.q_table[etat][action_index] += self.alpha * (recompense + self.gamma * best_future_q - self.q_table[etat][action_index])

    def recupere_recompense(self, a, v, s):
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
            self.recompense += 2     if not v.detruit and not v.est_pose else 0
            self.recompense += 12    if not v.detruit and v.est_pose else -10
            self.recompense += 10    if v.detruit and v.est_pose else -10
            self.recompense += 7     if v.peut_atterir() else -1
            self.recompense += 5     if -30 <= abs(v.angle) <= 30 else -1
            self.recompense += 2     if abs(v.h_speed) < max_h_speed else 0
            self.recompense += 2     if abs(v.v_speed) < max_v_speed else 0
            self.recompense += 10    if s.est_dans_la_zone(v) else -10
            self.recompense += 10    if s.se_rapproche_de_la_zone(v) else -10


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
