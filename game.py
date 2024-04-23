import pygame
from sys import exit
from random import randint

pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
dt = 0
game_state = "title"
movement_speed = 500  

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
            self.rect.topleft = (856, 304)
        if direction[1] == 1:
            self.image = pygame.transform.rotate(self.image, 270)
            self.rect.topleft = (872, 280)
        if direction[2] == 1:
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect.topleft = (856, 304)
    
    def update(self):
        self.animation_state()

class Box(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        # Color: Green = 1, Blue = 2, Yellow = 3
        global box_color
        box_color = color
        self.image = pygame.image.load("assets\\box{}.png".format(color))
        self.rect = self.image.get_rect(bottomleft = (880, 1080))
        self.sorted = False
    
    def movement(self):
        self.rect.y -= movement_speed * dt
        if not self.sorted:
            if direction == [1, 0, 0]:
                if self.rect.y <= 290:
                    self.rect.y = 290
                    self.sorted = True
                    
    
    def update(self):
        self.movement()


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

box_group = pygame.sprite.Group()

# Title screen 
title_surf = pygame.image.load("assets\\title_screen.png").convert_alpha()
title_text_surf = pygame.image.load("assets\\title_text.png").convert_alpha()
text_timer = 0

# Event timers
box_event = pygame.event.Event(pygame.USEREVENT, attr1 = "box_event")

# Game loop
while True:
    # Event loop
    for event in pygame.event.get():
        # Events during game
        if game_state == "game":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.quit()
                    exit()
                if event.key in (pygame.K_a, pygame.K_LEFT) :
                    direction = [1, 0, 0]
                if event.key in (pygame.K_w, pygame.K_UP):
                    direction = [0, 1, 0]
                if event.key in (pygame.K_d, pygame.K_RIGHT):
                    direction = [0, 0, 1]
            
            if event == box_event:
                box_group.add(Box(randint(1,3)))
        
        
        # Events during title screen
        if game_state == "title":
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                game_state = "game"
                pygame.event.post(box_event)
    
    # Draw and update classes during game
    if game_state == "game":
        background.draw(game_surface)
        background.update()

        arrow.draw(game_surface)
        arrow.update()

        box_group.draw(game_surface)
        box_group.update()

    
    # Display title screen
    elif game_state == "title":
        game_surface.blit(title_surf, (0, 0))
        if text_timer < 100:
            if text_timer > 50:
                game_surface.blit(title_text_surf, (480, 936))
            text_timer += (100 * dt)
        else:
            text_timer = 0



    fullscreen()
    pygame.display.update()
    dt = clock.tick(0) / 1000