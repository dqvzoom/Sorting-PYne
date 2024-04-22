import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
dt = 0

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        background_1 = pygame.image.load("assets\conveyor1.png").convert_alpha()
        background_2 = pygame.image.load("assets\conveyor2.png").convert_alpha()
        background_3 = pygame.image.load("assets\conveyor3.png").convert_alpha()
        background_4 = pygame.image.load("assets\conveyor4.png").convert_alpha()
        self.background_frames = [background_1, background_2, background_3, background_4]
        self.background_index = 0
        self.image = self.background_frames[self.background_index]
        self.rect = self.image.get_rect(center = (960, 540))
    
    def animation_state(self):
        self.background_index += (5 * dt)
        if self.background_index >= len(self.background_frames): self.background_index = 0
        self.image = self.background_frames[int(self.background_index)]
    
    def update(self):
        self.animation_state()

class Arrow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        arrow_1 = pygame.image.load("assets\\arrow1.png").convert_alpha()
        arrow_2 = pygame.image.load("assets\\arrow2.png").convert_alpha()
        arrow_3 = pygame.image.load("assets\\arrow3.png").convert_alpha()
        arrow_4 = pygame.image.load("assets\\arrow4.png").convert_alpha()
        arrow_5 = pygame.image.load("assets\\arrow5.png").convert_alpha()
        arrow_6 = pygame.image.load("assets\\arrow6.png").convert_alpha()
        arrow_7 = pygame.image.load("assets\\arrow7.png").convert_alpha()
        arrow_8 = pygame.image.load("assets\\arrow8.png").convert_alpha()
        arrow_9 = pygame.image.load("assets\\arrow9.png").convert_alpha()
        arrow_10 = pygame.image.load("assets\\arrow10.png").convert_alpha()
        arrow_11 = pygame.image.load("assets\\arrow11.png").convert_alpha()
        arrow_12 = pygame.image.load("assets\\arrow12.png").convert_alpha()
        self.arrow_frames = [arrow_1, arrow_2, arrow_3, arrow_4, arrow_5, arrow_6, arrow_7, arrow_8, arrow_9, arrow_10, arrow_11, arrow_12]
        self.arrow_index = 0
        self.image = self.arrow_frames[self.arrow_index]
        self.rect = self.image.get_rect(topleft = (856, 304))
        global direction
        direction = [0, 1, 0]
    
    def animation_state(self):
        self.arrow_index += (20 * dt)
        if self.arrow_index >= len(self.arrow_frames): self.arrow_index = 0
        self.image = self.arrow_frames[int(self.arrow_index)]
        if direction[0] == 1:
            pygame.transform.rotate(self.image, 0)
        if direction[1] == 1:
            self.image = pygame.transform.rotate(self.image, 270)
        if direction[2] == 1:
            self.image = pygame.transform.rotate(self.image, 180)
    
    def update(self):
        self.animation_state()

def fullscreen():
    if smallest_side == 1:
        game_surface_scaled = pygame.transform.scale(game_surface, (screen.get_height() * 1.77777777778, screen.get_height()))
    else:
        game_surface_scaled = pygame.transform.scale(game_surface(screen.get_width() / 1.77777777778, screen.get_width()))
    screen.blit(game_surface_scaled, (0,0))

# Create surface to blit the game onto
game_surface = pygame.Surface((1920, 1080))

# Create largest possible surface with 16:9 aspect ratio
screen_resolution = [screen.get_width(), screen.get_height()]
smallest_side = screen_resolution.index(min(screen_resolution))

clock = pygame.time.Clock()

# Groups
background = pygame.sprite.GroupSingle()
background.add(Background())

arrow = pygame.sprite.GroupSingle()
arrow.add(Arrow())

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pygame.quit()
                exit()
            if event.key == pygame.K_a:
                direction = [1, 0, 0]
            if event.key == pygame.K_w:
                direction = [0, 1, 0]
            if event.key == pygame.K_d:
                direction = [0, 0, 1]
    
    background.draw(game_surface)
    background.update()

    arrow.draw(game_surface)
    arrow.update()


    fullscreen()
    pygame.display.update()
    dt = clock.tick(0) / 1000