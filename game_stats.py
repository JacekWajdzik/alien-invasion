class GameStats():
	'''Monitorowanie danych statystycznych w grze "Alien Invasion"'''
	
	def __init__(self, ai_settings):
		'''Inicjalizacja statystyk'''
		self.ai_settings = ai_settings
		self.reset_stats()
		self.game_active = False
		self.game_paused = False
		self.high_score = 0
	def reset_stats(self):
		'''Inicjalizacja zmiennych danych'''
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0
		self.level = 1
