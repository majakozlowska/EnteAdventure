import pygame
import game_ente


def nick1():
    #stworzenie okna z polem do podania tekstu oraz inicjalizacja zmiennych 
    WIDTH = 1200
    HEIGHT = 900
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    bg = pygame.image.load("assets/bluenick.png")
    font = pygame.font.Font("assets/pixeleum-48.ttf", 40)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(100, 290, 140, 60)
    color = pygame.Color(255, 255, 255)
    active = True
    text = ""
    done = False
    #pętla powodująca wyświetlenie i oczekiwanie na odpowiedź
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        #zapis do pliku 
                        file = open("assets/player1.txt", "w")
                        file.write(str(text))
                        file.close()
                        #wyczyszczenie zmiennej 
                        text = ''
                        #wywołanie funkcji do pobrania drugiego nicku 
                        nick2()
                    elif event.key == pygame.K_BACKSPACE:
                        #cofanie wpisanego tekstu 
                        text = text[:-1]
                    else:
                        text += event.unicode
        #wyświetlanie wpisanego tekstu w okienku na ekranie 
        screen.blit(bg, (0, 0))
        txt_surface = font.render(text, True, (13, 29, 98))
        width = max(1000, txt_surface.get_width()+20)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y-5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)

def nick2():
    #stworzenie okna do pobrania drugiego nicku i pozostałe jak wyżej 
    WIDTH = 1200
    HEIGHT = 900
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    bg = pygame.image.load("assets/rednick.png")
    font = pygame.font.Font("assets/pixeleum-48.ttf", 40)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(100, 290, 140, 60)
    color = pygame.Color(255, 255, 255)
    active = True
    text = ""
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        file1 = open("assets/player2.txt", "w")
                        file1.write(str(text))
                        file1.close()
                        print(text)
                        text = ''
                        game_ente.game2()
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.blit(bg, (0, 0))
        txt_surface = font.render(text, True, (136, 1, 10))
        width = max(1000, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y-5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)

pygame.quit()