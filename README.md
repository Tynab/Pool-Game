# POOL GAME
The Pool Game project is a Python-based endeavor utilizing libraries such as pygame and pymunk. This project aims to create a virtual representation of the classic game of pool, implementing realistic physics and interactive gameplay features for an engaging user experience.

## IMAGE DEMO
<p align='center'>
<img src='pic/0.jpg'></img>
</p>

## CODE DEMO
```python
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
```
