import scipy.misc
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pygame
from PIL import Image
import matplotlib.pyplot as plt


white = (255, 255, 255)
w = 800
h = 800
black = (0, 0, 0)
b_x = 0
b_y = 0
d1 = []
d2 = []
gr=[]
r=[]
g=[]
b=[]


def move_line():
    global y_m
    d1[1] = y_m
    d2[1] = y_m


def draw_grath():
    im = scipy.misc.imread(filename, flatten=False, mode='RGB')
    img = Image.open(filename)
    for i in range(img.size[0]):
        m= list(im[d1[0]][i])
        r.append(m[0])
        g.append(m[1])
        b.append(m[2])
    plt.plot(r, 'r')
    plt.plot(g, 'g')
    plt.plot(b, 'b')
    plt.show()







filename = askopenfilename()
img = Image.open(filename)
if img.size[0] > img.size[1]:
    new_width = 780
    new_height = int(780 * img.size[1] / img.size[0])
    b_x = 10
    b_y = int((800 - new_height) / 2)
    d1 = [b_x, 400]
    d2 = [b_x + new_width, 400]
    max_d = [b_y, b_y + new_height]
else:
    new_height = 780
    new_width = int(780 * img.size[0] / img.size[1])
    b_y = 10
    b_x = int((800 - new_width) / 2)
    d1 = [b_x, 400]
    d2 = [b_x + new_width, 400]
    max_d = [b_y, b_y + new_height]
img = img.resize((new_width, new_height), Image.ANTIALIAS)
mode = img.mode
size = img.size
data = img.tobytes()
img_p = pygame.image.fromstring(data, size, mode)
screen = pygame.display.set_mode((w, h))
screen.fill(white)
done = False
clock = pygame.time.Clock()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] == 1:
                if ((d1[1] - 5) < y_m < (d1[1] + 5)) and (d1[0] < x_m < d2[0]):
                    line_d = 1
            if pygame.mouse.get_pressed()[1] == 1:
                draw_grath()
    screen.fill(white)
    x_m, y_m = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0] == 0:
        line_d = 0
    if line_d == 1 and max_d[0] < d1[1] < max_d[1]:
        move_line()
    screen.blit(img_p, (b_x, b_y))
    if d1[1] > max_d[1] - 5:
        d1[1] = max_d[1] - 5
        d2[1] = max_d[1] - 5
    elif d1[1] < max_d[0] + 5:
        d1[1] = max_d[0] + 5
        d2[1] = max_d[0] + 5
    pygame.draw.line(screen, black, [d1[0], d1[1]], [d2[0], d2[1]], 2)
    pygame
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
