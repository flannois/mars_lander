import pygame
from data import *
from vaisseau import Vaisseau

class Jeu:
    def __init__(self, scenar):
        self.tentative = 0
        self.att_reussi = 0
        self.scenar = scenar

    def actualisation(self, v, a, s, ia):
        # VAISSEAU
        v.actualisation()
        v.verif_si_HS()

    def affichage_du_jeu(self, a, v, s, ia):
        # AFFICHAGE
        a.effacer_tout()
        a.ecrire_info(v, ia, self)
        a.dessiner_vaisseau(v, self)
        a.dessiner_surface(s.mars_surface)
        
        pygame.display.flip()
            
    def touche_mars(self, a, v, s):
        points = []
        for i in range(len(s.mars_surface) - 1):
            pt1, pt2 = s.mars_surface[i]
            pt3, pt4 = s.mars_surface[i + 1]
            pt1 = pt1 // echelle
            pt2 = pt2 // echelle
            pt3 = pt3 // echelle
            pt4 = pt4 // echelle

            points.append(((pt1, pt2), (pt3, pt4)))
        
        atterissage = True if any(a.rect.clipline(*point) for point in points) else False
    
        if atterissage:
            if s.est_dans_la_zone(v) and v.peut_atterir() and not v.detruit:
                self.est_gagne = True
                v.est_pose = True
                self.att_reussi += 1
                
            else:
                self.est_gagne = False
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
        v.init_vaisseau(self.scenar['vaisseau'])

        return v
    
    def actions_clavier(self, keys, v, ia_action):
        if keys[pygame.K_SPACE]:
            
            v = self.je_relance_le_jeu(v)
        
        if not v.detruit and not v.est_pose:
            if not ia_active:
                if keys[pygame.K_RIGHT]:
                    v.angle -= degres_par_tour
                if keys[pygame.K_LEFT]:
                    v.angle += degres_par_tour
                if keys[pygame.K_1]:
                    v.puissance = 0
                if keys[pygame.K_2]:
                    v.puissance = 1
                if keys[pygame.K_3]:
                    v.puissance = 2
                if keys[pygame.K_4]:
                    v.puissance = 3
                if keys[pygame.K_5]:
                    v.puissance = 4

            else:
                v.angle, v.puissance = ia_action

            """
            if keys[pygame.K_RIGHT] or ia_action == 'right':
                v.angle -= degres_par_tour
            if keys[pygame.K_LEFT] or ia_action == 'left':
                v.angle += degres_par_tour
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
            """
      


        return v
    
    def toutes_actions_possibles(self, v):
        self.toutes_les_actions = []
        for a in range(5):
            for b in range(-6, 7):
                self.toutes_les_actions.append((b*degres_par_tour , a))

        #actions = []
        #actions.append('right')
        #actions.append('left') 
        #actions.append('0')
        #actions.append('1')   
        #actions.append('2')
        #actions.append('3')
        #actions.append('4')
        
        return self.toutes_les_actions
    
    def recup_actions_possibles(self, v):

        actions_possibles = []
        for action in self.toutes_les_actions:
            angle, puissance = action
            if (v.angle != angle_vaisseau_max or v.angle != -angle_vaisseau_max) and \
                (v.puissance <= 4 or v.puissance <= 0):

                if (v.angle - 15 == angle or v.angle + 15 == angle or v.angle == angle) and \
                (puissance + 1 == v.puissance or puissance - 1 == v.puissance or puissance == v.puissance):
                    
                    actions_possibles.append(action)

        
        
 
        return actions_possibles
        