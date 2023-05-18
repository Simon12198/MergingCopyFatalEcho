import time
from player import *
from csv_loader import *
import enemy

tile_size = 32

SCREEN_WIDTH = 1200
screen_height = 640

rescaled_width = 600
rescaled_height = 320
cooldown_tracker = 0


class Tiles(pygame.sprite.Sprite):
    def __init__(self, size, loc):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=loc)

    def update(self, scroll):
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]


class ground_tile(Tiles):
    def __init__(self, size, loc, img):
        super().__init__(size, loc)
        self.image = img
        self.mask = pygame.mask.from_surface(img)


class Level:


    def __init__(self, game_map, path, surface):
        self.game_map = game_map
        self.surface = surface
        self.game_map = self.load_map(path)
        self.bg_drawn = False
        self.player_direction = 0
        self.merchant_beside = 0
        self.mushroom_inv = 0
        self.damage = 10
        self.dead = False
        self.health = 20
        self.max_health = 20
        self.damage_taken = False
        # heart images
        self.full_heart = pygame.image.load('data/graphics/bg_images/heart.png').convert_alpha()
        self.half_heart = pygame.image.load('data/graphics/bg_images/half_heart.png').convert_alpha()
        self.empty_heart = pygame.image.load('data/graphics/bg_images/empty_heart.png').convert_alpha()

        self.player = pygame.sprite.GroupSingle()
        self.tiles = pygame.sprite.Group()
        self.bg_objects = pygame.sprite.Group()
        self.heart_objects = pygame.sprite.Group()
        self.coin = pygame.sprite.Group()
        self.Death = pygame.sprite.Group()
        self.tree = pygame.sprite.Group()
        self.mushroom_group = pygame.sprite.Group()
        self.blob_group = pygame.sprite.Group()
        self.slopesgroup = pygame.sprite.Group()
        self.topslopesgroup = pygame.sprite.Group()
        self.swordsman_group = pygame.sprite.Group()
        self.merchant_group = pygame.sprite.Group()
        self.Spawn = pygame.sprite.GroupSingle()
        self.End = pygame.sprite.Group()
        # use to calculate score
        self.score = 10000
        self.coin_count = 0
        self.start_time = time.time()
        self.player_on_slope = False
        self.bg_imgs = []
        #background images added to list
        for i in range(1, 6):
            bg_img = pygame.image.load('data/graphics/bg_images/' + f'forest-{i}.png').convert_alpha()
            self.bg_imgs.append(bg_img)
        #creating and importing the game map files and sprites
        self.terrain_layout = import_csv_files(self.game_map['Grass'])
        self.terrain_sprites = self.create_sprite(self.terrain_layout, 'Grass')

        self.Gold = import_csv_files(self.game_map['Gold'])
        self.create_sprite(self.Gold, 'Gold')
        self.Mushroom = import_csv_files(self.game_map['Mushroom'])
        self.create_sprite(self.Mushroom, 'Mushroom')
        self.Swordsman = import_csv_files(self.game_map['Swordsman'])
        self.create_sprite(self.Swordsman, 'Swordsman')
        self.Blob = import_csv_files(self.game_map['Blobs'])
        self.create_sprite(self.Blob, 'Blobs')
        self.merchantslayout = import_csv_files(self.game_map['Merchant'])
        self.create_sprite(self.merchantslayout, 'Merchant')

        self.tree_layout = import_csv_files(self.game_map['Trees'])
        self.create_sprite(self.tree_layout, 'Trees')

        self.slope_layout = import_csv_files(self.game_map['Slopes'])
        self.slope_sprites = self.create_sprite(self.slope_layout, 'Slopes')

        self.topslope_layout = import_csv_files(self.game_map['TopSlopes'])
        self.topslope_sprites = self.create_sprite(self.topslope_layout, 'TopSlopes')

        self.spawn = import_csv_files(self.game_map['Spawn'])
        self.create_sprite(self.spawn, 'Spawn')

        self.death = import_csv_files(self.game_map['Death'])
        self.create_sprite(self.death, 'Death')


    def armour_trade(self):
        self.health += 1
        self.mushroom_inv -= 8
    def weapons_trade(self, amount):
        self.damage += 2
        self.mushroom_inv -= 10

    def load_map(self, path):
        level_data = {}
        f = open(path + 'level', 'r')
        self.level = f.read()
        f.close()
        self.level = self.level.split('\n')
        for name in self.level:
            paths = path.split('/')
            level_name = paths[2]
            level_data[name] = path + level_name + '_' + name + '.csv'
        return (level_data)

    def create_sprite(self, layout, type):

        row_index = 0
        for row in layout:
            col_index = 0
            for col in row:
                if col != '-1':
                    if type == 'Grass':
                        terrain_layout = slicing_tiles('data/graphics/Terrain/Grass/Grass.png')
                        tile = terrain_layout[int(col)]
                        sprite = ground_tile(tile_size, [col_index * 32, row_index * 32], tile)
                        self.tiles.add(sprite)
                    if type == 'Gold':
                        gold = slicing_tiles('data/graphics/Terrain/Coin/gold_coin.png')
                        tiles = gold[int(col)]
                        sprite = ground_tile(tile_size, [col_index * 32, row_index * 32], tiles)
                        self.coin.add(sprite)
                    if type == 'Death':
                        death = slicing_tiles('data/graphics/Terrain/Death/Death.png')
                        tileset = death[int(col)]
                        sprite = ground_tile(tile_size, [col_index * 32, row_index * 32], tileset)
                        self.Death.add(sprite)
                    if type == 'Trees':
                        tree_layout = slicing_tiles('data/graphics/Terrain/Tree/Tree_tileset.png')
                        tiled = tree_layout[int(col)]
                        sprite = ground_tile(tile_size, [col_index * 32, row_index * 32], tiled)
                        self.tree.add(sprite)
                    if type == 'Merchant':
                        tree_layout = slicing_tiles('data/graphics/images/merchant.png')
                        tiled = tree_layout[int(col)]
                        sprite = ground_tile(tile_size, [col_index * 32, row_index * 32], tiled)
                        self.merchant_group.add(sprite)
                    if type == 'Mushroom':
                        mush_layout = slicing_tiles('data/graphics/images/mushroom_0.png', (16, 16))
                        tiled = mush_layout[int(col)]
                        sprite = ground_tile(tile_size, [col_index * 32, row_index * 32], tiled)
                        mushroom = enemy.Mushroom(col_index * 32, row_index * 32 + 18)
                        self.mushroom_group.add(mushroom)
                    if type == 'Swordsman':
                        enemy_layout = slicing_tiles('data/graphics/images/swordsman.png')
                        tiled = enemy_layout[int(col)]
                        sprite = ground_tile(tile_size, [col_index * 32, row_index * 32], tiled)
                        swordsman = enemy.Swordsman(col_index * 32, row_index * 32)
                        self.swordsman_group.add(swordsman)
                    if type == 'Blobs':
                        blob_layout = slicing_tiles('data/graphics/images/blob_img.png', (97, 30))
                        tiled = blob_layout[int(col)]
                        sprite = ground_tile(tile_size, [col_index * 32, row_index * 32], tiled)
                        blob = enemy.Blob(col_index * 32, row_index * 32 + 15)
                        self.blob_group.add(sprite)
                    if type == 'Slopes':
                        slope_layout = slicing_tiles('data/graphics/Terrain/Slopes/Slopes.png')
                        ramps = slope_layout[int(col)]
                        sprite = ground_tile(tile_size, [col_index * 32, row_index * 32], ramps)
                        self.slopesgroup.add(sprite)
                    if type == 'TopSlopes':
                        slope_layout = slicing_tiles('data/graphics/Terrain/Slopes/Slopes.png')
                        topramp = slope_layout[int(col)]
                        sprite = ground_tile(tile_size, [col_index * 32, row_index * 32], topramp)
                        self.topslopesgroup.add(sprite)
                    if type == 'Spawn':
                        life = slicing_tiles('data/graphics/Terrain/Spawn/Spawn.png')
                        born_set = life[int(col)]
                        if col == '0':
                            sprite = ground_tile(tile_size, [col_index * 32, row_index * 32], born_set)
                            if not self.dead:
                                self.Spawn.add(sprite)
                            self.dead = True
                            player = Player([col_index * 32, row_index * 32])
                            self.player.add(player)
                            self.dead = False
                        if col == '1':
                            sprite = ground_tile(tile_size, [col_index * 32, row_index * 32], born_set)
                            self.End.add(sprite)
                col_index += 1
            row_index += 1
        self.tile_sprites = self.tiles.sprites()
        self.slope_sprite = self.slopesgroup.sprites()
        self.topslope_sprites = self.topslopesgroup.sprites()

    def scrolling(self):
        spawn = self.Spawn.sprite
        player = self.player.sprite
        true_scroll = [0, 0]
        if self.dead == False:
            true_scroll[0] += (player.rect.x-true_scroll[0] - rescaled_width // 2) // 15
            true_scroll[1] += (player.rect.y-true_scroll[1] - rescaled_height // 2) // 15
            self.scroll = true_scroll.copy()
            self.scroll[0] = int(self.scroll[0])
            self.scroll[1] = int(self.scroll[1])
        else:
            true_scroll[0] += (spawn.rect.x-true_scroll[0] - rescaled_width // 3.12)
            true_scroll[1] += (spawn.rect.y-true_scroll[1] - rescaled_height * 1.173)
            self.scroll = true_scroll.copy()
            self.scroll[0] = int(self.scroll[0])
            self.scroll[1] = int(self.scroll[1])
    def collision_movement(self):
        if self.dead == False:
            player = self.player.sprite
            player.x = player.rect.x
            player.x += player.movement[0]
            player.rect.x = int(player.x)

            self.collision_types = {'top': False, 'bottom': False, 'left': False, 'right': False}
            for tile in self.tiles.sprites():
                if tile.rect.colliderect(player.rect):
                    if player.movement[0] > 0:
                        player.rect.right = tile.rect.left
                        self.collision_types['right'] = True
                    if player.movement[0] < 0:
                        player.rect.left = tile.rect.right
                        self.collision_types['left'] = True

            player.y = player.rect.y
            player.y += player.movement[1]
            player.rect.y = int(player.y)

            maxVerticalOffset = 0  # in cases where player collides with multiple slopes at once, we should move him by maximum required amount, otherwise he'll be moved up next frame. Less jitter
            for slope in self.slopesgroup.sprites():
                if slope.rect.colliderect(player.rect):
                    offset = (slope.rect.left - player.rect.left, slope.rect.top - player.rect.top-1)
                    almostCollisionOffset = player.mask.overlap(slope.mask, offset)  # if not None: player is exactly 1 pixel above slope, aka touching the slope, without being inside of it
                    realCollisionOffset = pygame.sprite.collide_mask(player, slope)  # if not None: Player has at least 1 pixel inside the slope

                    if almostCollisionOffset:
                        self.collision_types['bottom'] = True  # remove vertical momentum

                    if realCollisionOffset:
                        verticalOffset = player.rect.height - realCollisionOffset[1]  # move the player by this amount, and he'll be touching the current ground tile without being inside of it
                        if verticalOffset > maxVerticalOffset:
                            maxVerticalOffset = verticalOffset
                        self.collision_types['bottom'] = True
            if maxVerticalOffset:
                player.rect.bottom -= maxVerticalOffset

            maxtopVerticalOffset = 0
            for topslope in self.topslopesgroup.sprites():
                if topslope.rect.colliderect(player.rect):
                    topoffset = (topslope.rect.left - player.rect.left, topslope.rect.top - player.rect.top + 1)
                    almostCollisionOffset1 = player.mask.overlap(topslope.mask, topoffset)
                    realCollisionOffset2 = pygame.sprite.collide_mask(player, topslope)
                    if almostCollisionOffset1:
                        player.vertical_momentum = 0  # remove vertical momentum
                        player.collide_bottom = False
                    if realCollisionOffset2:
                        verticalOffset2 = player.rect.height + realCollisionOffset2[1]
                        if verticalOffset2 > maxtopVerticalOffset:
                            maxtopVerticalOffset = verticalOffset2
                            player.collide_bottom = False
            if maxtopVerticalOffset:
                player.rect.top += maxtopVerticalOffset

            for coin in self.coin.sprites():
                if coin.rect.colliderect(player.rect):
                    self.coin.remove(coin)
            for mushroom in self.mushroom_group.sprites():
                mushroom_top = mushroom.rect.top
                player_bottom = player.rect.bottom
                if mushroom_top <= player_bottom:
                    if mushroom.rect.colliderect(player.rect):
                        self.mushroom_group.remove(mushroom)
                        self.mushroom_inv += 1

            self.merchant_beside = 0
            for merchant in self.merchant_group.sprites():
                if merchant.rect.colliderect(player.rect):
                    self.merchant_beside += 1

            for death in self.Death.sprites():
                if death.rect.colliderect(player.rect):
                    self.dead = True
                    self.health = 0
                    self.player.empty()

            for tile in self.tiles.sprites():
                if tile.rect.colliderect(player.rect):
                    if player.movement[1] > 0:
                        player.rect.bottom = tile.rect.top
                        self.collision_types['bottom'] = True
                    if player.movement[1] < 0:
                        player.rect.top = tile.rect.bottom
                        self.collision_types['top'] = True

            for coin in self.coin.sprites():
                if coin.rect.colliderect(player.rect):
                    self.coin.remove(coin)
            if self.collision_types['bottom']:
                player.collide_bottom = True
                player.air_timer = 0
                player.vertical_momentum = 0
            else:
                player.collide_bottom = False
                player.air_timer += 1

            if self.collision_types['top']:
                player.vertical_momentum = 0
    def attack(self):
        if self.dead == False:
            player = self.player.sprite
            player.x = player.rect.x
            player.x += player.movement[0]
            player.rect.x = int(player.x)
            for swordsman in self.swordsman_group.sprites():
                if swordsman.rect.colliderect(player.rect):
                    self.health -= 2
                    # play animation of swordman swinging sword in direction of player


    def merchant_check(self):
        if self.merchant_beside != 0:
            return True
        else:
            return False


    def dying(self):
        self.player.empty()
        self.player = pygame.sprite.GroupSingle()
        if self.scroll[0] == 0 and self.scroll[1] == 0:
            self.create_sprite(self.spawn, 'Spawn')

            print('YOU DIED')
            self.health = 20
    def draw_img(self, img, x, y):
        self.surface.blit(img, (x, y))
    def draw_bg(self):
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_RIGHT] and self.player_direction < 3000:
            self.player_direction += 1
        elif self.keys[pygame.K_LEFT] and self.player_direction > 0:
            self.player_direction -= 1
        for x in range(14):
            speed = 1
            for i in self.bg_imgs:
                self.surface.blit(i, ((x * 600) - self.player_direction * speed, 0))
                speed += 0.1
    def draw_hearts(self):
        half_hearts_total = self.health / 2
        half_heart_exists = half_hearts_total - int(half_hearts_total) != 0
        for heart in range(int(self.max_health / 2)):
            if int(half_hearts_total) > heart:
                self.surface.blit(self.full_heart, (heart * 30 + 5, 10))
            elif half_heart_exists and int(half_hearts_total) == heart:
                self.surface.blit(self.half_heart, (heart * 30 + 5, 10))
            else:
                self.surface.blit(self.empty_heart, (heart * 30 + 5, 10))
        if self.health == 0:
            self.dying()
    def button_held(self):
        player = self.player.sprite
        player.jump_held = True

    def button_released(self):
        player = self.player.sprite
        player.jump_held = False
    def run(self):
        # tiles
        self.time_elasped = (time.time() - self.start_time) * 50
        self.scrolling()
        # death
        if self.dead:
            self.dying()
        # merchant check
        self.merchant_check()
        #background drawing
        self.tiles.update(self.scroll)
        self.tiles.draw(self.surface)
        self.slopesgroup.update(self.scroll)
        self.slopesgroup.draw(self.surface)
        self.topslopesgroup.update(self.scroll)
        self.topslopesgroup.draw(self.surface)
        self.mushroom_group.update(self.scroll)
        self.mushroom_group.draw(self.surface)

        self.bg_objects.update(self.scroll)
        self.bg_objects.draw(self.surface)
        self.heart_objects.draw(self.surface)
        self.coin.update(self.scroll)
        self.coin.draw(self.surface)
        self.tree.update(self.scroll)
        self.tree.draw(self.surface)
        self.blob_group.update(self.scroll)
        self.blob_group.draw(self.surface)
        self.swordsman_group.update(self.scroll)
        self.swordsman_group.draw(self.surface)
        self.Death.update(self.scroll)
        self.Spawn.update(self.scroll)
        self.merchant_group.update(self.scroll)
        self.merchant_group.draw(self.surface)
        # player
        player = self.player.sprite

        self.player.update(self.scroll)
        self.player.draw(self.surface)
        self.collision_movement()


