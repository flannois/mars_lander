from data import *
import pygame

import math
import numpy as np

import random
from time import sleep
class Vaisseau:
    def init_vaisseau(self, info):
        self.x =            info['x']
        self.y =            fenY - info['y']
        self.h_speed =      info['h_speed']
        self.v_speed =      info['v_speed']
        self.fuel =         info['fuel']
        self.angle =        info['rotate']
        self.puissance =    info['power']
        self.detruit =      False
        self.est_pose =     False

    def en_dehors_de_la_zone(self):
        if not 0 < self.x < fenX or not 0 < self.y < fenY:
            return True
        else:
            return False

    def verif_si_HS(self):
        if self.en_dehors_de_la_zone():
            self.detruit = True
            return True
        else:
            return False

    def a_plus_dessence(self):
        if self.fuel <= 0:
            self.fuel = 0
            return True
        else:
            return False

    def actualisation(self):
        if self.fuel <= 0 or self.detruit or self.est_pose:
            self.puissance = 0
        
        if not self.detruit and not self.est_pose:
           
            self.fuel -= self.puissance
        
            # Calcul des vitesses
            self.v_speed += gravite

            # Conversion en radians
            angle_radians = math.radians(self.angle)

            # Calcul du sinus et du cosinus
            sin = math.sin(angle_radians)
            cos = math.cos(angle_radians)

            # Calcul trigo pour vitesse
            self.v_speed -= self.puissance * cos
            self.h_speed -= self.puissance * sin

            # Calcul des positions
            self.y += self.v_speed
            self.x += self.h_speed

    def peut_atterir(self):
        if self.angle == 0 and abs(self.v_speed) < max_v_speed and abs(self.h_speed) < max_h_speed:
            return True
        else:
            return False
        

class Surface:
    def __init__(self, mars_surface):
        self.mars_surface = mars_surface

    def calcul_zone_atterissage(self):
        surf = scenar['surface_mars']
        for i in range(len(surf) -1):
            p1X, p1Y = surf[i]
            p2X, p2Y = surf[i+1]
            if p1Y == p2Y:
                self.atterissage = ((p1X, p1Y),(p2X, p2Y))

    def est_dans_la_zone(self,v):
        zoneAtterissageGauche, zoneAtterissageDroite = self.atterissage
        if zoneAtterissageGauche[0] < v.x < zoneAtterissageDroite[0]:
            return True
        else:
            return False
   

class Affichage:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Mars Lander IA')
        
        # Initialisation de la fenêtre
        self.fenX = fenX // echelle
        self.fenY = fenY // echelle
        self.screen = pygame.display.set_mode((self.fenX, self.fenY))

        # Couleur de l'arrière-plan
        self.BLANC = (255, 255, 255)
        self.ROUGE = (255, 0, 0)

    # Fonction pour dessiner la surface de Mars
    def dessiner_surface(self, surface_mars):
        for i in range(len(surface_mars) - 1):
            x1, y1 = surface_mars[i]
            x1, y1 = x1 // echelle, y1 // echelle
            x2, y2 = surface_mars[i + 1]
            x2, y2 = x2 // echelle, y2 // echelle

            pygame.draw.line(self.screen, self.ROUGE, (x1, self.fenY - y1), (x2, self.fenY - y2), 10)

    def dessiner_vaisseau(self, vaisseau, j):
        
        if not vaisseau.detruit:
            img = f'images/vaisseau{vaisseau.puissance}.png'
        else:
            img = "images/detruit.png"
        
        if vaisseau.est_pose:
            img = "images/vaisseauA.png"
        
        image = pygame.image.load(img)
        image = pygame.transform.rotate(image, vaisseau.angle)  # Pour incliner l'image selon l'angle
        self.rect = image.get_rect(center=(vaisseau.x // echelle, vaisseau.y // echelle))
        self.screen.blit(image, self.rect)

    def effacer_tout(self):
        self.screen.fill(self.BLANC)

    def affiche_info(self, nom, valeur, pos):
        font = pygame.font.Font(None, 36)
        valeur = round(valeur, 3)
        text = f"{nom} : {valeur}"
        text_a_afficher = font.render(text, True, NOIR)
        self.screen.blit(text_a_afficher, pos)

    def traduction_angle(self, angle):
        calcul = angle % 360
        return calcul

    def ecrire_info(self, vaisseau, ia, j):
        self.affiche_info("x",          vaisseau.x,         (10,0))
        self.affiche_info("y",          vaisseau.y,         (10,25))
        self.affiche_info("v_speed",    vaisseau.v_speed,   (10,50))
        self.affiche_info("h_speed",    vaisseau.h_speed,   (10,75))
        self.affiche_info("fuel",       vaisseau.fuel,      (10,100))
        self.affiche_info("angle",      self.traduction_angle(vaisseau.angle) , (10,125))
        self.affiche_info("puissance",  vaisseau.puissance, (10,150))
        self.affiche_info("gravite",    gravite,            (10,175))

        self.affiche_info("Tx ap",      ia.alpha,           (1000,0))
        self.affiche_info("Rec fut",    ia.gamma,           (1000,25))
        self.affiche_info("Tx exp",     ia.epsilon,         (1000,50))
        self.affiche_info("Tx ap",      ia.epsilon_decay,   (1000,75))
        
        self.affiche_info("Tentative",  j.tentative,        (1000,125))
        self.affiche_info("Atterissages",  j.att_reussi,    (1000,150))

        self.affiche_info("Récompense",  ia.recompense,         (1000,200))

        

        self.affiche_info("Img/sec",  img_par_sec,   (500,10))

class Jeu:
    def __init__(self):
        self.tentative = 0
        self.att_reussi = 0

    def actualisation(self, v, a, s):
        # VAISSEAU
        v.actualisation()
        v.verif_si_HS()

        # AFFICHAGE
        a.effacer_tout()
        a.ecrire_info(v, ia, j)
        a.dessiner_vaisseau(v, self)
        a.dessiner_surface(s.mars_surface)
        
        pygame.display.flip()
            
    def touche_mars(self, a, v, s):
        points = []
        for i in range(len(s.mars_surface) - 1):
            pt1, pt2 = s.mars_surface[i]
            pt3, pt4 = s.mars_surface[i + 1]

            pt1 = pt1 // echelle
            pt2 = (fenY // echelle) - (pt2 // echelle)
            pt3 = pt3 // echelle
            pt4 = (fenY // echelle) - (pt4 // echelle)

            points.append(((pt1, pt2), (pt3, pt4)))

        atterissage = True if any(a.rect.clipline(*point) for point in points) else False
        
        if atterissage:
            if s.est_dans_la_zone(v) and v.peut_atterir() and not v.detruit:
                j.est_gagne = True
                v.est_pose = True
                self.att_reussi += 1
                sleep(1)
            else:
                j.est_gagne = False
                v.detruit = True
            self.fin_du_jeu(v)
           
    def fin_du_jeu(self, v):
        if v.detruit or v.est_pose:
            v.v_speed = 0
            v.h_speed = 0
            
    def je_relance_le_jeu(self, v):
        self.tentative += 1
        v = None
        v = Vaisseau()
        v.init_vaisseau(scenar['vaisseau'])
        return v
    
    def actions_clavier(self, keys, v, ia_action):
        
        if keys[pygame.K_SPACE]:
            v = self.je_relance_le_jeu(v)
        
        if not v.detruit and not v.est_pose:
            if keys[pygame.K_LEFT] or ia_action == 'left':
                v.angle += degres_par_tour
            if keys[pygame.K_RIGHT] or ia_action == 'right':
                v.angle -= degres_par_tour
            if keys[pygame.K_1] or ia_action == '0':
                v.puissance = 0
            if keys[pygame.K_2] or ia_action == '1':
                v.puissance = 1
            if keys[pygame.K_3] or ia_action == '2':
                v.puissance = 2
            if keys[pygame.K_4] or ia_action == '3':
                v.puissance = 3
            if keys[pygame.K_5] or ia_action == '4':
                v.puissance = 4
        return v
    
    def actions_possibles(self):
        actions = []
        actions.append('left')
        actions.append('right')
        actions.append('0')
        actions.append('1')
        actions.append('2')
        actions.append('3')
        actions.append('4')
        
        return actions
        

class IALearning:
    def __init__(self, actions, alpha=0.1, gamma=0.9, epsilon=1.0, epsilon_decay=0.995):
        # Liste des actions possibles : inclinaison et niveaux de puissance
        self.actions = actions
        self.alpha = alpha          # Taux d'apprentissage
        self.gamma = gamma          # Facteur de récompense future
        self.epsilon = epsilon      # Taux d'exploration
        self.epsilon_decay = epsilon_decay
        self.q_table = {}           # Table Q pour stocker les états et les actions
        self.recompense = 0

    def recupere_etat(self, vaisseau, surface):
        # État défini par position, vitesse horizontale et verticale, carburant, et si en zone d'atterrissage
        return (int(vaisseau.x), int(vaisseau.y), 
                int(vaisseau.h_speed), int(vaisseau.v_speed),
                int(vaisseau.angle), int(vaisseau.fuel),
                surface.est_dans_la_zone(vaisseau))

    def choisir_action(self, etat):
        # Choisir une action basée sur l'état courant en utilisant epsilon-greedy
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions)  # Exploration
        else:
            return self.meilleure_action(etat)  # Exploitation

    def meilleure_action(self, etat):
        # Trouver la meilleure action pour un état donné
        if etat not in self.q_table:
            self.q_table[etat] = np.zeros(len(self.actions))  # Initialiser si pas dans Q-table
        return self.actions[np.argmax(self.q_table[etat])]

    def update_q_table(self, etat, action, recompense, next_etat):
        # Mise à jour de la Q-table pour améliorer la prise de décision
        if etat not in self.q_table:
            self.q_table[etat] = np.zeros(len(self.actions))
        if next_etat not in self.q_table:
            self.q_table[next_etat] = np.zeros(len(self.actions))

        # Indice de l'action pour mise à jour
        action_index = self.actions.index(action)
        best_future_q = np.max(self.q_table[next_etat])
        
        # Equation de mise à jour Q-learning
        self.q_table[etat][action_index] += self.alpha * (recompense + self.gamma * best_future_q - self.q_table[etat][action_index])

    def recupere_recompense(self, a, v, s):
        
        recompense = 100 - abs(v.v_speed) - abs(v.h_speed)
        
        # Récompense pour encourager un atterrissage stable
        if v.est_pose:
            recompense += 100  # Récompense élevée pour un atterrissage réussi
        if v.detruit:
            recompense -= 100  # Pénalité pour un crash
            
        # Récompenses pour contrôle et stabilité
        if abs(v.angle) == 0:
            recompense += 20
        else:
            recompense -= 20

        # Récompenses pour contrôle de vitesse
        if v.x < max_h_speed:
            recompense += 5
        else:
            recompense -= 5
        
        if v.y < max_h_speed:
            recompense += 5
        else:
            recompense -= 5
        

        if v.en_dehors_de_la_zone:
            recompense -= 5
        elif s.est_dans_la_zone(v):
            recompense += 5

  

        self.recompense = recompense
        return recompense

    def decay_epsilon(self):
        # Réduire l'exploration au fil du temps
        self.epsilon = max(0.01, self.epsilon * self.epsilon_decay)

    def ia_appui(self, key):
        return key

scenar = scenario0

# Initialisation des objets
v = Vaisseau()
v.init_vaisseau(scenar['vaisseau'])
s = Surface(scenar['surface_mars'])
a = Affichage()
j = Jeu()

actions = j.actions_possibles()

ia = IALearning(actions)

s.calcul_zone_atterissage()

clock = pygame.time.Clock()

# Boucle Pygame

while True:
    clock.tick(img_par_sec)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    etat = ia.recupere_etat(v, s)
    ia_action = ia.choisir_action(etat)
    

    keys = pygame.key.get_pressed()
    j.actions_clavier(keys, v, ia_action)

    # Actualisation de l'état et affichage
    j.actualisation(v, a, s)
    j.touche_mars(a, v, s)

    # Calcul de la récompense et mise à jour
    recompense = ia.recupere_recompense(a, v, s)
    next_etat = ia.recupere_etat(v, s)
    ia.update_q_table(etat, ia_action, recompense, next_etat)
    
    # Mise à jour d'exploration
    ia.decay_epsilon()

    v.peut_atterir()
    
    j.fin_du_jeu(v)
     

    # Vérifier fin du jeu et relancer si nécessaire
    if v.detruit or v.est_pose:
        v = j.je_relance_le_jeu(v)



