import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	'''Klasa przedstawiajaca pojedynczego obcego'''
	def __init__(self, ai_settings, screen):
		'''Inicjalizacja obcego i zdefiniowanie jego polozenia'''
		super().__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		self.image = pygame.image.load('images/ufo3.bmp')
		self.rect = self.image.get_rect()
		
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		
		self.x = float(self.rect.x)
		
	def blitme(self):
		'''Wyswietlenie obcego w aktualnym polozeniu'''
		self.screen.blit(self.image, self.rect)
		
	def update(self):
		'''Przesuniecie obcego w prawo'''
		self.x += (self.ai_settings.alien_speed_factor * 
					self.ai_settings.fleet_direction)
		self.rect.x = self.x
		
	def check_edges(self):
		'''Zwraca wartosc True, gdy obcy beda przy krawedzi'''
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True
