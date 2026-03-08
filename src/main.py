import math
import random
import pygame

pygame.init()

W, H = 1100, 700
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Ofisten Kaçış - MVP")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 22)
small = pygame.font.SysFont("arial", 18)

PLAYER_SPEED = 4
BULLET_SPEED = 10
ENEMY_SPEED = 1.6

player = pygame.Vector2(120, 120)
health = 100
has_key = False
car_started = False
escape_done = False

office_walls = [
    pygame.Rect(250, 0, 30, 450),
    pygame.Rect(500, 250, 30, 450),
    pygame.Rect(700, 0, 30, 380),
]

key_rect = pygame.Rect(940, 90, 24, 24)
car_zone = pygame.Rect(860, 540, 180, 120)

enemies = [
    pygame.Vector2(850, 140),
    pygame.Vector2(620, 620),
    pygame.Vector2(390, 120),
]

bullets = []

engine_progress = 0.0


def collide_walls(pos, r=16):
    rect = pygame.Rect(pos.x - r, pos.y - r, r * 2, r * 2)
    return any(rect.colliderect(w) for w in office_walls)


running = True
while running:
    dt = clock.tick(60)
    mx, my = pygame.mouse.get_pos()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and not escape_done:
            dirv = pygame.Vector2(mx - player.x, my - player.y)
            if dirv.length() > 0:
                dirv = dirv.normalize()
                bullets.append([pygame.Vector2(player.x, player.y), dirv])

    keys = pygame.key.get_pressed()
    if not escape_done:
        move = pygame.Vector2(0, 0)
        if keys[pygame.K_w]:
            move.y -= PLAYER_SPEED
        if keys[pygame.K_s]:
            move.y += PLAYER_SPEED
        if keys[pygame.K_a]:
            move.x -= PLAYER_SPEED
        if keys[pygame.K_d]:
            move.x += PLAYER_SPEED
        if move.length() > 0:
            move = move.normalize() * PLAYER_SPEED

        new_pos = player + move
        if 20 < new_pos.x < W - 20 and 20 < new_pos.y < H - 20 and not collide_walls(new_pos):
            player = new_pos

    if key_rect.width > 0 and player.distance_to(pygame.Vector2(key_rect.center)) < 28 and keys[pygame.K_e]:
        has_key = True
        key_rect.width = 0

    in_car = car_zone.collidepoint(player.x, player.y)
    if in_car and has_key and not car_started:
        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
            if keys[pygame.K_i]:
                engine_progress = min(100.0, engine_progress + 1.1)
            else:
                engine_progress = max(0.0, engine_progress - 0.3)
        else:
            engine_progress = max(0.0, engine_progress - 1.0)

        if engine_progress >= 100.0:
            car_started = True

    if car_started and in_car:
        escape_done = True

    for b in bullets:
        b[0] += b[1] * BULLET_SPEED

    bullets = [b for b in bullets if 0 <= b[0].x <= W and 0 <= b[0].y <= H]

    for enemy in enemies[:]:
        vec = player - enemy
        if vec.length() > 0:
            enemy += vec.normalize() * ENEMY_SPEED

        if enemy.distance_to(player) < 18 and not escape_done:
            health -= 0.08 * (dt / 16.6)

        for b in bullets[:]:
            if enemy.distance_to(b[0]) < 18:
                enemies.remove(enemy)
                bullets.remove(b)
                break

    screen.fill((16, 18, 26))

    for w in office_walls:
        pygame.draw.rect(screen, (60, 70, 90), w)

    pygame.draw.rect(screen, (40, 40, 40), car_zone)
    pygame.draw.rect(screen, (100, 120, 120), car_zone, 2)
    car_text = small.render("Fiat Egea 1.6", True, (220, 220, 220))
    screen.blit(car_text, (car_zone.x + 30, car_zone.y + 10))

    if key_rect.width > 0:
        pygame.draw.rect(screen, (240, 200, 40), key_rect)
        screen.blit(small.render("Araba Anahtarı", True, (240, 220, 140)), (key_rect.x - 24, key_rect.y - 24))

    pygame.draw.circle(screen, (70, 160, 255), (int(player.x), int(player.y)), 14)
    for enemy in enemies:
        pygame.draw.circle(screen, (220, 60, 60), (int(enemy.x), int(enemy.y)), 14)

    for b in bullets:
        pygame.draw.circle(screen, (255, 240, 120), (int(b[0].x), int(b[0].y)), 4)

    hud = [
        f"Can: {max(0, int(health))}",
        f"Anahtar: {'VAR' if has_key else 'YOK'}",
        f"Dusman: {len(enemies)}",
    ]
    for i, t in enumerate(hud):
        screen.blit(font.render(t, True, (235, 235, 235)), (18, 18 + i * 28))

    if not has_key:
        msg = "Ofisten cikis icin araba anahtarini bul!"
    elif not in_car:
        msg = "Anahtari aldin. Otoparktaki araca git."
    elif not car_started:
        msg = "Araba calistir: CTRL (debriyaj) + I (kontak)"
    else:
        msg = "KACIS BASARILI!"

    screen.blit(font.render(msg, True, (255, 220, 120)), (18, H - 36))

    if in_car and has_key and not car_started:
        pygame.draw.rect(screen, (30, 30, 30), (W - 300, 20, 260, 80))
        pygame.draw.rect(screen, (180, 180, 180), (W - 300, 20, 260, 80), 2)
        pygame.draw.rect(screen, (80, 200, 120), (W - 280, 60, int(engine_progress * 2.2), 20))
        screen.blit(small.render("Kontak Gecisi / Devir", True, (240, 240, 240)), (W - 280, 32))

    if health <= 0:
        screen.blit(font.render("OLDUN! Tekrar dene.", True, (255, 90, 90)), (W // 2 - 100, H // 2))

    pygame.display.flip()

pygame.quit()
