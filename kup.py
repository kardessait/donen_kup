import math
import time
import os
import shutil

chars = " .:-=+*#%@"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_size():
    size = shutil.get_terminal_size()
    return size.columns, size.lines

def rotate(x, y, z, ax, ay):
    y2 = y * math.cos(ax) - z * math.sin(ax)
    z2 = y * math.sin(ax) + z * math.cos(ax)

    x2 = x * math.cos(ay) - z2 * math.sin(ay)
    z3 = x * math.sin(ay) + z2 * math.cos(ay)

    return x2, y2, z3

def project(x, y, z, width, height, scale):
    z += 6
    f = scale / z
    x = int(x * f + width / 2)
    y = int(y * f + height / 2)
    return x, y, z

ax = 0
ay = 0

while True:
    width, height = get_size()

    # küp boyutunu terminale göre ayarla
    scale = min(width, height) * 1.2

    screen = [[" " for _ in range(width)] for _ in range(height)]
    zbuffer = [[float('inf') for _ in range(width)] for _ in range(height)]

    step = 0.3  # çözünürlük (küçük = daha detaylı)

    rng = [i * step for i in range(-6, 7)]

    for x in rng:
        for y in rng:

            # ön-arka
            for z in [-2, 2]:
                rx, ry, rz = rotate(x, y, z, ax, ay)
                px, py, depth = project(rx, ry, rz, width, height, scale)

                if 0 <= px < width and 0 <= py < height:
                    if depth < zbuffer[py][px]:
                        zbuffer[py][px] = depth
                        shade = int((1 / depth) * 15)
                        shade = max(0, min(len(chars)-1, shade))
                        screen[py][px] = chars[shade]

            for z in rng:
                for face in [-2, 2]:

                    # x sabit
                    rx, ry, rz = rotate(face, y, z, ax, ay)
                    px, py, depth = project(rx, ry, rz, width, height, scale)
                    if 0 <= px < width and 0 <= py < height:
                        if depth < zbuffer[py][px]:
                            zbuffer[py][px] = depth
                            shade = int((1 / depth) * 15)
                            shade = max(0, min(len(chars)-1, shade))
                            screen[py][px] = chars[shade]

                    # y sabit
                    rx, ry, rz = rotate(x, face, z, ax, ay)
                    px, py, depth = project(rx, ry, rz, width, height, scale)
                    if 0 <= px < width and 0 <= py < height:
                        if depth < zbuffer[py][px]:
                            zbuffer[py][px] = depth
                            shade = int((1 / depth) * 15)
                            shade = max(0, min(len(chars)-1, shade))
                            screen[py][px] = chars[shade]

    clear()
    for row in screen:
        print("".join(row))

    ax += 0.05
    ay += 0.03
    time.sleep(0.03)