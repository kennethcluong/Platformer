import pygame
from game_data import levels
from support import import_folder, Spritesheet
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
import sys


class Node(pygame.sprite.Sprite):
    def __init__(self, position, status, icon_speed, path):
        super().__init__()
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = pygame.Surface((50, 50))
        if status == 'unlocked':
            self.status = 'unlocked'
            self.image.fill('green')
        else:
            self.status = 'locked'
            self.image.fill('red')
        self.rect = self.image.get_rect(center=position)
        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed / 2),
                                          self.rect.centery - (icon_speed / 2),
                                          icon_speed,
                                          icon_speed)

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        if self.status == 'unlocked':
            # self.animate()
            pass
        else:
            tint_surface = self.image.copy()
            tint_surface.fill('black', None, pygame.BLEND_RGBA_MULT)
            self.image.blit(tint_surface, (0, 0))


class Icon(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.position = position
        self.image = pygame.Surface((20, 20))
        self.image.fill('blue')
        self.rect = self.image.get_rect(center=position)

    def update(self):
        self.rect.center = self.position


class OverWorld:
    def __init__(self, start_level, max_level, display_surface, create_level):
        self.current_level = start_level
        self.max_level = max_level
        self.display_surface = display_surface
        self.create_level = create_level

        self.moving = False
        self.move_direction = pygame.math.Vector2(0, 0)
        self.speed = 8

        self.setup_nodes()
        self.setup_icon()

    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()

        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], 'unlocked', self.speed, node_data['node_graphics'])
            else:
                node_sprite = Node(node_data['node_pos'], 'locked', self.speed, node_data['node_graphics'])
            self.nodes.add(node_sprite)

    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def draw_paths(self):
        if self.current_level > 0:
            points = [node_data['node_pos'] for index, node_data in enumerate(levels.values()) if index <= self.max_level]
            pygame.draw.lines(self.display_surface, (255, 150, 100), False, points, 6)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.moving:
            if keys[pygame.K_d] and self.current_level < self.max_level:
                # self.move_direction =
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_a] and self.current_level > 0:
                # self.move_direction =
                self.current_level -= 1
                self.moving = True
            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)

    def get_movement_data(self, target):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)

        if target == 'next':
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)

        return (end - start).normalize()

    def update_icon_position(self):
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0, 0)

    def run(self):
        self.input()
        self.update_icon_position()
        self.icon.update()
        self.nodes.update()
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)


class MainMenu:
    def __init__(self, display_surface):
        self.display_surface = display_surface
        self.font = pygame.font.Font(None, 50)

        # self.title = self.font.render("Pirate Spidey Parkour", True, (255, 0, 0), (0, 0, 0))
        # self.title = Spritesheet(pygame.image.load("../graphics/spritesheet.png").convert_alpha())
        # self.title_rect = self.title.get_rect()
        self.title_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        self.play = self.font.render("PLAY", True, (255, 0, 0), (0, 0, 0))
        self.play_rect = self.play.get_rect()
        self.play_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)

        self.quit = self.font.render("QUIT", True, (255, 0, 0), (0, 0, 0))
        self.quit_rect = self.quit.get_rect()
        self.quit_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100)

        self.in_main_menu = True

    def draw(self):
        self.display_surface.blit(self.title, self.title_rect)
        self.display_surface.blit(self.play, self.play_rect)
        self.display_surface.blit(self.quit, self.quit_rect)

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    if self.play_rect.collidepoint(pygame.mouse.get_pos()):
                        self.in_main_menu = False
                    if self.quit_rect.collidepoint(pygame.mouse.get_pos()):
                        pygame.quit()
                        sys.exit()


class IntroductionScreen:
    def __init__(self, display_surface, duration, fade_duration):
        self.display_surface = display_surface
        self.duration = duration
        self.fade_duration = fade_duration
        self.start_time = pygame.time.get_ticks()
        self.alpha = 255  # start fully opaque
        self.image = pygame.image.load().convert()

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time

        if elapsed_time > self.duration:
            fade_time = elapsed_time - self.duration
            self.alpha = max(255 - int((fade_time / self.fade_duration) * 255), 0)

    def draw(self):
        faded_image = self.image.copy()
        faded_image.set_alpha(self.alpha)
        self.display_surface.blit(faded_image, (0, 0))

    def is_finished(self):
        return self.alpha == 0



