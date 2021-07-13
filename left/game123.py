import pygame

screen = pygame.display.set_mode((800, 600))
game = True
x = 400
y = 300
clock = pygame.time.Clock()
FPS = 45
paddle1 = pygame.Rect((300, 0, 200, 25))
paddle2 = pygame.Rect((300, 600, 200, 25))
circle = pygame.Rect((300, 400, 60, 60))
speed = 1
while game:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            game = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] == True:
        paddle1.x -= 1
    if keys[pygame.K_RIGHT] == True:
        paddle1.x += 1
    circle.y += speed
    if circle.bottom >= 600:
        speed = -1

    screen.fill((0, 0, 255))
    pygame.draw.circle(screen, (255, 0, 0), circle.center, 30)
    pygame.draw.rect(screen, (255, 0, 0), paddle1)
    pygame.display.update()
