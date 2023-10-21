from utils import *


print('Start')
windols = Windols()

def Start():
    Cactus()
    masiv = [0 for _ in range(8)]

    for _ in range(50):
        diffusions = [random.randint(0, 200_000) / 100_000 for _ in range(8)]
        RGP = (255, 255, 255)
        dino_1 = Dino_intelect(diffusions, masiv, RGP)
        dino_1.random_diffusions = True

    diffusions = [1.00001, -1.00001, 1.00001, 1.00001, 0.00001, 1.00001, -0.00001, 1.00001]
    RGP = (255, 0, 0)
    Dino_intelect(diffusions, masiv, RGP)

    diffusions = [-0.001, 0.001, 0.001, -0.001, 0.001, -0.001, 0.001, -0.001]
    RGP = (0, 0, 255)
    Dino_intelect(diffusions, masiv, RGP)

    diffusions = [1.01, 0.0000001, 0.001, 04.1, 0.09501, 1.001, -0.0901, -0.19]
    RGP = (160, 160, 160)
    Dino_intelect(diffusions, masiv, RGP)

    diffusions = [0.3542001, -0.001, 0.6782306601, 6.0061, 6.001, 0.001, -06.001, 0.0601]
    RGP = (160, 160, 0)
    Dino_intelect(diffusions, masiv, RGP)

    diffusions = [-3.001, -03.001, 0.4001, -0.001, 0.0301, 3, 0.001, 0.8001]
    RGP = (160, 0, 160)
    Dino_intelect(diffusions, masiv, RGP)

    diffusions = [-4.001, 8.001, 1.06601, -0.0061, 6.001, -2.001, -1.001, -0.0601]
    RGP = (0, 160, 160)
    Dino_intelect(diffusions, masiv, RGP)

    diffusions = [-3.9787, -3.75783, 0.4001, -0.7, 0.894755, 0.00001, 0.001, 0.25456]
    RGP = (160, 0, 110)
    Dino_intelect(diffusions, masiv, RGP)

    diffusions = [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001]
    RGP = (0, 0, 110)
    Dino_intelect(diffusions, masiv, RGP)

    diffusions = [-0.0001, -0.0001, -0.0001, -0.0001, -0.0001, -0.0001, -0.0001, -0.0001]
    RGP = (7, 174, 110)
    Dino_intelect(diffusions, masiv, RGP)

    diffusions = [0.12001, 0.3254001, 0.06601, 0.2340061, 0.001, 0.001, 0.2354001, 0.0601]
    RGP = (7, 100, 20)
    Dino_intelect(diffusions, masiv, RGP)


Start()

# Цикл игры

while True:
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            pygame.quit()

    windols.rendering()

