import pygame
from data import *

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
        print(surface_mars)
        for i in range(len(surface_mars) - 1):
            x1, y1 = surface_mars[i]
            x1, y1 = x1 // echelle, y1 // echelle
            x2, y2 = surface_mars[i + 1]
            x2, y2 = x2 // echelle, y2 // echelle

            pygame.draw.line(self.screen, self.ROUGE, (x1, y1), (x2, y2), 10)

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

        self.affiche_info("Img/sec",  img_par_sec,   (500,10))

        if ia_active:
            self.affiche_info("Tx ap",      ia.alpha,           (1000,0))
            self.affiche_info("Rec fut",    ia.gamma,           (1000,25))
            self.affiche_info("Tx exp",     ia.epsilon,         (1000,50))
            self.affiche_info("Tx ap",      ia.epsilon_decay,   (1000,75))
            
            self.affiche_info("Tentative",  j.tentative,        (1000,125))
            self.affiche_info("Atterissages",  j.att_reussi,    (1000,150))

            self.affiche_info("Récompense",  ia.recompense,         (1000,200))
        