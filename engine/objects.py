import pygame
import random
import logging
from model.AI import ModelDino
import engine.config_physics as config_physics

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Dino(ModelDino):
    character_img = pygame.image.load("assets/images_1.png")
    size_dino_up = config_physics.size_dino_up
    size_dino_down = config_physics.size_dino_down

    force_jamb= config_physics.force_jamb  # H
    mass = config_physics.mass  # кг

    def __init__(self, size_window: list, default_cardinal: list=[10, 0]):
        super().__init__()
        self.size_window = size_window

        self.velocity = 0 # м/с
        self.force = 0  # H
        self.score = 0
        self.live = True

        self.size_dino = self.size_dino_up
        self.coordinate = [default_cardinal[0], size_window[1] - self.size_dino[1]]

    def get_coordinate(self):
        xy_up_left = (self.coordinate[0], self.coordinate[1])
        xy_up_right = (self.coordinate[0] + self.size_dino[0], self.coordinate[1])
        xy_down_left = (self.coordinate[0], self.coordinate[1] + self.size_dino[1])
        xy_down_right = (self.coordinate[0] + self.size_dino[0], self.coordinate[1] + self.size_dino[1])

        return xy_up_left, xy_up_right, xy_down_left, xy_down_right

    def jamb_up(self):
        if self.coordinate[1] == self.size_window[1] - self.size_dino[1]:
            self.velocity += self.force_jamb / self.mass
        self.score -= 0.3

    def jamb_down(self):
        self.velocity -= self.force_jamb / self.mass
        self.size_dino = self.size_dino_down
        self.score -= 0.3

    def gravity_dino(self):
        # F_r = F_т - F
        # F_r = a * m; F_т = m * g

        self.velocity -= config_physics.gravity
        self.coordinate[1] -= self.velocity

        if self.coordinate[1] > self.size_window[1] - self.size_dino[1]:
            self.velocity = 0
            self.coordinate[1] = self.size_window[1] - self.size_dino[1]

    def movement(self):
        if self.coordinate[1] >= self.HEIGHT - self.HEIGHT_Dino:
            self.force = self.force_max
            self.velocity = 0

    def education(self):  # обучение
        self.study(self.score)

    def solution(self, s: int, h: int, u: int):  # решение
        rec = self.rec_model([s, h, u])
        if rec[0] < 1:
            return True
        return False

    def rendering(self, screen):
        character_img = pygame.transform.scale(self.character_img, self.size_dino)
        screen.blit(character_img,
                    (self.coordinate[0], self.coordinate[1], self.size_dino[0], self.size_dino[1]))

    def frame(self, screen, s: int, h: int, u: int):
        self.size_dino = self.size_dino_up
        if self.solution(s, h, u):
            self.jamb_up()

        self.score += 0.1
        self.gravity_dino()
        self.rendering(screen)

    def kill(self):
        self.live = False

    def revival(self):
        self.score = 0
        self.live = True


class Cactus:
    size_cactus = config_physics.size_cactus
    cactus_color = config_physics.cactus_color
    add_cactus = False
    del_cactus = False

    def __init__(self, size_window):
        self.size_window = size_window

        self.cactus_size = self.size_cactus[random.randint(0, len(self.size_cactus) - 1)]

        self.coordinate = [size_window[0], size_window[1] - self.cactus_size[1]]
        self.cacti_difference = random.randint(200, 400)

    def get_coordinate(self):
        xy_up_left = (self.coordinate[0], self.coordinate[1])
        xy_up_right = (self.coordinate[0] + self.cactus_size[0], self.coordinate[1])
        xy_down_left = (self.coordinate[0], self.coordinate[1] + self.cactus_size[1])
        xy_down_right = (self.coordinate[0] + self.cactus_size[0], self.coordinate[1] + self.cactus_size[1])

        return xy_up_left, xy_up_right, xy_down_left, xy_down_right

    def movement(self, velocity):
        self.coordinate[0] -= velocity

    def rendering(self, screen):
        pygame.draw.rect(screen, self.cactus_color,
                         (self.coordinate[0], self.coordinate[1], self.cactus_size[0], self.cactus_size[1]))

    def frame(self, screen, velocity):
        self.movement(velocity)

        if self.coordinate[0] <= self.size_window[0] - self.cacti_difference and self.add_cactus is not None:
            self.add_cactus = True
        if self.coordinate[0] + self.cactus_size[0] <= 0:
            self.del_cactus = True

        self.rendering(screen)


class Window:
    background_color = (242, 242, 242)
    text_color = (0, 0, 0)

    def __init__(self, name="Game", w=1000, h=600):
        self.velocity = config_physics.velocity
        self.size_window = [w, h]
        self.num_generation = 1

        self.list_dino_person = []

        self.list_cactus_person = []

        self.screen = pygame.display.set_mode(self.size_window)
        pygame.display.set_caption(name)


    def start(self, num_dino=1):
        for _ in range(num_dino):
            self.add_dino()
        self.add_cactus()

    def add_dino(self):
        dino = Dino(self.size_window)
        self.list_dino_person.append(dino)

    def add_cactus(self):
        cactus = Cactus(self.size_window)
        self.list_cactus_person.append(cactus)

    def del_cactus(self, cactus):
        self.list_cactus_person.remove(cactus)

    def finish(self):
        self.num_generation += 1
        self.velocity = config_physics.velocity
        max_record = 0

        for dino_person in self.list_dino_person:
            max_record = max(max_record, dino_person.score)
            dino_person.education()
            dino_person.revival()

        for cactus_person in self.list_cactus_person[:]:
            self.del_cactus(cactus_person)
        self.add_cactus()

        logging.info(f"Finish: {max_record}")

    def collision(self):
        cactus_xy_up_left, cactus_xy_up_right, _, _ = self.list_cactus_person[0].get_coordinate()

        for dino_person in self.list_dino_person:
            _, _, dino_xy_down_left, dino_xy_down_right = dino_person.get_coordinate()
            if ((cactus_xy_up_left[0] <= dino_xy_down_left[0] <= cactus_xy_up_right[0] or
                cactus_xy_up_left[0] <= dino_xy_down_right[0] <= cactus_xy_up_right[0]) and
                dino_xy_down_left[1] >= cactus_xy_up_left[1]):
                dino_person.kill()

    def rendering_text(self):
        font = pygame.font.Font(None, 30)

        text_surface = font.render(f"Velocity: {self.velocity}", True, self.text_color)
        self.screen.blit(text_surface, (10, 20))

        text_v = font.render(f"Generation: {self.num_generation}", True, self.text_color)
        self.screen.blit(text_v, (10, 50))

    def rendering(self):
        self.velocity += config_physics.acceleration

        # Рендеринг
        self.screen.fill(self.background_color)

        num_live_dino = 0

        for dino_person in self.list_dino_person:
            if dino_person.live:
                if self.list_cactus_person[0].coordinate[0] > dino_person.coordinate[0]: cactus = self.list_cactus_person[0]
                else: cactus = self.list_cactus_person[1]

                s = cactus.coordinate[0] - dino_person.coordinate[0]
                h = cactus.cactus_size[1]
                u = self.velocity

                num_live_dino += 1
                dino_person.frame(self.screen, s, h, u)

        for cactus_person in self.list_cactus_person[:]:
            cactus_person.frame(self.screen, self.velocity)

            if cactus_person.add_cactus:
                self.add_cactus()
                cactus_person.add_cactus = None
            elif cactus_person.del_cactus:
                self.del_cactus(cactus_person)

        self.collision()
        self.rendering_text()

        if not num_live_dino:
            self.finish()

        pygame.display.flip()
