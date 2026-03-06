import math
import pygame

class SimpleSlashAnimation:
    def __init__(self, x, y, direction, duration=8):
        self.x = x
        self.y = y
        self.direction = direction
        self.duration = duration
        self.timer = 0
        self.finished = False

    def update(self):
        self.timer += 1
        if self.timer >= self.duration:
            self.finished = True

    def draw(self, screen, camera):
        screen_x, screen_y = camera.apply(self.x, self.y)

        size = 40
        rect = pygame.Rect(
            screen_x - size//2,
            screen_y - size//2,
            size,
            size
        )

        dx, dy = self.direction

        # angles en radians
        if (dx, dy) == (0, -1):  # haut
            start_angle = math.radians(200)
            end_angle = math.radians(340)

        elif (dx, dy) == (0, 1):  # bas
            start_angle = math.radians(20)
            end_angle = math.radians(160)

        elif (dx, dy) == (-1, 0):  # gauche
            start_angle = math.radians(110)
            end_angle = math.radians(250)

        elif (dx, dy) == (1, 0):  # droite
            start_angle = math.radians(-70)
            end_angle = math.radians(70)

        else:
            start_angle = 0
            end_angle = math.pi

        pygame.draw.arc(screen, (255, 255, 255), rect, start_angle, end_angle, 4)
