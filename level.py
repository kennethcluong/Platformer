import pygame
from settings import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from tile import Tile
from player import Player
from particles import ParticleEffect
from game_data import levels
from timer import Timer
import os
# from decoration import Water, Clouds


class Level:
    def __init__(self, display_surface, current_level, create_over_world):
        self.timer = Timer()
        self.current_level = current_level
        level_data = levels[self.current_level]
        level_content = level_data['content']
        self.new_max_level = level_data['unlock']
        self.create_over_world = create_over_world

        self.background = pygame.transform.scale(pygame.image.load('../graphics/9213.jpeg'),
                                                 (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.font = pygame.font.Font(None, 40)
        self.text_surface = self.font.render(level_content, True, 'white')
        self.text_rect = self.text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

        self.display_surface = display_surface
        self.setup_level(level_data['layout'])
        self.world_shift = 0
        self.current_x = 0
        self.lives = 3

        self.dust_sprite = pygame.sprite.GroupSingle()
        self.explosion_sprites = pygame.sprite.Group()
        self.player_on_ground = False

        self.original_spawn_position = (0, 200)
        self.original_tile_positions = {}

        for sprite in self.tiles.sprites():
            self.original_tile_positions[sprite] = sprite.rect.topleft
        self.best_time = self.load_best_time()

        # Decoration Configuration
        # self.water = Water(SCREEN_HEIGHT - 20, SCREEN_WIDTH * TILE_SIZE, 192)
        # self.cloud_sprites = Clouds(400, SCREEN_WIDTH * TILE_SIZE, 30)

    def load_best_time(self):
        filename = f"best_time_level_{self.current_level}.txt"
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return float(f.read().strip())
        return 6000000000000000000

    def save_best_time(self):
        filename = f"best_time_level_{self.current_level}.txt"
        with open(filename, 'w') as f:
            f.write(str(self.best_time))

    def create_jump_particles(self, position):
        if self.player.sprite.facing_right:
            position -= pygame.math.Vector2(10, 5)
        else:
            position += pygame.math.Vector2(10, -5)
        jump_particle_sprite = ParticleEffect(position, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_floor and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)

    def get_player_on_ground(self):
        if self.player.sprite.on_floor:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        # dict_values([level_0, level_1])

        for row_index, row in enumerate(layout):
            for column_index, column in enumerate(row):
                x = column_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if column == 'X':
                    tile = Tile((x, y))
                    self.tiles.add(tile)
                if column == 'P':
                    player_sprite = Player((x, y), self.display_surface, self.create_jump_particles)
                    self.player.add(player_sprite)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < SCREEN_WIDTH / 4 and direction_x < 0:
            self.world_shift = 5
            player.speed = 0
        elif player_x > SCREEN_WIDTH - (SCREEN_WIDTH / 4) and direction_x > 0:
            self.world_shift = -5
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_floor = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_floor and player.direction.y < 0 or player.direction.y > 1:
            player.on_floor = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

    def check_enemy_collision(self):
        if True:
            self.player.sprite.direction.y = -15
            explosion_sprite = ParticleEffect(enemy.rect.center, "explosion")
            self.explosion_sprites.add(explosion_sprite)
            enemy.kill()
        else:
            pass

    def enemy_horizontal_movement_collision(self):
        for enemy in self.enemies.sprites():
            enemy.rect.x += enemy.direction.x * enemy.speed
            for tile in self.tiles.sprites():
                if tile.rect.colliderect(enemy.rect):
                    enemy.reverse()
                    break
            enemy.rect.x -= enemy.direction.x * enemy.speed

    def check_death_condition(self):
        # or pygame.sprite.spritecollide(self.player.sprite, self.enemy, False)
        if self.player.sprite.rect.top > SCREEN_HEIGHT:
            self.player.sprite.rect.midbottom = self.original_spawn_position
            for sprite, original_position in self.original_tile_positions.items():
                sprite.rect.topleft = original_position
            self.lives -= 1
            print(self.lives)
            if self.lives == 0:
                self.timer.reset()
                self.create_over_world(self.current_level, 0)

    def check_win_condition(self):
        if pygame.sprite.spritecollide(self.player, self.portal):
            if self.timer.elapsed_time <= self.timer.best_time:
                self.timer.best_time = self.timer.elapsed_time
                self.save_best_time()
            self.create_over_world(self.current_level, self.new_max_level)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            self.create_over_world(self.current_level, self.new_max_level)
        if keys[pygame.K_ESCAPE]:
            self.create_over_world(self.current_level, 0)

    def run(self):
        # self.cloud_sprites.draw(self.display_surface, self.world_shift)
        self.input()
        self.display_surface.blit(self.background, (0, 0))
        self.display_surface.blit(self.text_surface, self.text_rect)
        # Dust Particles

        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # Enemy
        self.explosion_sprites.update(self.world_shift)
        self.explosion_sprites.draw(self.display_surface)

        # Level Tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        # Player
        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()
        self.player.draw(self.display_surface)
        self.timer.update()
        self.timer.draw(self.display_surface)
        self.check_death_condition()
        self.check_enemy_collision()
        # self.water.draw(self.display_surface, self.world_shift)
