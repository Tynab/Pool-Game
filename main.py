import pygame
import pymunk
import pymunk.pygame_util
import math

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 678

# game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pool")

# pymunk space
space = pymunk.Space()
static_body = space.static_body
draw_options = pymunk.pygame_util.DrawOptions(screen)

# clock
clock = pygame.time.Clock()
FPS = 120

# game variables
dia = 36
force = 2000
taking_shot = True

# color
BG = (50, 50, 50)

# load images
cue_image = pygame.image.load("assets/images/cue.png").convert_alpha()
table_image = pygame.image.load("assets/images/table.png").convert_alpha()
ball_images = []

for i in range(1, 17):
    ball_image = pygame.image.load(f"assets/images/ball_{i}.png").convert_alpha()
    ball_images.append(ball_image)


# function for creating balls
def create_ball(radius, pos):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = 5
    shape.elasticity = 0.8
    # use pivot joint to add friction
    pivot = pymunk.PivotJoint(static_body, body, (0, 0), (0, 0))
    pivot.max_bias = 0  # disable joint correction
    pivot.max_force = 1000  # emulate linear friction
    space.add(body, shape, pivot)

    return shape


# setup game balls
balls = []
rows = 5

# potting balls
for col in range(5):
    for row in range(rows):
        pos = (250 + col * (dia + 1), 267 + row * (dia + 1) + col * dia / 2)
        new_ball = create_ball(dia / 2, pos)
        balls.append(new_ball)

    rows -= 1

# cue ball
pos = (888, SCREEN_HEIGHT / 2)
cue_ball = create_ball(dia / 2, pos)
balls.append(cue_ball)

# new_ball = create_ball(25, (300, 300))
# cue_ball = create_ball(25, (600, 310))

# create pool table cushions
cushions = [
    [(88, 56), (109, 77), (555, 77), (564, 56)],
    [(621, 56), (630, 77), (1081, 77), (1102, 56)],
    [(89, 621), (110, 600), (556, 600), (564, 621)],
    [(622, 621), (630, 600), (1081, 600), (1102, 621)],
    [(56, 96), (77, 117), (77, 560), (56, 581)],
    [(1143, 96), (1122, 117), (1122, 560), (1143, 581)],
]


# function for creating cushions
def create_cushion(poly_dims):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (0, 0)
    shape = pymunk.Poly(body, poly_dims)
    shape.elasticity = 0.8
    space.add(body, shape)


for cushion in cushions:
    create_cushion(cushion)


# create pool cue
class Cue:
    def __init__(self, pos):
        self.original_image = cue_image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self, angle):
        self.angle = angle

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(
            self.image,
            (
                self.rect.centerx - self.image.get_width() / 2,
                self.rect.centery - self.image.get_height() / 2,
            ),
        )


cue = Cue(balls[-1].body.position)

# game loop
run = True

while run:
    clock.tick(FPS)
    space.step(1 / FPS)

    # fill background
    screen.fill(BG)

    # draw pool table
    screen.blit(table_image, (0, 0))

    # draw pool balls
    for i, ball in enumerate(balls):
        screen.blit(
            ball_images[i],
            (ball.body.position[0] - ball.radius, ball.body.position[1] - ball.radius),
        )

    taking_shot = True

    # check if all the balls have stopped moving
    for ball in balls:
        taking_shot = (
            int(ball.body.velocity[0]) == 0 and int(ball.body.velocity[1]) == 0
        )

    # draw pool cue
    if taking_shot:
        # calculate pool cue angle
        mouse_pos = pygame.mouse.get_pos()
        cue.rect.center = balls[-1].body.position
        x_dist = balls[-1].body.position[0] - mouse_pos[0]
        y_dist = -(
            balls[-1].body.position[1] - mouse_pos[1]
        )  # -ve because pygame y coordinates increase down the screen
        cue_angle = math.degrees(math.atan2(y_dist, x_dist))
        cue.update(cue_angle)
        cue.draw(screen)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            x_impulse = math.cos(math.radians(cue_angle))
            y_impulse = math.sin(math.radians(cue_angle))
            balls[-1].body.apply_impulse_at_local_point(
                (force * -x_impulse, force * y_impulse), (0, 0)
            )

        run = event.type != pygame.QUIT

    # space.debug_draw(draw_options)
    pygame.display.update()

pygame.quit()
