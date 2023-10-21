from constal import *



class Windols:
    WIDTH = 1000
    HEIGHT = 600
    FPS = 60

    # Создаем игру и окно
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    pygame.display.set_caption("Game")

    gravity = 3.8  # м/(с ** 2)
    friction_force = 70  # H
    velocity_dino_initially = [2.5]
    velocity_dino = velocity_dino_initially[:]  # м/с
    acceleration_dino = 0.0005  # м/(с ** 2)

    stage = 0
    max_record = 0
    max_masiv = None

    list_cactus_person = []
    list_dino_person = []
    list_dino_person_dead = []

    def finish(self):
        for dino_person in self.list_dino_person_dead[:]:
            if self.max_record < dino_person.record:
                self.max_record = dino_person.record
                self.max_masiv = dino_person.masiv[:]

        for dino_person in self.list_dino_person_dead:
            dino_person.record = 0
            if dino_person.random_diffusions:
                dino_person.diffusions = [random.randint(-200_000, 200_000) / 200_000 for _ in range(8)]
            dino_person.education(self.max_masiv)

        self.list_dino_person = self.list_dino_person_dead[:]
        self.list_dino_person_dead = []

        for cactus_person in self.list_cactus_person[:][:-1]:
            self.list_cactus_person.remove(cactus_person)

        self.stage += 1
        self.velocity_dino[0] = self.velocity_dino_initially[0]
        print(self.stage, self.max_record, self.max_masiv)

    def collision(self):
        for dino_person in self.list_dino_person:
            for cactus_person in self.list_cactus_person:
                if (dino_person.cordinate[0] + dino_person.WIDTH_Dino >= cactus_person.cordinate[0] and
                        dino_person.cordinate[0] < cactus_person.cordinate[0] + cactus_person.WIDTH_Cactus):
                    if dino_person.cordinate[1] + dino_person.HEIGHT_Dino >= cactus_person.cordinate[1]:
                        self.list_dino_person.remove(dino_person)
                        self.list_dino_person_dead.append(dino_person)

    def rendering(self):
        # Обновление

        # Рендеринг
        self.screen.fill(BLACK)

        self.collision()

        for dino_person in self.list_dino_person:
            if self.list_cactus_person[0].cordinate[0] > dino_person.cordinate[0]:
                cactus = self.list_cactus_person[0]
            else:
                cactus = self.list_cactus_person[1]

            s = cactus.cordinate[0] - dino_person.cordinate[0]
            h = cactus.HEIGHT_Cactus
            u = self.velocity_dino[0]

            dino_person.frame(s, h, u)

        for cactus_person in self.list_cactus_person[:]:
            cactus_person.frame()

        if self.list_dino_person == []:
            self.finish()

        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()

        # Держим цикл на правильной скорости
        self.clock.tick(self.FPS)


class Dino_intelect(Windols):
    WIDTH_Dino = 20
    HEIGHT_Dino = 40

    force_max = 180  # H
    force = 0  # H
    mass = 20  # кг
    velocity = 0  # м/с
    record = 0
    random_diffusions = False

    def __init__(self, diffusions, masiv, RGP):
        # masiv and diffusions: [m0, m1, m2, m3, m4, m5, m6, m7]
        self.diffusions = diffusions
        self.education(masiv)

        self.cordinate = [20, self.HEIGHT - self.HEIGHT_Dino]
        self.RGP = RGP

        self.list_dino_person.append(self)

    def gravity_dino(self):
        if self.cordinate[1] < self.HEIGHT - self.HEIGHT_Dino or self.force == self.force_max:
            # F_r = F_т - F
            # F_r = a * m; F_т = m * g
            a = ((self.mass * self.gravity) - self.force) / self.mass

            if a > 0:
                a -= self.friction_force / self.mass

            self.velocity += a

            self.cordinate[1] += self.velocity
            self.force -= self.friction_force
            if self.force < 0:
                self.force = 0

        if self.cordinate[1] > self.HEIGHT - self.HEIGHT_Dino:
            self.cordinate[1] = self.HEIGHT - self.HEIGHT_Dino

    def movement(self):
        self.record -= 0.8
        if self.cordinate[1] >= self.HEIGHT - self.HEIGHT_Dino:
            self.force = self.force_max
            self.velocity = 0

    def education(self, masiv: list):  # обучение
        self.masiv = [masiv_neuro + self.diffusions[n_neuro] for n_neuro, masiv_neuro in enumerate(masiv)]

    def solution(self, s: int, h: int, u: int):  # решение
        # 0_1
        #        1_1
        # 0_2           2
        #        1_2
        # 0_3
        # TODO: не одоптимны
        neuro_1_1 = (s * self.masiv[0]) + (h * self.masiv[1]) + (u * self.masiv[2])
        neuro_1_2 = (s * self.masiv[3]) + (h * self.masiv[4]) + (u * self.masiv[5])

        neuro_2 = (neuro_1_1 * self.masiv[6]) + (neuro_1_2 * self.masiv[7])

        # if neuro_2 < 0.001:
        #     self.cordinate[1] = self.HEIGHT - self.HEIGHT_Dino
        if neuro_2 > 8:
            self.movement()
            return True
        return False

    def rendering_second(self):
        pygame.draw.rect(self.screen, self.RGP,
                         (self.cordinate[0], self.cordinate[1], self.WIDTH_Dino, self.HEIGHT_Dino))

    def frame(self, s, h, u):
        self.record += 1
        self.solution(s, h, u)
        self.gravity_dino()
        self.rendering_second()


class Cactus(Windols):
    Size_Cactus = [[20, 40], [30, 30], [35, 25], [30, 40]]
    RGP = (0, 255, 0)
    app_catus = False

    def __init__(self):
        self.WIDTH_Cactus, self.HEIGHT_Cactus = self.Size_Cactus[random.randint(0, len(self.Size_Cactus) - 1)]
        self.cordinate = [self.WIDTH, self.HEIGHT - self.HEIGHT_Cactus]

        self.list_cactus_person.append(self)
        self.cacti_difference = random.randint(200, 400)

    def movement(self):
        self.cordinate[0] -= self.velocity_dino[0]
        self.velocity_dino[0] += self.acceleration_dino

    def rendering(self):
        pygame.draw.rect(self.screen, self.RGP,
                         (self.cordinate[0], self.cordinate[1], self.WIDTH_Cactus, self.HEIGHT_Cactus))

    def frame(self):
        self.rendering()
        self.movement()

        # создание следушего катуса
        if self.cordinate[0] <= self.WIDTH - self.cacti_difference and not self.app_catus:
            self.app_catus = True
            Cactus()

        if self.cordinate[0] + self.WIDTH_Cactus <= 0 and self in self.list_cactus_person:
            self.list_cactus_person.remove(self)
