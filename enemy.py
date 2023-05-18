import pygame, sys
SCREEN_WIDTH = 1200
screen_height = 640
WINDOW_SIZE = (SCREEN_WIDTH, screen_height)  # set up window size
screen = pygame.display.set_mode(WINDOW_SIZE)  # initiate screen
import player
class Mushroom(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.mush = []
        self.mush.append(pygame.image.load('data/graphics/images/mushroom_0.png'))
        self.mush.append(pygame.image.load('data/graphics/images/mushroom_1.png'))
        self.mush.append(pygame.image.load('data/graphics/images/mushroom_2.png'))
        self.current_mush = 0
        self.image = self.mush[self.current_mush]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.flip = False
        self.move_direction = 1
        self.move_counter = 0

    def flip_flip(self, boolean):
        if self.flip != boolean:
            self.flip = boolean
    def update(self, scroll):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 30:
            self.move_direction *= -1
            self.move_counter *= -1
            if self.move_direction <= 0:
                self.flip_flip(True)
            if self.move_direction >= 0:
                self.flip_flip(False)
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        self.current_mush += 0.25
        if int(self.current_mush) >= len(self.mush):
            self.current_mush = 0
        self.image = self.mush[int(self.current_mush)]
        self.image = pygame.transform.flip(self.image, self.flip, False)

class Swordsman(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        #swordsman attacking animation
        self.attack_animation = False
        self.pause_running = False
        self.attacking = []
        self.attacking.append(pygame.image.load('data/graphics/swordsman/attack/swordsman.png'))
        self.attacking.append(pygame.image.load('data/graphics/swordsman/attack/swordman_swordup.png'))
        self.attacking.append(pygame.image.load('data/graphics/swordsman/attack/sword_swong_almost.png'))
        self.attacking.append(pygame.image.load('data/graphics/swordsman/attack/sword_swing.png'))
        self.attacking.append(pygame.image.load('data/graphics/swordsman/attack/sword_fully_swong.png'))
        self.current_frame = 0
        self.attack_image = self.attacking[self.current_frame]
        self.attack_rect = self.attack_image.get_rect()
        # swordsman running animation
        self.running_animation = True
        self.man = []
        self.man.append(pygame.image.load('data/graphics/swordsman/run/run_0.png'))
        self.man.append(pygame.image.load('data/graphics/swordsman/run/run_1.png'))
        self.man.append(pygame.image.load('data/graphics/swordsman/run/run_2.png'))
        self.man.append(pygame.image.load('data/graphics/swordsman/run/run_3.png'))
        self.man.append(pygame.image.load('data/graphics/swordsman/run/run_4.png'))
        self.man.append(pygame.image.load('data/graphics/swordsman/run/run_5.png'))
        self.man.append(pygame.image.load('data/graphics/swordsman/run/run_6.png'))
        self.current_sword = 0
        self.image = self.man[self.current_sword]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.flip = False
        self.move_direction = 1
        self.move_counter = 0
        self.health = 10


    def attacking_check(self):
        self.attack_animation = True
        print("attacking")

    def flip_flip(self, boolean):
        if self.flip != boolean:
            self.flip = boolean

    def update(self, scroll):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 30:
            self.move_direction *= -1
            self.move_counter *= -1
            if self.move_direction <= 0:
                self.flip_flip(False)
            if self.move_direction >= 0:
                self.flip_flip(True)
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        self.current_sword += 0.25
        if int(self.current_sword) >= len(self.man):
            self.current_sword = 0
        self.image = self.man[int(self.current_sword)]
        self.image = pygame.transform.flip(self.image, self.flip, False)
        self.current_frame += 0.25
    #attacking animation
        if int(self.current_frame) >= len(self.attacking):
            self.current_frame = 0
        self.attack_image = self.attacking[int(self.current_frame)]
        self.attack_image = pygame.transform.flip(self.attack_image, self.flip, False)

class Blob(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load('data/graphics/images/blob_img.png').convert_alpha()
        self.rect = self.img.get_rect()
        self.blob_group = pygame.sprite.Group()
        self.rect.x = x
        self.rect.y = y
        self.flip = False
