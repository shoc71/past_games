import pygame

pygame.init()

# Constants
WHITE = (255,255,255) # having all caps as constants makes organzing variables so much easier
RED = (255,0,0)# rare instances of this changing, but easier to call and find from other variables
BLACK = (0,0,0)

WINDOW_SIZE = (1280,720)
WINDOW_TITLE = "Pygame Tutorial"

HORIZONTAL = 1
UP = 2
DOWN = 0

FRAME_RATE = 60
ANIMATION_FRAME_RATE = 10

WINDOW = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(WINDOW_TITLE)

CLOCK = pygame.time.Clock()

player_input = {"left": False, "right": False, "up": False, "down" : False}

background = pygame.transform.scale(pygame.image.load("assets/background.png"), WINDOW_SIZE)

objects = []# iterating all objects in this game loop

class Object:
    def __init__(self, x, y, width, height, image):
        self.x = x# the reason its in the init is because its going to be called differently later on
        self.y = y# the arguments are going to be used and called, all number/variable vaules go in there
        self.width = width
        self.height = height
        self.image = image
        self.velocity = [0, 0]# velocity is meant to handle x-direction and y-direction (no z-direction in 2D)

        objects.append(self)# whenever you create an object, it's going to add itself to the object list already

    def draw(self):# default image, then size, then position
        WINDOW.blit(pygame.transform.scale(self.image, (self.width, self.height)), (self.x, self.y))

    def update(self):
        self.x += self.velocity[0]# this makes speed and travel so much easier to do
        self.y += self.velocity[1]
        self.draw()# this will be called in the game loop

class Entity(Object):# devire a lot of things from the object class
    def __init__(self, x, y, width, height, tileset, speed):# overriding the constructor
        super().__init__(x, y, width, height, None)
        # last two to be used on player and enemies; over-riding all methods
        # calling the constructor from the object class
        self.speed = speed

        self.tileset = load_tileset(tileset, 16, 16)# entirely dependent on your tile image sizes

        self.direction = 0
        self.flipX = False
        self.frame = 0
        self.frames = [0,1,0,2] # litsed order of conducting animation sprites
        self.frame_timer = 0
        #most of the animation is gonna to be done here out of convience for enemies and other ojbects

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

    def draw(self):# overriding draw to draw our player
        image = pygame.transform.scale(self.tileset[self.frames[self.frame]][self.direction], (self.width, self.height))
            # the line above is dissecting as well the animation sequence and the tiles
        self.change_direction()

        image = pygame.transform.flip(image, self.flipX, False)# actaully flipping the drawn image
        WINDOW.blit(image, (self.x, self.y))

        if self.velocity[0] == 0 and self.velocity[1] == 0:
            self.frame = 0  
            return
        
        self.frame_timer += 1 # this is to prevent line t-3 above to stay at 0 at all times

        if self.frame_timer < ANIMATION_FRAME_RATE: 
            # waiting until the frametimer hits 10, its a good vaule; keeps growing timer
            return# framerate = 10
        
        self.frame += 1
        if self.frame >= len(self.frames):
            self.frame = 0# reseting our animation

        self.frame_timer = 0

    def update(self):
        self.x += self.velocity[0] * self.speed
        self.y += self.velocity[1] * self.speed
        self.draw()

class Player(Entity):
    def __init__(self, x, y, width, height, tileset, speed):
        super().__init__(x, y, width, height, tileset, speed)

def check_input(key, value):
    if key == pygame.K_w or key == pygame.K_UP:
        player_input["up"] = value
    elif key == pygame.K_s or key == pygame.K_DOWN:
        player_input["down"] = value
    elif key == pygame.K_a or key == pygame.K_LEFT:
        player_input["left"] = value
    elif key == pygame.K_d or key == pygame.K_RIGHT:
        player_input["right"] = value

def load_tileset(filename, width, height):# images in a tileset; multiple images in an image 
    image = pygame.image.load(filename).convert_alpha()# - the single image from that is called a tile
    image_width, image_height = image.get_size()
    tileset = []# chopping the individual tiles into their own images; 2-dimension list
    for tile_x in range(0, image_width // width):# range only works with whole numbers
        line = []# one dimension for all columns
        tileset.append(line)
        for tile_y in range(0, image_height // height):
            rect = (tile_x * width, tile_y * height, width, height)
            line.append(image.subsurface(rect))# subsurface is useful for calling bit-images (96x96)
    return tileset# makes calling this outside the function every easy

# Objects
# test_enetity = Entity(400,400,50,50,"assets/player-Sheet.png", 5)
player = Player(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2, 75, 75, "assets/player-Sheet.png", 5)

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
    
    player.velocity[0] = player_input["right"] - player_input["left"]
    player.velocity[1] = player_input["down"] - player_input["up"]

    WINDOW.blit(background, (0,0))

    for obj in objects:# iterating through each object
        obj.update()

    CLOCK.tick(FRAME_RATE)
    pygame.display.update()