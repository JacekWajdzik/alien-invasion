import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	'''Klasa przedstawiajaca obraz statku kosmicznego'''
	
	def __init__(self, ai_settings, screen, scaleship=False):
		'''Inicjalizacja statku kosmicznego i jego polozenie poczatkowe'''
		super().__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		#Wczytanie obrazu rakiety i pobranie jego prostokata
		self.image = pygame.image.load('images/rocket.bmp')
		if scaleship:
			self.image = pygame.transform.scale(self.image, (20, 40))
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		#Kazdy nowy statek pojawia sie na dole ekranu
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		#Punkt srodkowy statku
		self.center = float(self.rect.centerx)
		#Opcje wskazujace na poruszanie sie statku
		self.moving_right = False
		self.moving_left = False
		
	def update(self):
		'''Uaktualnienie poruszania sie statku na podstawie opcji wskazujacej
		na jego ruch'''
		
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > 0:
			self.center -= self.ai_settings.ship_speed_factor
		
		self.rect.centerx = self.center
		
	def blitme(self):
		'''Wyswietlenie statku w jego aktualnym polozeniu'''
		self.screen.blit(self.image, self.rect)
	
	def center_ship(self):
		'''Umieszczenie statku na srodku przy dolnej krawedzi ekranu'''
		self.center = self.screen_rect.centerx
	
