import pygame
from sys import exit
from random import randint

pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption("Sorting PYne")
dt = 0
game_state = "title"
movement_speed = 200
last_score = 0
score = 0
high_score = 0
hard_high_score = 0
is_hard = False


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        background_1 = pygame.image.load("assets\\conveyor1.png").convert_alpha()
        background_2 = pygame.image.load("assets\\conveyor2.png").convert_alpha()
        background_3 = pygame.image.load("assets\\conveyor3.png").convert_alpha()
        background_4 = pygame.image.load("assets\\conveyor4.png").convert_alpha()
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
        elif direction[1] == 1:
            self.image = pygame.transform.rotate(self.image, 270)
            self.rect.topleft = (872, 272)
        elif direction[2] == 1:
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect.topleft = (856, 304)
    
    def update(self):
        self.animation_state()

class Box(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        # Color: Green = 1, Blue = 2, Yellow = 3
        self.box_color = color
        self.image = pygame.image.load("assets\\box{}.png".format(color))
        self.rect = self.image.get_rect(topleft = (880, 1240))
        self.sorted = False
        self.new_spawned = False
    
    def movement(self):
        # Movement before sorting and locking it in as sorted at right Y position
        if not self.sorted:
            self.rect.y -= movement_speed * dt
            if self.rect.y <= 288:
                self.rect.y = 296
                self.sorted = True
                self.sorted_direction = direction.index(1)
        # Movement after sorting
        else:
            if self.sorted_direction == 0:
                self.rect.x -= (movement_speed * 1.1) * dt
            elif self.sorted_direction == 1:
                self.rect.y -= movement_speed * dt
            elif self.sorted_direction == 2:
                self.rect.x += (movement_speed * 1.1) * dt
    
    def spawn_new(self):
        # Spawn new box after current box passes certain position
        if self.sorted:
            if not self.new_spawned:
                if self.sorted_direction == 0:
                    if self.rect.x <= 456:
                        pygame.event.post(box_event)
                        self.new_spawned = True
                elif self.sorted_direction == 1:
                    if self.rect.y <= 0:
                        pygame.event.post(box_event)
                        self.new_spawned = True
                elif self.sorted_direction == 2:
                    if self.rect.x >= 1416:
                        pygame.event.post(box_event)
                        self.new_spawned = True
    
    def despawn(self):
        global health
        if self.sorted:
            if self.sorted_direction == 0:
                if self.rect.x <= -160:
                    if self.box_color == 4:
                        health += 2
                        print(health)
                    if not self.box_color == 1:
                        health -= 1
                        print(health)
                    self.kill()
            elif self.sorted_direction == 1:
                if self.rect.y <= -160:
                    if self.box_color == 5:
                        health += 2
                        print(health)
                    if not self.box_color == 2:
                        health -= 1
                        print(health)
                    self.kill()
            elif self.sorted_direction == 2:
                if self.rect.x >= 2080:
                    if self.box_color == 6:
                        health += 2
                        print(health)
                    if not self.box_color == 3:
                        health -= 1
                        print(health)
                    self.kill()
        if health == 0: self.kill()
                
    def update(self):
        self.movement()
        self.spawn_new()
        self.despawn()



def fullscreen():
    if smallest_side == 1:
        game_surface_scaled = pygame.transform.scale(game_surface, (screen.get_height() * 1.77777777778, screen.get_height()))
    else:
        game_surface_scaled = pygame.transform.scale(game_surface(screen.get_width() / 1.77777777778, screen.get_width()))
    screen.blit(game_surface_scaled, (0,0))


def check_game_over():
    global health
    if health == 0: 
        global game_state
        game_state = "dead"
        global play_button_index
        play_button_index = 0
        global hard_button_index
        hard_button_index = 0
        global score
        return score
    else: return 0
        
        

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

# UI 
title_surf = pygame.image.load("assets\\title_screen.png").convert_alpha()
title_text_surf = pygame.image.load("assets\\title_text.png").convert_alpha()
title_text_timer = 50

heart1_surf = pygame.image.load("assets\\heart.png").convert_alpha()
heart2_surf = pygame.image.load("assets\\heart.png").convert_alpha()
heart1_rect = heart1_surf.get_rect(topright = (1888, 32))
heart2_rect = heart2_surf.get_rect(topright = (1760, 32))

menu_surf = pygame.image.load("assets\\main_menu.png").convert_alpha()

game_over_surf = pygame.image.load("assets\\game_over.png").convert_alpha()

pixel_font = pygame.font.Font("fonts\\pixeltype.ttf", 170)

score_text = pixel_font.render("Score: {}".format(score), False, (0,0,0))
score_text_rect = score_text.get_rect(topleft = ((32,32)))

# Menu buttons
play_button_1 = pygame.image.load("assets\\play_button1.png").convert_alpha()
play_button_2 = pygame.image.load("assets\\play_button2.png").convert_alpha()
play_button_frames = [play_button_1, play_button_2]
play_button_index = 0
play_button_rect = play_button_1.get_rect(topleft = (600, 800))

hard_button_1 = pygame.image.load("assets\\hard_button1.png").convert_alpha()
hard_button_2 = pygame.image.load("assets\\hard_button2.png").convert_alpha()
hard_button_frames = [hard_button_1, hard_button_2]
hard_button_index = 0
hard_button_rect = play_button_1.get_rect(topleft = (984, 800))

close_button = pygame.image.load("assets\\close_button.png").convert_alpha()
close_button_rect = close_button.get_rect(topleft = (1792, 72))

# Pause screen
pause_surf = pygame.image.load("assets\\pause_screen.png").convert_alpha()

continue_button_1 = pygame.image.load("assets\\pause_continue1.png").convert_alpha()
continue_button_2 = pygame.image.load("assets\\pause_continue2.png").convert_alpha()
continue_button_frames = [continue_button_1, continue_button_2]
continue_button_index = 0
continue_button_rect = continue_button_1.get_rect(topleft = (680, 496))

quit_button_1 = pygame.image.load("assets\\pause_quit1.png").convert_alpha()
quit_button_2 = pygame.image.load("assets\\pause_quit2.png").convert_alpha()
quit_button_frames = [quit_button_1, quit_button_2]
quit_button_index = 0
quit_button_rect = quit_button_1.get_rect(topleft = (680, 664))

# Events
box_event = pygame.event.Event(pygame.USEREVENT, attr1 = "box_event")

# Game loop
while True:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # Events during game
        if game_state == "game":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    continue_button_index = 0
                    quit_button_index = 0
                    game_state = "paused"
                if event.key in (pygame.K_a, pygame.K_LEFT) :
                    direction = [1, 0, 0]
                if event.key in (pygame.K_w, pygame.K_UP):
                    direction = [0, 1, 0]
                if event.key in (pygame.K_d, pygame.K_RIGHT):
                    direction = [0, 0, 1]

            # User events
            if event == box_event:
                if health == 2 or last_health == True:
                    last_health = False
                    box_group.add(Box(randint(1,3)))
                elif last_health  == False:
                    if randint(1, 10) == 1:
                        last_health = True
                        box_group.add(Box(randint(4,6)))
                    else:
                        box_group.add(Box(randint(1,3)))
                score += 1
                if movement_speed <= 1600:
                    movement_speed += 20
            

    
        # Events during title screen
        if game_state == "title":
            if event.type in (pygame.KEYUP, pygame.MOUSEBUTTONDOWN):
                game_state = "menu"
        
        # Events during menu screen
        if game_state == "menu":
            # Check play button press and start game
            pos = list(pygame.mouse.get_pos())
            # Take the mouse position and scale it, too
            ratio_x = (screen.get_width() / 1920)
            ratio_y = (screen.get_height() / 1080)
            scaled_pos = (pos[0] / ratio_x, pos[1] / ratio_y)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(scaled_pos):
                    play_button_index = 1
                if hard_button_rect.collidepoint(scaled_pos):
                    hard_button_index = 1
                if close_button_rect.collidepoint(scaled_pos):
                    pygame.quit()
                    quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if play_button_rect.collidepoint(scaled_pos):
                    game_state = "game"
                    is_hard = False
                    score = 0
                    health = 2
                    pygame.time.set_timer(box_event, 1000, 1)
                    movement_speed = 150
                    last_health = False
                    direction = [0, 1, 0]
                elif hard_button_rect.collidepoint(scaled_pos):
                    game_state = "game"
                    is_hard = True
                    score = 0
                    health = 2
                    pygame.time.set_timer(box_event, 1000, 1)
                    movement_speed = 1700
                    last_health = False
                    direction = [0, 1, 0]
                else:
                    play_button_index = 0
                    hard_button_index = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
        
        # Events during pause screen
        if game_state == "paused":
            # Check play button press and start game
            pos = list(pygame.mouse.get_pos())
            # Take the mouse position and scale it, too
            ratio_x = (screen.get_width() / 1920)
            ratio_y = (screen.get_height() / 1080)
            scaled_pos = (pos[0] / ratio_x, pos[1] / ratio_y)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button_rect.collidepoint(scaled_pos):
                    continue_button_index = 1
                if quit_button_rect.collidepoint(scaled_pos):
                    quit_button_index = 1
            elif event.type == pygame.MOUSEBUTTONUP:
                if continue_button_rect.collidepoint(scaled_pos):
                    game_state = "game"
                    if score == 0:
                        pygame.event.post(box_event)
                elif quit_button_rect.collidepoint(scaled_pos):
                    health = 0
                    box_group.update()
                    play_button_index = 0
                    hard_button_index = 0
                    game_state = "menu"
                else:
                    continue_button_index = 0
                    quit_button_index = 0


        # Events during game over screen
        if game_state == "dead":
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    game_state = "menu"
    
    if game_state == "game":
        # Draw and update classes during game
        background.draw(game_surface)
        background.update()

        arrow.draw(game_surface)
        arrow.update()

        box_group.draw(game_surface)
        box_group.update()

        # Blit UI elements
        game_surface.blit(heart1_surf, heart1_rect)
        if health == 2: game_surface.blit(heart2_surf, heart2_rect)

        score_text = pixel_font.render("Score:  {}".format(score), False, (0,0,0))
        game_surface.blit(score_text, score_text_rect)

        last_score = check_game_over()
        if is_hard: 
            if last_score > hard_high_score:
                hard_high_score = last_score
        elif last_score > high_score: high_score = last_score 

    
    # Display title screen
    elif game_state == "title":
        game_surface.blit(title_surf, (0, 0))
        if title_text_timer < 100:
            if title_text_timer > 50:
                game_surface.blit(title_text_surf, (480, 936))
            title_text_timer += (100 * dt)
        else:
            title_text_timer = 0
    
    # Display menu screen
    elif game_state == "menu":
        game_surface.blit(menu_surf, (0,0))
        game_surface.blit(play_button_frames[play_button_index], play_button_rect)
        game_surface.blit(hard_button_frames[hard_button_index], hard_button_rect)
        high_score_text = pixel_font.render("High score:  {}".format(str(high_score)), False, (0,0,0))
        hard_high_score_text = pixel_font.render("Hard score:  {}".format(str(hard_high_score)), False, (0,0,0))
        game_surface.blit(high_score_text, (936, 128))
        game_surface.blit(hard_high_score_text, (936, 272))
        game_surface.blit(close_button, close_button_rect)
        if not last_score == 0:
            last_score_text = pixel_font.render("You got  {}!".format(str(last_score)), False, (0,0,0))
            last_score_text_rect = last_score_text.get_rect(center = (960, 584))
            game_surface.blit(last_score_text, last_score_text_rect)

    # Display pause screen
    elif game_state == "paused":
        background.draw(game_surface)
        background.update()
        game_surface.blit(pause_surf, (0,0))
        game_surface.blit(continue_button_frames[continue_button_index], continue_button_rect)
        game_surface.blit(quit_button_frames[quit_button_index], quit_button_rect)

        game_surface.blit(heart1_surf, heart1_rect)
        if health == 2: game_surface.blit(heart2_surf, heart2_rect)

        score_text = pixel_font.render("Score:  {}".format(score), False, (0,0,0))
        game_surface.blit(score_text, score_text_rect)

    
    # Display game over screen
    elif game_state == "dead":
        game_surface.blit(game_over_surf, (0,0))


    fullscreen()
    pygame.display.update()
    dt = clock.tick(60) / 1000