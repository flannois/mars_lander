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
        print(points)
        #atterissage = True if any(a.rect.clipline(*point) for point in points) else False
        atterissage = False
        for point in points:
            
            if any(a.rect.clipline(*point)):
                print(points)
                print(point, v.x, v.y)
                
                atterissage = True

        if atterissage:
            print()
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
        actions.append('right')
        actions.append('left') 
        actions.append('0')
        actions.append('1')   
        actions.append('2')
        actions.append('3')
        actions.append('4')
        
        return actions