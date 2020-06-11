class Settings():
	'''Klasa przeznaczona do przechowywania wszystkich ustawien gry'''
	
	def __init__(self):
		'''Inicjalizacja ustawien gry'''
		self.screen_width = 1366
		self.screen_height = 715
		self.bg_color = (255, 182, 193)
		self.ship_limit = 3
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (139, 0, 0)
		self.bullets_allowed = 5
		self.fleet_drop_speed = 30 #w dol
		self.speedup_scale = 1.1
		self.score_scale = 1.5
		self.initialize_dynamic_settings()
	
	def initialize_dynamic_settings(self):
		'''Inicjalizacja ustawien ulegajacych zmianie'''
		self.ship_speed_factor = 1.2
		self.bullet_speed_factor = 2
		self.alien_speed_factor = 0.66
		self.fleet_direction = 1 #1-w prawo, -1-w lewo
		self.alien_points = 50
		
	def increase_speed(self):
		'''Zmiana ustawien szybkosci'''
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		self.alien_points = int(self.alien_points * self.score_scale)
		
		
		
