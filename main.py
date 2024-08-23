import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from level import Level
from overworld import OverWorld, MainMenu, IntroductionScreen
from ui import UI


class Game:
    def __init__(self):
        pygame.init()
        # Screen Setup
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('PLATFORMER')
        pygame.display.set_icon(pygame.image.load('../graphics/64629c0ba19e223.png'))
        self.background = pygame.transform.scale(pygame.image.load(
            '../graphics/pixel-art-christmas-landscape-with-red-house-pine-snow-santa-claus-8-bit-game-background-vector.jpeg'),
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.ui = UI(self.screen)

        self.clock = pygame.time.Clock()
        self.max_level = 0
        self.over_world = OverWorld(0, self.max_level, self.screen, self.create_level)
        self.status = 'intro'
        self.main_menu = MainMenu(self.screen)
        self.game_complete = True
        self.introduction_screen = IntroductionScreen(self.screen, 3000, 1000)

    def create_level(self, current_level):
        self.level = Level(self.screen, current_level, self.create_over_world)
        self.status = 'level'

    def create_over_world(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.over_world = OverWorld(current_level, self.max_level, self.screen, self.create_level)
        self.status = 'over_world'

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def draw(self):
        self.screen.fill((155, 155, 155))
        self.screen.blit(self.background, (0, 0))
        # if self.status == 'main_menu':
        #     self.main_menu.draw()
        if self.game_complete:
            font = pygame.font.Font(None, 40)
            win_message = font.render("YOU COMPLETED THE GAME", True, (0, 0, 0))
            win_message_rect = win_message.get_rect(center=self.screen.get_rect().center)
            # self.screen.fill((255, 255, 255))
            self.screen.blit(win_message, win_message_rect)
        elif self.status == "intro":
            self.introduction_screen.update()
            self.introduction_screen.draw()
            if self.introduction_screen.is_finished():
                self.status = "main_menu"
        elif self.status == 'over_world':
            self.over_world.run()
        else:
            self.level.run()
            self.ui.show_coins(4)
        pygame.display.update()

    def run(self):
        while True:
            self.main_menu.input()
            self.input()
            self.draw()
            self.clock.tick(FPS)


if __name__ == '__main__':
    Game().run()
