import sys
import pygame
from time import sleep
from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, stats, sb, ship, 
							aliens, bullets):
	'''Reakcja na nacisniecie klawisza'''
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE and not stats.game_paused:
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_ESCAPE:
		sys.exit()
	elif event.key == pygame.K_RETURN:
		if not stats.game_active:
			start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)
		else:
			if stats.game_paused:
				stats.game_paused = False
			else:
				stats.game_paused = True

def check_keyup_events(event, ship):
	'''Reakcja na puszczenie klawisza'''
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship,
					aliens, bullets):
	'''Reakcja na zdarzenia generowane przez klawiature lub mysz'''
	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				check_keydown_events(event, ai_settings, screen, stats, sb, ship,
				 aliens, bullets)
			elif event.type == pygame.KEYUP:
				check_keyup_events(event, ship)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_x, mouse_y = pygame.mouse.get_pos()
				check_play_button(ai_settings, screen, stats, sb, play_button,
									ship, aliens, bullets, mouse_x, mouse_y)
		
def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
	'''Rozpoczecie nowej gry'''
	ai_settings.initialize_dynamic_settings()
	pygame.mouse.set_visible(False)
	stats.reset_stats()
	stats.game_active = True
	
	aliens.empty()
	create_fleet(ai_settings, screen, ship, aliens)
	ship.center_ship()
	bullets.empty()
	sb.prep_level()
	sb.prep_score()
	sb.prep_high_score()
	sb.prep_ships()
			
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, 
					aliens, bullets, mouse_x, mouse_y):
	'''Rozpoczecie nowej gry po kliknieciu przycisku Graj'''
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active	:
		start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)
				
def fire_bullet(ai_settings, screen, ship, bullets):
	'''Wystrzelenie pocisku jesli nie przekroczono limitu'''
	if len(bullets) < ai_settings.bullets_allowed:
			new_bullet = Bullet(ai_settings, screen, ship)
			bullets.add(new_bullet)
			
def update_screen(ai_settings, screen, stats, sb, ship, aliens,
					bullets, play_button, pause_button):
	'''Uaktualnienie obrazow na ekranie i przejscie do nowego ekranu'''
	#Odswierzenie ekranu w trakcie kazde iteracji		
	screen.fill(ai_settings.bg_color)
	#Ponowne wyswietlenie wszystkich pociskow pod warstwami
	#rakiety i obcych
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	
	ship.blitme()
	aliens.draw(screen)
	sb.show_score()
	
	if not stats.game_active:
		play_button.draw_button()
	if stats.game_paused:
		pause_button.draw_button()
	
	#Wyswietlenie ostatnio zmodyfikowanego ekranu
	pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
	'''Uaktualnienie polozenia pociskow'''
	bullets.update()	
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
			stats.score -= 5
			sb.prep_score()
	check_bullet_alien_collision(ai_settings, screen, stats, sb, 
									ship, aliens, bullets)

def check_bullet_alien_collision(ai_settings, screen, stats, sb, 
									ship, aliens, bullets):
	'''Reakcja na kolizje pocisku i obcego'''
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats, sb)
		
	if(len(aliens)) == 0:
		bullets.empty()
		ai_settings.increase_speed()
		stats.level += 1
		sb.prep_level()
		create_fleet(ai_settings, screen, ship, aliens)

def get_number_alien_x(ai_settings, alien_width):
	'''Ustalenie liczby obcych mieszczacych sie w rzedzie'''
	available_space_x = ai_settings.screen_width - 2*alien_width
	number_aliens_x = int(available_space_x / (2*alien_width))
	return number_aliens_x
	
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	'''Utworzenie obcego i umieszczenie go w rzedzie'''
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2*alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2*alien.rect.height * row_number
	aliens.add(alien)

def get_number_rows(ai_settings, ship_height, alien_height):
	'''Ustalenie ile rzedow obcych zmiesci sie na ekranie'''
	available_space_y = (ai_settings.screen_height -
						(3*alien_height) - ship_height)
	number_rows = int(available_space_y / (2*alien_height))
	return number_rows	
	

def create_fleet(ai_settings, screen, ship, aliens):
	'''Utworzenie pelnej floty obcych'''
	#Utworzenie obcego i ustalenie liczby obcych, ktorzy mieszcza sie w rzedzie
	#Odleglosc miedzy obcymi jest rowna szerokosci obcego
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_alien_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, 
									alien.rect.height)
	
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number, row_number)
	
def check_fleet_edges(ai_settings, aliens):
	'''Odpowiednia reakcja na dotarcie do krawedzi'''
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break
			
def change_fleet_direction(ai_settings, aliens):
	'''Przesuniecie calej floty w dol i zmiana kierunku'''
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
	'''Sprawdzenie czy ktorys obcy dotarl do konca ekranu'''
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
			break

def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
	'''Uaktualnienie polozenia wszystkich obcych'''
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	#Wykrywanie kolizji miedzy rakieta a obcymi
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
	check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)
	
def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
	'''Reakcja na uderzenie obcego w statek'''
	if stats.ships_left > 0:
		sleep(0.5)
		stats.ships_left -= 1
		sb.prep_ships()
		aliens.empty()
		
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		
		bullets.empty()
		
		
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
	
def check_high_score(stats, sb):
	'''Sprawdzenie czy osiagnieto najlepszy wynik'''
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
