import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from ship import Ship
from button import Button
from scoreboard import Scoreboard
import game_functions as gf

def run_game():
	
	#Inicjalizacja Pygame, ustawien i obiektu ekranu
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
	pygame.display.set_caption("Inwazja obcych")
	
	#Utworzenie przycisku
	play_button = Button(ai_settings, screen, 'Graj')
	pause_button = Button(ai_settings, screen, 'Pauza')
	
	#Utworzenie egzemplarza GameStats
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)
	#Utworzenie rakiety
	ship = Ship(ai_settings, screen)
	#Utworzenie grupy pociskow
	bullets = Group()
	aliens = Group()
	gf.create_fleet(ai_settings, screen, ship, aliens)
	
	#Rozpoczecie petli glownej gry
	while True:
		gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
						aliens, bullets)
		if stats.game_active and not stats.game_paused:
			ship.update()
			gf.update_bullets(ai_settings, screen, stats, sb, 
								ship, aliens, bullets)
			gf.update_aliens(ai_settings, stats, screen, sb,
								ship, aliens, bullets)		
		gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
							play_button, pause_button)
		
		
run_game()
	
