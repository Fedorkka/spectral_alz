from tkinter import *
from tkinter import ttk
import scipy.misc
from tkinter.filedialog import askopenfilename
import pygame
from PIL import Image
import matplotlib.pyplot as plt


global d1, d2
white = (255, 255, 255)
w = 800
h = 800
black = (0, 0, 0)
b_x = 0
b_y = 0
d1 = []
d2 = []
cr=[]
cb=[]
cg=[]
gr = []
r = []
g = []
b = []




def main_menu():
    global root, screen_width, screen_height
    root = Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry('600x400'+'+'+str(int(screen_width/2)-300)+"+"+str(int(screen_height/2)-400))
    s = ttk.Style()
    s1 = ttk.Style()
    s.configure('my.TButton', font=('Arial', 30))
    s1.configure('my.TLabel', font=('Arial', 30))
    lb_h = ttk.Label(root, text="Анализатор спекстра", style='my.TLabel').place(x=100, y=20)
    upload = ttk.Button(root, text="Загрузить изображение", style='my.TButton', command=open_img).place(x=70, y=100)
    calibrate = ttk.Button(root, text="Калибровка", style='my.TButton').place(x=170, y=190)
    root.mainloop()


def move_line(line):
    global d1, d2, cr, cb, cg
    x_m, y_m = pygame.mouse.get_pos()
    if line== "black":
        d1[1] = y_m
        d2[1] = y_m


def crop_img(img):
    global d1, d2, max_d
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
    return new_width, new_height, b_x, b_y


def open_img():
    global d1, d2, root, filename, max_d
    root.withdraw()
    filename = askopenfilename()
    img = Image.open(filename)
    new_width, new_height, b_x, b_y = crop_img(img)
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
                        color= "black"
                if pygame.mouse.get_pressed()[1] == 1:
                    draw_graph(color)
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
        pygame.display.flip()
        clock.tick(60)
    root.deiconify()
    pygame.quit()


def calibrate():

    global d1, d2, root, filename, max_d
    root.withdraw()
    filename = askopenfilename()
    img = Image.open(filename)
    new_width, new_height, b_x, b_y = crop_img(img)
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
                if pygame.mouse.get_pressed()[0] == 1:
                    if ((cr[1] - 5) < x_m < (cr[1] + 5)) and (cr[0] < y_m < cr[0]):
                        line_d = 1
                        color = "red"
                if pygame.mouse.get_pressed()[1] == 1:
                    draw_graph()
        screen.fill(white)
        x_m, y_m = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == 0:
            line_d = 0
        if line_d == 1 and max_d[0] < cr[1] < max_d[1]:
            move_line(color)
        screen.blit(img_p, (b_x, b_y))
        if d1[1] > max_d[1] - 5:
            d1[1] = max_d[1] - 5
            d2[1] = max_d[1] - 5
        elif d1[1] < max_d[0] + 5:
            d1[1] = max_d[0] + 5
            d2[1] = max_d[0] + 5
        pygame.draw.line(screen, black, [d1[0], d1[1]], [d2[0], d2[1]], 2)
        pygame.display.flip()
        clock.tick(60)
    root.deiconify()
    pygame.quit()


def draw_graph():


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

main_menu()
