import pygame
import random
import menu_lobby

pygame.init()
pause = False

#zdefiniowanie opcji powrotu do menu 
def back_menu():
    pygame.mixer.fadeout(3000)
    pygame.time.wait(3000)
    pygame.display.update()
    pygame.display.flip()
    menu_lobby.music_main_menu()

def back_menu_fast():
    pygame.mixer.fadeout(500)
    pygame.time.wait(500)
    pygame.display.update()
    pygame.display.flip()
    menu_lobby.music_main_menu()

#zdefiniowanie gry 
def game():
    #inicjalizcja zmiennych i stałych 
    WIDTH = 1200
    HEIGHT = 900
    i = 0
    bg = pygame.image.load("assets/bg_game_image.png")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Ente Reise")
    icon = pygame.image.load("assets/icon_img.png")
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()

    player_img = pygame.image.load("assets/ente.png").convert_alpha()
    powerup1 = pygame.image.load("assets/bread.png").convert_alpha()
    powerup2 = pygame.image.load("assets/loaf.png").convert_alpha()
    powerup3 = pygame.image.load("assets/crossaint.png").convert_alpha()
    enemy_img = pygame.image.load("assets/bullet.png").convert_alpha()

    font = pygame.font.Font("assets/pixeleum-48.ttf", 80)
    lost = False
    lost_img = pygame.image.load("assets/lost_game.png")
    score = 0
    hiscore = 0

    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 400)

    ADDPOWERUP = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDPOWERUP, 6000)

    ADDSCORE = pygame.USEREVENT + 3
    pygame.time.set_timer(ADDSCORE, 50)
    
    #zdefiniowanie klasy gracza
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super(Player, self).__init__()
            self.surf = player_img
            self.surf = player_img
            self.rect = self.surf.get_rect(
                center = (
                    100,
                    HEIGHT / 2
                )
            )
            self.speed = 10

        #poruszanie gracza
        def update(self, keys):
            self.surf = player_img

            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
                self.rect.move_ip(-self.speed, 0)
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < WIDTH:
                self.rect.move_ip(self.speed, 0)
            if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 0:
                self.rect.move_ip(0, -self.speed)
            if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < HEIGHT:
                self.rect.move_ip(0, self.speed)
            if keys[pygame.K_ESCAPE]:
                back_menu_fast()

    #zdefiniowanie klasy wroga
    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            super(Enemy, self).__init__()
            self.surf = enemy_img
            self.rect = self.surf.get_rect(
                center = (
                    random.randint(WIDTH + 20, WIDTH + 100),
                    random.randint(60, HEIGHT - 60)
                )
            )
            self.speed = random.randint(5, 20)

        #losowe prędkości wrogów 
        def update(self):
            self.rect.move_ip(-self.speed, 0)
            if self.rect.right < 0:
                self.kill()

    #zdefiniowanie klasy powerup
    class Powerup(pygame.sprite.Sprite):
        POWERUP_MAP = {
                    "p1": (powerup1),
                    "p2": (powerup2),
                    "p3": (powerup3)
                    }
        #losowanie położenia i prędkości powerupów
        def __init__(self, p_type):
            super(Powerup, self).__init__()
            self.surf = self.POWERUP_MAP[p_type]
            self.rect = self.surf.get_rect(
                center = (
                    random.randint(WIDTH + 20, WIDTH + 100),
                    random.randint(20, HEIGHT-160)
                )
            )
            self.speed = random.randint(5, 20)
            self.p_type = p_type

        #uaktualnienie pozycji powerupów
        def update(self):
            self.rect.move_ip(-self.speed, 0)
            if self.rect.right < 0:
                self.kill()

    player = Player()
    enemies = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    health = 200
    
    run = True
    lobby = False

    while run:
        #przesuwające się tło 
        clock.tick(60)
        screen.blit(bg, (i, 0))
        screen.blit(bg, (2730 + i, 0))

        if i == -2730:
            screen.blit(bg, (2730 + i, 0))
            i = 0
        i -= 1

        #obsługa eventów w grze 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lobby = True
            if event.type == ADDENEMY:
                enemy = Enemy()
                enemies.add(enemy)
                all_sprites.add(enemy)
            if event.type == ADDPOWERUP:
                powerup = Powerup(random.choice(["p1", "p2", "p3"]))
                powerups.add(powerup)
                all_sprites.add(powerup)
            if event.type == ADDSCORE and lost == False:
                score += 1

        keys = pygame.key.get_pressed()
        player.update(keys)
        enemies.update()
        powerups.update()

        #kontrola kolizji wróg - gracz i ich obsługa
        for enemy in enemies:
            if pygame.Rect.colliderect(player.rect, enemy.rect):
                menu_lobby.collision_shell()
                enemy.kill()
                health -= 40
        
        #kontrola kolizji powerup - gracz i ich obsługa
        for powerup in powerups:
            if pygame.Rect.colliderect(player.rect, powerup.rect):
                menu_lobby.collision_powerup()
                powerup.kill()
                if health < 200:
                    health += 20
        
        #odświeżanie położenia duszków
        for sprite in all_sprites:
            screen.blit(sprite.surf, sprite.rect)

        #zakończenie gry gdy skończy się HP
        if health <= 0:
            lost = True

        #easteregg
        if score == 2137:
            menu_lobby.easteregg()

        if score > 2137 and score < 2400:
            player_img = pygame.image.load("assets/papjeszente.png")
        elif score == 2350:
            menu_lobby.easteregg_end()
        else:
            player_img = pygame.image.load("assets/ente.png")

        #zamknięcie okna gry, porównanie wyniku do rekordu i ew. zapis, jeżeli jest większy
        if lobby:
            if score > hiscore:
                file = open("assets/Highscore.txt", "w")
                file.write(str(score))
                file.close()
            back_menu_fast()

        if lost:
            #wyświetlenie obrazku przegranej i odegranie dźwięku 
            screen.blit(lost_img, (0, 0))
            menu_lobby.lost_sound()
            if score > hiscore:
                file = open("assets/Highscore.txt", "w")
                file.write(str(score))
                file.close()
            pygame.display.update()
            pygame.display.flip()
            back_menu()
        
        #wyświetlanie obecnego wyniku 
        score_label = font.render(f"{score}", 1, (255, 255, 255))
        screen.blit(score_label, (WIDTH/2 - score_label.get_width()/2, 4))

        #wyświetlanie i aktualizacja healthbaru 
        screen.blit(pygame.image.load("assets/healthbar.png"), (460, 120))
        pygame.draw.rect(screen, (102, 198, 79), (500, 150, (health), 20))

        pygame.display.update()
        pygame.display.flip()

    pygame.quit()

#większość jak wyżej 
def game2():
    WIDTH = 1200
    HEIGHT = 900
    i = 0
    bg = pygame.image.load("assets/bg_game_image.png")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Ente Reise")
    icon = pygame.image.load("assets/ente.png")
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()

    def paused():
        clock.tick(0)
        print("done")

    player1_img = pygame.image.load("assets/blueente.png").convert_alpha()
    player2_img = pygame.image.load("assets/redente.png").convert_alpha()
    powerup1 = pygame.image.load("assets/bread.png").convert_alpha()
    powerup2 = pygame.image.load("assets/loaf.png").convert_alpha()
    powerup3 = pygame.image.load("assets/crossaint.png").convert_alpha()
    enemy_img = pygame.image.load("assets/bullet.png").convert_alpha()

    font = pygame.font.Font("assets/pixeleum-48.ttf", 100)
    lost1 = False
    lost2 = False
    lost1_img = pygame.image.load("assets/red_win.png")
    lost2_img = pygame.image.load("assets/blue_win.png")

    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 400)

    ADDPOWERUP = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDPOWERUP, 6000)
    
    class Player1(pygame.sprite.Sprite):
        def __init__(self):
            super(Player1, self).__init__()
            self.surf = player1_img
            self.rect = self.surf.get_rect(
                center = (
                    100,
                    300
                )
            )
            self.speed = 10

        def update(self, keys):
            if keys[pygame.K_a] and self.rect.left > 0:
                self.rect.move_ip(-self.speed, 0)
            if keys[pygame.K_d] and self.rect.right < WIDTH:
                self.rect.move_ip(self.speed, 0)
            if keys[pygame.K_w] and self.rect.top > 0:
                self.rect.move_ip(0, -self.speed)
            if keys[pygame.K_s] and self.rect.bottom < HEIGHT:
                self.rect.move_ip(0, self.speed)
            if keys[pygame.K_ESCAPE]:
                back_menu_fast()
            if keys[pygame.K_p]:
                paused()
                print("paused")

    class Player2(pygame.sprite.Sprite):
        def __init__(self):
            super(Player2, self).__init__()
            self.surf = player2_img
            self.rect = self.surf.get_rect(
                center = (
                    100,
                    600
                )
            )
            self.speed = 10

        def update(self, keys):
            if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.move_ip(-self.speed, 0)
            if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
                self.rect.move_ip(self.speed, 0)
            if keys[pygame.K_UP] and self.rect.top > 0:
                self.rect.move_ip(0, -self.speed)
            if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
                self.rect.move_ip(0, self.speed)
            if keys[pygame.K_ESCAPE]:
                back_menu_fast()
            if keys[pygame.K_p]:
                paused()
                print("paused")

    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            super(Enemy, self).__init__()
            self.surf = enemy_img
            self.rect = self.surf.get_rect(
                center = (
                    random.randint(WIDTH + 20, WIDTH + 80),
                    random.randint(60, HEIGHT - 60)
                )
            )
            self.speed = random.randint(5, 20)

        def update(self):
            self.rect.move_ip(-self.speed, 0)
            if self.rect.right < 0:
                self.kill()

    class Powerup(pygame.sprite.Sprite):
        POWERUP_MAP = {
                    "p1": (powerup1),
                    "p2": (powerup2),
                    "p3": (powerup3)
                    }
        def __init__(self, p_type):
            super(Powerup, self).__init__()
            self.surf = self.POWERUP_MAP[p_type]
            self.rect = self.surf.get_rect(
                center = (
                    random.randint(WIDTH + 20, WIDTH + 100),
                    random.randint(20, HEIGHT-160)
                )
            )
            self.speed = random.randint(5, 20)
            self.p_type = p_type

        def update(self):
            self.rect.move_ip(-self.speed, 0)
            if self.rect.right < 0:
                self.kill()

    player1 = Player1()
    player2 = Player2()
    enemies = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player1)
    all_sprites.add(player2)

    health1 = 200
    health2 = 200
    
    run = True
    lobby = False

    while run:
        clock.tick(60)
        screen.blit(bg, (i, 0))
        screen.blit(bg, (2730 + i, 0))

        if i == -2730:
            screen.blit(bg, (2730 + i, 0))
            i = 0
        i -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lobby = True
            if event.type == ADDENEMY:
                enemy = Enemy()
                enemies.add(enemy)
                all_sprites.add(enemy)
            if event.type == ADDPOWERUP:
                powerup = Powerup(random.choice(["p1", "p2", "p3"]))
                powerups.add(powerup)
                all_sprites.add(powerup)

        keys = pygame.key.get_pressed()
        player1.update(keys)
        player2.update(keys)
        enemies.update()
        powerups.update()

        for enemy in enemies:
            if pygame.Rect.colliderect(player1.rect, enemy.rect):
                menu_lobby.collision_shell()
                enemy.kill()
                health1 -= 40

        for enemy in enemies:
            if pygame.Rect.colliderect(player2.rect, enemy.rect):
                menu_lobby.collision_shell()
                enemy.kill()
                health2 -= 40
        
        for powerup in powerups:
            if pygame.Rect.colliderect(player1.rect, powerup.rect):
                menu_lobby.collision_powerup()
                powerup.kill()
                if health1 < 200:
                    health1 += 20

        for powerup in powerups:
            if pygame.Rect.colliderect(player2.rect, powerup.rect):
                menu_lobby.collision_powerup()
                powerup.kill()
                if health2 < 200:
                    health2 += 20
        
        for sprite in all_sprites:
            screen.blit(sprite.surf, sprite.rect)

        #różne warianty na zakończenia, w zależności od wygranego gracza 
        if health1 <= 0:
            lost1 = True

        if health2 <= 0:
            lost2 = True

        if lobby:
            back_menu_fast()

        if lost1:
            screen.blit(lost1_img, (0, 0))
            menu_lobby.lost2_sound()
            with open("assets\player2.txt", "r") as PL1:
                player1 = (PL1.read())
                PL1.close()
            player1_label = font.render(player1, 1, (255, 255, 255))
            print(player1)
            screen.blit(player1_label, (WIDTH/2 - player1_label.get_width()/2, 320))
            pygame.display.update()
            pygame.display.flip()
            back_menu()

        if lost2:
            menu_lobby.lost2_sound()
            screen.blit(lost2_img, (0, 0))
            with open("assets\player1.txt", "r") as PL2:
                player2 = (PL2.read())
                PL2.close()
            player2_label = font.render(player2, 1, (255, 255, 255))
            print(player2)
            screen.blit(player2_label, (WIDTH/2 - player2_label.get_width()/2, 320))
            pygame.display.update()
            pygame.display.flip()
            back_menu()

        screen.blit(pygame.image.load("assets/bluehealthbar.png"), (20, 20))
        pygame.draw.rect(screen, (13, 29, 98), (60, 50, (health1), 20))

        screen.blit(pygame.image.load("assets/redhealthbar.png"), (900, 20))
        pygame.draw.rect(screen, (136, 1, 10), (940, 50, (health2), 20))

        pygame.display.update()
        pygame.display.flip()

    pygame.quit()
