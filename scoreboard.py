import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
	'''Klasa przedstawia punktacje'''
	def __init__(self, ai_settings, screen, stats):
		'''Inicjalizacja atrybutow punktacji'''
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.ai_settings = ai_settings
		self.stats = stats
		
		self.text_color = (0, 0, 0)
		self.font = pygame.font.SysFont(None, 40)
		
		self.prep_level()
		self.prep_score()
		self.prep_high_score()
		self.prep_ships()
	
	def prep_score(self):
		'''Przeksztalcenie punktacji w obraz'''
		score_str = 'SCORE: ' + "{:,}".format(self.stats.score)
		self.score_image = self.font.render(score_str, True, 
					self.text_color, self.ai_settings.bg_color)
		self.score_rect = self.score_image.get_rect()
		self.score_rect.centerx = self.screen_rect.centerx
		self.score_rect.top = self.level_rect.top
		
	def prep_high_score(self):
		'''Konwerscja najlepszego wyniku w obraz'''
		high_score_str ='HS: ' + "{:,}".format(self.stats.high_score)
		self.high_score_image = self.font.render(high_score_str, True, 
					self.text_color, self.ai_settings.bg_color)
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.right = self.level_rect.left - 20
		self.high_score_rect.top = self.level_rect.top
		
	def prep_level(self):
		'''Przygotowanie poziomu do wyswietlenia'''
		self.level_image = self.font.render(('LVL ' + str(self.stats.level)),
							True, self.text_color, self.ai_settings.bg_color)
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.screen_rect.right - 20
		self.level_rect.top = 5
				
	def prep_ships(self):
		'''Przygotowanie do wyswietlania pozostalych statkow'''
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.ai_settings, self.screen, True)
			ship.rect.x = 10 + ship_number * ship.rect.width
			ship.rect.y = 5
			self.ships.add(ship)
	
	def show_score(self):
		'''Wyswietlenie punktacji na ekranie'''
		self.screen.blit(self.level_image, self.level_rect)
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.ships.draw(self.screen)
