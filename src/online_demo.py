import argparse
import json
import socket
import threading
import pygame

parser = argparse.ArgumentParser()
parser.add_argument("--host", default="127.0.0.1")
parser.add_argument("--port", type=int, default=5055)
parser.add_argument("--name", default="oyuncu")
args = parser.parse_args()

pygame.init()
screen = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 20)

pos = [120, 120]
others = {}
running = True

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((args.host, args.port))


def listener():
    global running
    buf = b""
    while running:
        try:
            data = sock.recv(4096)
            if not data:
                break
            buf += data
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                payload = json.loads(line.decode("utf-8"))
                others.clear()
                others.update(payload)
        except OSError:
            break


threading.Thread(target=listener, daemon=True).start()

while running:
    dt = clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        pos[1] -= 3
    if keys[pygame.K_s]:
        pos[1] += 3
    if keys[pygame.K_a]:
        pos[0] -= 3
    if keys[pygame.K_d]:
        pos[0] += 3

    msg = json.dumps({"name": args.name, "x": pos[0], "y": pos[1]}) + "\n"
    try:
        sock.sendall(msg.encode("utf-8"))
    except OSError:
        running = False

    screen.fill((20, 24, 34))
    pygame.draw.circle(screen, (80, 220, 120), (int(pos[0]), int(pos[1])), 14)
    screen.blit(font.render(f"Sen: {args.name}", True, (255, 255, 255)), (10, 10))

    for name, p in others.items():
        if name == args.name:
            continue
        pygame.draw.circle(screen, (240, 120, 120), (int(p["x"]), int(p["y"])), 14)
        screen.blit(font.render(name, True, (240, 220, 220)), (int(p["x"]) + 12, int(p["y"]) - 12))

    screen.blit(font.render("WASD ile hareket (temel online demo)", True, (220, 220, 220)), (10, 40))
    pygame.display.flip()

sock.close()
pygame.quit()
