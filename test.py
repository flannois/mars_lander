import pygame

pygame.init()
window = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

rect = pygame.Rect(180, 180, 40, 40)
speed = 5
lines = [((20, 300), (150, 20)), ((20, 300), (380, 250)), ((380, 250), (20, 300))]

run = True
while run:
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 

    keys = pygame.key.get_pressed()
    rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * speed
    rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * speed
    rect.centerx %= window.get_width()
    rect.centery %= window.get_height()
    color = "red" if any(rect.clipline(*line) for line in lines) else "green"

    window.fill(0)
    pygame.draw.rect(window, color, rect)
    for line in lines:
        pygame.draw.line(window, "white", *line)
    pygame.display.flip()

pygame.quit()
exit()