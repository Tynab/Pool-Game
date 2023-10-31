import pygame
import pymunk
import pymunk.pygame_util

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 678

# game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pool')

# pymunk space
space = pymunk.Space()
static_body = space.static_body
draw_options = pymunk.pygame_util.DrawOptions(screen)

# clock
clock = pygame.time.Clock()
FPS = 120

# color
BG = (50, 50, 50)

# load images
table_image = pygame.image.load('assets/images/table.png').convert_alpha()


def create_ball(radius, pos):  # function for creating balls
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = 5

    # use pivot joint to add friction
    pivot = pymunk.PivotJoint(static_body, body, (0, 0), (0, 0))
    pivot.max_bias = 0  # disable joint correction
    pivot.max_force = 1000  # emulate linear friction
    space.add(body, shape, pivot)

    return shape


new_ball = create_ball(25, (300, 300))
cue_ball = create_ball(25, (600, 310))

# create pool table cushions
cushions = [
    [(88, 56), (109, 77), (555, 77), (564, 56)]
]


def create_cushion(poly_dims):  # function for creating cushions
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = ((0, 0))
    shape = pymunk.Poly(body, poly_dims)
    space.add(body, shape)


# game loop
run = True

while run:
    clock.tick(FPS)
    space.step(1 / FPS)

    # fill background
    screen.fill(BG)

    # draw pool table
    screen.blit(table_image, (0, 0))

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            cue_ball.body.apply_impulse_at_local_point((-1500, 0), (0, 0))
        run = event.type != pygame.QUIT

    space.debug_draw(draw_options)
    pygame.display.update()

pygame.quit()
