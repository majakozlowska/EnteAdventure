import pygame
import sys
import game_ente
import nicki

pygame.init()

#inicjalizacja miksera audio 
pygame.mixer.pre_init()
pygame.mixer.init(frequency=44100, size=-16, channels=4, buffer=512)

#wczytanie muzyki/dźwięków i przypisanie do zmiennych 
sound_menu = pygame.mixer.Sound("assets/a.wav")
sound_game = pygame.mixer.Sound("assets/c.wav")
sound_shot = pygame.mixer.Sound("assets/shot.wav")
sound_heal = pygame.mixer.Sound("assets/heal.wav")
sound_lost = pygame.mixer.Sound("assets/lost.wav")
sound_what = pygame.mixer.Sound("assets/what.wav")
sound_easteregg = pygame.mixer.Sound('assets/heal.wav')
sound_easteregg_end = pygame.mixer.Sound('assets/Poof.wav')

#inicjalizacja kanałów w mikserze
pygame.mixer.Channel(1)
pygame.mixer.Channel(2)
pygame.mixer.Channel(3)

#regulacja głośności dźwęków 
sound_menu.set_volume(0.5)
sound_game.set_volume(0.5)
sound_shot.set_volume(0.5)

#uruchomienie muzyki w menu w nieskończonej pętli 
pygame.mixer.Channel(1).play(sound_menu, loops=-1)
#inicjalizacja zmiennych oraz zmiana tytułu i ikony okna 
WIDTH = 1200
HEIGHT = 900
i = 0
bg_img = pygame.image.load("assets/bg_image.png")
bg = pygame.transform.scale(bg_img, (1200, 900))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
loading = True
pygame.display.set_caption("Menu")
icon = pygame.image.load("assets/icon_img.png")
pygame.display.set_icon(icon)

#stworzenie funkcji odtwarzających dźwięki 
def collision_shell():
    pygame.mixer.Channel(3).play(sound_shot)

def collision_powerup():
    pygame.mixer.Channel(3).play(sound_heal)

def lost_sound():
    pygame.mixer.Channel(3).play(sound_lost)

def lost2_sound():
    pygame.mixer.Channel(3).play(sound_what)

def easteregg():
     pygame.mixer.Channel(3).play(sound_easteregg)


def easteregg_end():
    pygame.mixer.Channel(3).play(sound_easteregg_end)

#zdeklarowanie klasy Button od przycisków i ich działania 
class Button():
	def __init__(self, image, hover_image, pos, text_input, font):
		self.image = image
		self.hover_image = hover_image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
    
    #odświeżanie wyglądu przycisku 
	def update(self, screen):
		screen.blit(self.image, self.rect)
                
    #sprawdzanie czy przycisk naciśnięty
	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

    #zmiana koloru po naciśnięciu przycisku 
	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.image = self.hover_image

#funkcja od czcionki 
def get_font(size):
    return pygame.font.Font("assets/pixeleum-48.ttf", 40)

#uruchomienie menu głównego i jego muzyki 
def music_main_menu():
    pygame.mixer.Channel(1).play(sound_menu, loops=-1)
    main_menu()

while loading == True:

    #uruchomienie gry 1 osobowej 
    def play():
        game_ente.game()
    
    #uruchomienie gry 2 osobowej 
    def play2():
        nicki.nick1()

    #funkcja odpowiedzialna za funkcjonalność menu 
    def main_menu():
        while True:
            i = 0
            screen.blit(bg, (i, 0))
            screen.blit(bg, (WIDTH+i, 0))
            if i == -WIDTH:
                screen.blit(bg, (WIDTH+i, 0))
                i = 0
            i -= 1

            #wczytanie najwyższego wyniku do zmiennej 
            with open("assets\Highscore.txt", "r") as HS:
                Hiscore = (HS.read())
                HS.close()
                #wyświetlenie najwyższego wyniku 
                HS_TEXT = get_font(20).render("High score: " + Hiscore, True, "White")
                HS_RECT = HS_TEXT.get_rect(center=(600, 850))
                screen.blit(HS_TEXT, HS_RECT)

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            #przyciski i wczytanie na nie grafiki 
            ONEPLAYER_BUTTON = Button(image=pygame.image.load("assets/oneplayer_button.png"), hover_image=pygame.image.load("assets/oneplayer_hover.png"), pos=(565, 445), 
                                    text_input=None, font=get_font(75))
            TWOPLAYERS_BUTTON = Button(image=pygame.image.load("assets/twoplayers_button.png"), hover_image=pygame.image.load("assets/twoplayers_hover.png"), pos=(565, 535), 
                                    text_input=None, font=get_font(75))
            QUIT_BUTTON = Button(image=pygame.image.load("assets/quit_button.png"), hover_image=pygame.image.load("assets/quit_hover.png"), pos=(570, 625), 
                                    text_input=None, font=get_font(75))

            #sprawdzanie czy przycisk naciśnięty 
            for button in [ONEPLAYER_BUTTON, TWOPLAYERS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(screen)
            
            #reakcja na eventy w menu 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ONEPLAYER_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.mixer.stop()
                        pygame.mixer.Channel(2).play(sound_game, loops=-1)
                        play()
                    if TWOPLAYERS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.mixer.stop()
                        pygame.mixer.Channel(2).play(sound_game, loops=-1)
                        play2()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
            pygame.display.flip()

    main_menu()