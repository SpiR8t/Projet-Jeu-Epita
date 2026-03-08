import math
import pygame

class SpriteSheet:
    """
    Class pour la gestion des spritesheet pour les joueurs, ennemis et autres animations 'statiques' 
    c'est à dire ne se déplaçant pas.
    """
    def __init__(self, image_path):
        self.sheet = pygame.image.load(image_path).convert_alpha()

    def get_frame(self, x, y, width, height, scale=1):
        frame = pygame.Surface((width, height), pygame.SRCALPHA)
        frame.blit(self.sheet, (0, 0), (x, y, width, height))
        if scale != 1:
            frame = pygame.transform.scale(frame, (int(width * scale), int(height * scale)))
        return frame

    def get_animation(self, row, num_frames, frame_width, frame_height, scale=1):
        y = row * frame_height
        return [self.get_frame(i * frame_width, y, frame_width, frame_height, scale)
                for i in range(num_frames)]

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
