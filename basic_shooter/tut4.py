import pygame
import random

pygame.init()
pygame.font.get_init() # this is a thing appraently

TEXT_FONT = pygame.font.SysFont("arail", 52)

# Constants
WHITE = (255,255,255) # having all caps as constants makes organzing variables so much easier
RED = (255,0,0)# rare instances of this changing, but easier to call and find from other variables
BLACK = (0,0,0)

WINDOW_SIZE = (1280,720)
WINDOW_TITLE = "Pygame Tutorial"

HORIZONTAL = 1
UP = 2
DOWN = 0

BOUND_X = (66,1214)
BOUND_Y = (50,620)

FRAME_RATE = 60
ANIMATION_FRAME_RATE = 10

WINDOW = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(WINDOW_TITLE)

CLOCK = pygame.time.Clock()

score = 0

is_game_over = False
player_input = {"left": False, "right": False, "up": False, "down" : False}

background = pygame.transform.scale(pygame.image.load("assets/background.png"), WINDOW_SIZE)

objects = []
bullets = []
enemies = []
particles = []

class Object:
    def __init__(self, x, y, width, height, image):
        self.x = x# the reason its in the init is because its going to be called differently later on
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.velocity = [0, 0]
        self.collider = [width, height]

        objects.append(self)

    def draw(self):
        WINDOW.blit(pygame.transform.scale(self.image, (self.width, self.height)), (self.x, self.y))

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.draw()

    def get_center(self):
        return self.x + self.width / 2 , self.y + self.height / 2

class Entity(Object):# devire a lot of things from the object class
    def __init__(self, x, y, width, height, tileset, speed):# overriding the constructor
        super().__init__(x, y, width, height, None)
        self.speed = speed

        self.tileset = load_tileset(tileset, 16, 16)

        self.direction = 0
        self.flipX = False
        self.frame = 0
        self.frames = [0,1,0,2] # litsed order of conducting animation sprites
        self.frame_timer = 0

    def change_direction(self):
        if self.velocity[0] < 0: # going left
            self.direction = HORIZONTAL
            self.flipX = True
        elif self.velocity[0] > 0: # going right
            self.direction = HORIZONTAL
            self.flipX = False
        elif self.velocity[1] > 0:
            self.direction = DOWN
        elif self.velocity[1] < 0:
            self.direction = UP

    def draw(self):
        image = pygame.transform.scale(self.tileset[self.frames[self.frame]][self.direction], (self.width, self.height))
        self.change_direction()

        image = pygame.transform.flip(image, self.flipX, False)
        WINDOW.blit(image, (self.x, self.y))

        if self.velocity[0] == 0 and self.velocity[1] == 0:
            self.frame = 0  
            return
        
        self.frame_timer += 1

        if self.frame_timer < ANIMATION_FRAME_RATE: 
            return
        
        self.frame += 1
        if self.frame >= len(self.frames):
            self.frame = 0

        self.frame_timer = 0

    def update(self):
        self.x += self.velocity[0] * self.speed
        self.y += self.velocity[1] * self.speed
        self.draw()

class Player(Entity):
    def __init__(self, x, y, width, height, tileset, speed):
        super().__init__(x, y, width, height, tileset, speed)
        self.health = self.max_length = 3 # double assignment 

    def update(self):
        super().update()

        self.x = max(BOUND_X[0], min(self.x, BOUND_X[1] - self.width))
        self.y = max(BOUND_Y[0], min(self.y, BOUND_Y[1] - self.height))

class Enemy(Entity):
    def __init__(self, x, y, width, height, tileset, speed):
        super().__init__(x, y, width, height, tileset, speed)
        self.max_width = width
        self.max_height = height
        self.width = 0 # why are we doing this?
        self.height = 0 # creating a spwaning enemy like growing from 0 to its normal width

        self.health = 3
        self.collider = [width / 2.5, height / 1.5] # eliminating hitting the tiles which dont exist 
        enemies.append(self)

        self.start_timer = 0

    def cooldown(self):
        if self.start_timer < 1:
            self.start_timer += 0.03
            self.x -= 1
            self.y -= 1# this is a tosic way of solving your problems
        self.width = int(self.max_width * self.start_timer)
        self.height = int(self.max_height * self.start_timer)

    def update(self):
        player_center = player.get_center()
        enemy_center = self.get_center()

        self.velocity = [player_center[0] - enemy_center[0], player_center[1] - enemy_center[1]]

        magnitude = (self.velocity[0] ** 2 + self.velocity[1] ** 2) ** 0.5
        self.velocity = [self.velocity[0] / magnitude * self.speed, self.velocity[1] / magnitude * self.speed]

        self.cooldown()
        if self.start_timer < 1:
            self.velocity = [0, 0]

        super().update()# call teh update method of teh entity calss

    def change_direction(self):
        super().change_direction()

        if self.velocity[1] > self.velocity[0] > 0:
            self.direction = DOWN
        elif self.velocity[1] < self.velocity[0] < 0:
            self.direction = UP

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            global score
            score += 1
            self.destroy()

    def destroy(self):
        objects.remove(self)
        enemies.remove(self)

def check_input(key, value):
    if key == pygame.K_w or key == pygame.K_UP:
        player_input["up"] = value
    elif key == pygame.K_s or key == pygame.K_DOWN:
        player_input["down"] = value
    elif key == pygame.K_a or key == pygame.K_LEFT:
        player_input["left"] = value
    elif key == pygame.K_d or key == pygame.K_RIGHT:
        player_input["right"] = value

def load_tileset(filename, width, height):
    image = pygame.image.load(filename).convert_alpha()
    image_width, image_height = image.get_size()
    tileset = []
    for tile_x in range(0, image_width // width):
        line = []
        tileset.append(line)
        for tile_y in range(0, image_height // height):
            rect = (tile_x * width, tile_y * height, width, height)
            line.append(image.subsurface(rect))
    return tileset

def enemy_spawner():# this is made with the intention to go on forever
    while True:
        for i in range(60):
            yield #tunrs function into an enumerator - counts every time the looop goes and uses the function
            # used here to exit the loop and when called back a secnod time, it starts here
        randomX = random.randint(BOUND_X[0], BOUND_Y[1] - 75)# 75 is the size of the enemy to prevent them from
        randomY = random.randint(BOUND_Y[0], BOUND_Y[1] - 75)# - spwaning outside the bounds
        enemy = Enemy(randomX, randomY, 75, 75, "assets/enemy-Sheet.png", 2)

        #preventing enemy spawn on top of player
        player_center = player.get_center()
        if abs(player_center[0] - enemy.x) < 250 and abs(player_center[1] - enemy.y) < 250:
            enemy.x = random.randint(BOUND_X[0], BOUND_X[1] - 75)
            enemy.y = random.randint(BOUND_Y[0], BOUND_Y[1] - 75)


def spawn_particles(x, y,):
    particle = Object(x, y, 75, 75, pygame.image.load("assets/particles.png"))

# Objects
player = Player(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2, 75, 75, "assets/player-Sheet.png", 5)
target = Object(0, 0, 50, 50, pygame.image.load("assets/cursor.png"))
spawner = enemy_spawner()

pygame.mouse.set_visible(False)

def shoot():
    player_center = player.get_center()
    bullet = Object(player_center[0], player_center[1], 16, 16, pygame.image.load("assets/bullet.png"))

    target_center = target.get_center()
    bullet.velocity = [target_center[0] - player_center[0], target_center[1] - player_center[1]]

    magnitude = (bullet.velocity[0] ** 2 + bullet.velocity[1] ** 2) ** 0.5

    bullet.velocity = [bullet.velocity[0] / magnitude * 10, bullet.velocity[1] / magnitude * 10] # * 10 for speed

    bullets.append(bullet)

def check_collisions(obj1, obj2):
    x1, y1 = obj1.get_center()
    x2, y2 = obj2.get_center()
    w1, h1 = obj1.collider[0] / 2, obj1.collider[1] / 2
    w2, h2 = obj2.collider[0] / 2, obj2.collider[1] / 2
    if x1 + w1 > x2 - w2 and x1 - w1 < x2 + w2:
        return y1 + h1 > y2 - h2 and y1 - h1 < y2 + h2
    return False

def display_ui():
    for i in range(player.max_length):
        img = pygame.image.load("assets/heart_empty.png" if i >= player.health else "assets/heart.png")
        img = pygame.transform.scale(img, (50,50))
        WINDOW.blit(img, (i * 50 + WINDOW_SIZE[0] / 2 - player.max_length * 25, 25))

    score_text = TEXT_FONT.render(f"Score : {score}", True, BLACK)
    # used for anti-aliasing - soothing out jagged edges by blending in adjacent colors with same color
    # simple explaination; - used to imporve graphics 
    WINDOW.blit(score_text, (score_text.get_width() / 2, 25))

    if is_game_over:
        game_over_1 = pygame.font.SysFont("arail",108)
        game_over_text = game_over_1.render("Game Over!", True, BLACK)
        WINDOW.blit(game_over_text, (WINDOW_SIZE[0] / 2 - game_over_text.get_width() / 2,
                                     WINDOW_SIZE[1] / 2 - game_over_text.get_height() / 2))

def update_screen():
    CLOCK.tick(FRAME_RATE)
    pygame.display.update()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            check_input(event.key, True)
            if event.key == pygame.K_ESCAPE:
                exit()
        elif event.type == pygame.KEYUP:
            check_input(event.key, False)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            shoot()
    
    mousePos = pygame.mouse.get_pos()
    target.x = mousePos[0] - target.width / 2
    target.y = mousePos[1] - target.height / 2

    player.velocity[0] = player_input["right"] - player_input["left"]
    player.velocity[1] = player_input["down"] - player_input["up"]

    WINDOW.blit(background, (0,0))

    display_ui()

    if is_game_over: # game over screen
        pygame.mouse.set_visible(True)
        update_screen()
        continue

    next(spawner)# this will iterate through the enemerator

    if player.health <= 0:
        if not is_game_over:
            is_game_over = True

    objects.remove(target)
    objects.sort(key=lambda o: o.y) # key argu with lambda - each element of obj list; comparing all y-obj's
    objects.append(target)

    for obj in objects:# iterating through each object
        obj.update()

    for b in bullets:
        if BOUND_X[0] <= b.x <= BOUND_X[1] and BOUND_Y[0] <= b.y <= BOUND_Y[1]:
            continue
        bullets.remove(b)
        objects.remove(b)

    for e in enemies:
        if check_collisions(player, e):
            player.health -= 1
            e.destroy()
            continue
        for b in bullets:
            if check_collisions(b, e):
                e.take_damage(1)
                # score += 1
                bullets.remove(b)
                objects.remove(b)

    update_screen()