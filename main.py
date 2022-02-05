import pygame
import os
import sys
from random import randint
import json

pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def colide(her, group):
    z = her.pseudorect
    #print(z, her.rect)
    c = []
    for i in group:
        if z.colliderect(i.rect):
            c.append(i)
    return c

def pseudo(r):
    y, x = r.top, r.left
    return pygame.Rect(x + 3, y, 44, 50)
class Pole:
    def __init__(self, level):
        self.level = level
        # self.test_init()
        self.update_ = True
        self.pressdbtn = None
        self.update_level()

    def next_level(self):
        self.level += 1
        self.update_level()

    def update_level(self):
        global all_wals, all_sprites
        all_sprites = pygame.sprite.Group()
        all_wals = pygame.sprite.Group()

        if self.level == 'menu':
            self.update_ = False
            self.arr = []
            self.hero = None
            self.respown = None
            self.trigger = None
            self.butns = []
            self.butns.append(Button(300, 200 + 50, 200, 70, contin, 'continue_game'))
            self.butns.append(Button(300, 270 + 50, 200, 70, new_game, 'new_game'))
            self.butns.append(Button(300, 340 + 50, 200, 70, quit, 'quit'))
            return
        if self.level == "edit":
            self.drow = False
            self.item_ojc = []
            self.butns = []
            self.arr = []
            self.obj = None
            self.butns = []
            self.butns.append(Button(0, 0, 50, 50, new_item, "menu"))
            self.butns.append(Button(50, 0, 50, 50, delete_last, "reset"))
            self.butns.append(Button(100, 0, 50, 50, savve, "save"))
            lvl = Level(5)
            self.arr, self.respown, self.trigger = lvl.init()
            self.hero = Charecter(self.respown)
            return
        try:
            lvl = Level(self.level)
        except:
            self.test_init()
            return
        self.update_ = True
        self.arr, self.respown, self.trigger = lvl.init()
        self.hero = Charecter(self.respown)

        self.effects = []

        self.butns = []
        self.butns.append(Button(750, 0, 50, 50, to_menu, 'menu'))
        self.butns.append(Button(700, 0, 50, 50, self.hero.die, 'reset'))

    def test_init(self):
        all_sprites = pygame.sprite.Group()
        all_wals = pygame.sprite.Group()
        self.arr = []
        self.effects = []
        self.butns = []
        self.pressdbtn = None
        self.respown = (200, 500)
        self.finish = (700, 400)
        self.arr.append(Planka(0, 600, 700, 20))
        self.arr.append(Planka(200, 450, 400, 20))
        self.arr.append(Planka(600, 20, 20, 700))
        self.arr.append(Planka(-10, 0, 10, 800))
        self.arr.append(Planka(450, 200, 200, 20))
        self.arr.append(Ship(621, 598 - 40, (700 - 621), 'up'))
        self.arr.append(Ship(599 - 40, 221, 447 - 221, 'left'))
        self.hero = Charecter(self.respown)
        self.trigger = Triger(self.finish)
        self.butns.append(Button(750, 0, 50, 50, to_menu, 'menu'))
        self.butns.append(Button(690, 0, 50, 50, self.hero.die, 'reset'))

    def event_reaction(self, event):
        if self.level == "edit":
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in self.butns:
                    if i.dot(event.pos):
                        self.pressdbtn = i
                        return
                if self.obj is not None:
                    self.item_ojc.append(event.pos)
                    if len(self.item_ojc) == 2:
                        creat_obj(self.obj, self.item_ojc)

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.pressdbtn is not None:
                    self.pressdbtn.unpress()
                    self.pressdbtn = None
            return
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if self.level == 'menu':
                return
            self.hero.react(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event)
            for i in self.butns:
                if i.dot(event.pos):
                    self.pressdbtn = i
                    break
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressdbtn is not None:
                self.pressdbtn.unpress()
                self.pressdbtn = None

    def update(self):
        if self.level == "menu" or self.level == "edit":
            return
        self.hero.update()
        for i in self.effects:
            i.update()
        self.trigger.update()



class Charecter(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        self.imgs = []
        for i in range(1, 6):
            self.imgs.append(load_image(f'{i}.png', colorkey=(255, 255, 255)))
        self.image = self.imgs[0]
        x, y = pos
        self.rect = pygame.Rect(x, y, 50, 50)
        self.pseudorect = pseudo(self.rect)
        # print(self.rect.bottom)
        self.x_move = 0
        self.y_move = 0
        self.mod = 0
        self.num = 0

        self.lpress = False
        self.rpress = False

        self.rat = 1
        self.charge = 0
        self.can_dash = True
        self.cd = 0
        self.dying = False
        self.jump_boost = -100000

        self.can_doble = True

    def react(self, ev):
        # print(ev.key)

        if ev.type == pygame.KEYDOWN:
            if ev.key == 51:
                global fps
                if fps == 60:
                    fps = 5
                    self.die()
                else:
                    fps = 60
            elif ev.key == 50:
                print(self.rect.right)

            elif ev.key == 97 and self.mod != 2:
                self.x_move = -2.5
                self.lpress = True
                self.rat = -1
            # elif ev.key == pygame.K_UP:
            # self.y_move = -5
            elif ev.key == 100 and self.mod != 2:
                self.x_move = 2.5
                self.rpress = True
                self.rat = 1
            # elif ev.key == pygame.K_DOWN:
            # self.y_move = 5
            elif ev.key == 108 and self.mod == 0:
                self.y_move = -7
                self.mod = 1
                self.jump_boost = 0
            elif ev.key == 108 and self.mod == 1 and self.can_doble:
                self.y_move = -7
                self.mod = 1
                self.jump_boost = -70
                self.can_doble = False
                pole.effects.append(Jump_Effect(self.rect.left, self.rect.top))
            elif (ev.key == 59 or ev.key == 1078) and self.can_dash:
                self.mod = 2
                self.can_dash = False
                if self.rat == 1:
                    pole.effects.append(Dash_Effect(self.rect.left, self.rect.top, self.rat))
                else:
                    pole.effects.append(Dash_Effect(self.rect.left - 10, self.rect.top, self.rat))
            else:
                print(ev.key)
        elif ev.type == pygame.KEYUP:
            if ev.key == 97:
                # self.x_move = 0
                self.lpress = False
            # if ev.key == pygame.K_UP:
            # self.y_move = 0
            if ev.key == 100:
                # self.x_move = 0
                self.rpress = False
            # if ev.key == pygame.K_DOWN:
            # self.y_move = 0
            if ev.key == 108 and self.mod == 1:
                self.jump_boost = -100000

    def update(self):

        if pygame.sprite.spritecollide(self, triger, False):
            pole.next_level()
            # try:
            #   pole.next_level()
            # except:
            # pole.test_init()

        self.move()
        self.pseudorect = self.pseudorect.move(self.x_move, self.y_move)
        if self.dying:
            self.tm -= 1
            if self.tm == 0:
                self.die()
                self.dying = False
            else:
                self.next_image("die")
                return

        if self.cd != 0:
            self.cd -= 1
            if self.cd == 0:
                self.can_dash = True

        self.rect = self.rect.move(self.x_move, self.y_move)
        self.num += 1
        if self.x_move == 0:
            if self.rpress == True:
                self.x_move = 5
            if self.lpress == True:
                self.x_move = -5

        # self.image = self.imgs[int(self.num)  % 5]

    # mods
    # 1 = падать
    # 0 = стоять
    # 3 = не двигатся
    # 2 дэш
    def move(self):
        #  Вертикаль
        if self.mod == 1:
            y = self.y_move
            flag = False
            if self.jump_boost >= -140:
                flag = True
            elif y < 9:
                y += 0.7
            if flag:
                self.jump_boost += y
                if self.y_move == 0:
                    self.jump_boost -= 10

            # проверка на косание

            self.pseudorect = self.pseudorect.move(0, y)
            lst_col = colide(self, all_wals)
            self.pseudorect = self.pseudorect.move(0, -y)
            # if касание реакция
            if lst_col:
                if all(map(lambda x: x.is_killing(), lst_col)):
                    # print(11111111)
                    self.dying = True
                    self.tm = 7
                    self.rect = self.rect.move(self.x_move * 2, self.y_move * 2)
                    self.mod = 3
                    # self.die()
                    return
                if y < 0:
                    b = 0
                    for i in lst_col:
                        if i.rect.bottom > b:
                            b = i.rect.bottom

                    y = b - self.pseudorect.top
                else:
                    b = 1000

                    for i in lst_col:

                        if i.rect.top < b:
                            b = i.rect.top

                    # print(b)
                    y = b - self.pseudorect.bottom
                    self.mod = 0
                    pole.effects.append(Fall_Effect(self.rect.left - 10, self.rect.top + y))
                    self.can_doble = True
                # print(b, self.rect.bottom)
                # print(y)
            self.y_move = y

            # непонятные вещи
        elif self.mod == 3:
            self.y_move = 0
        elif self.mod == 0:
            self.pseudorect = self.pseudorect.move(0, 1)
            lst_col = colide(self, all_wals)
            self.pseudorect = self.pseudorect.move(0, -1)
            if lst_col:
                if all(map(lambda x: x.is_killing(), lst_col)):
                    self.dying = True
                    self.tm = 1
                    self.rect = self.rect.move(self.x_move * 2, self.y_move * 2)
                    self.mod = 3
                    return
                self.y_move = 0
            else:
                self.mod = 1
                self.jump_boost = -200
        elif self.mod == 2:
            self.y_move = 0

        # для x
        if self.mod == 1:

            x = self.x_move
            if (self.lpress or self.rpress) and abs(x) < 5:
                x += self.rat / 4
            # print(x)
            if not self.lpress and not self.rpress or abs(x) > 5:
                if x < 0:
                    x += 0.3
                    x = min(0, x)
                elif x > 0:
                    x -= 0.3
                    x = max(0, x)
            self.pseudorect = self.pseudorect.move(x, 0)
            lst_col = colide(self, all_wals)
            self.pseudorect = self.pseudorect.move(-x, 0)

            if lst_col:
                if all(map(lambda x: x.is_killing(), lst_col)):
                    # print(11111111)
                    self.dying = True
                    self.tm = 1
                    self.rect = self.rect.move(self.x_move * 2, self.y_move * 2)
                    self.mod = 3
                    return
                # print(self.rect.right)
                if x < 0:
                    b = 0

                    for i in lst_col:
                        if i.rect.right > b:
                            b = i.rect.right

                    x = b - self.pseudorect.left
                else:
                    b = 1000

                    for i in lst_col:

                        if i.rect.left < b:
                            b = i.rect.left

                    # print(b)
                    x = b - self.pseudorect.right
                    # print(b, self.rect.right)

                # print(b, self.rect.bottom)
                # print(y)
                # print(x)
            self.x_move = x
        elif self.mod == 0:

            x = self.x_move
            if (self.lpress or self.rpress) and abs(x) < 5:
                x += self.rat / 4
            # print(x)
            if not self.lpress and not self.rpress or abs(x) > 5:
                if x < 0:
                    x += 0.5
                    x = min(0, x)
                elif x > 0:
                    x -= 0.5
                    x = max(0, x)

            self.pseudorect = self.pseudorect.move(x, 0)
            lst_col = colide(self, all_wals)
            self.pseudorect = self.pseudorect.move(-x, 0)

            if lst_col:
                if all(map(lambda x: x.is_killing(), lst_col)):
                    # print(11111111)
                    self.dying = True
                    self.tm = 1
                    self.rect = self.rect.move(self.x_move * 2, self.y_move * 2)
                    self.mod = 3
                    return
                # print(self.rect.right)
                if x < 0:
                    b = 0

                    for i in lst_col:
                        if i.rect.right > b:
                            b = i.rect.right

                    x = b - self.pseudorect.left
                else:
                    b = 1000

                    for i in lst_col:

                        if i.rect.left < b:
                            b = i.rect.left

                    # print(b)
                    x = b - self.pseudorect.right
                    # print(b, self.rect.right)

                # print(b, self.rect.bottom)
                # print(y)
                # print(x)
            self.x_move = x
        elif self.mod == 2:
            self.image = self.imgs[2]
            x = DASH_SPEED * self.rat
            self.pseudorect = self.pseudorect.move(x, 0)
            lst_col = colide(self, all_wals)
            self.pseudorect = self.pseudorect.move(-x, 0)
            if lst_col:
                if all(map(lambda x: x.is_killing(), lst_col)):
                    # print(11111111)
                    self.dying = True
                    self.tm = 1
                    self.rect = self.rect.move(self.x_move * 2, self.y_move * 2)
                    self.mod = 3
                    return
                # print(self.rect.right)
                self.mod = 1
                if x < 0:
                    b = 0

                    for i in lst_col:
                        if i.rect.right > b:
                            b = i.rect.right

                    x = b - self.pseudorect.left
                else:
                    b = 1000

                    for i in lst_col:

                        if i.rect.left < b:
                            b = i.rect.left

                    # print(b)
                    x = b - self.pseudorect.right
                    # print(b, self.rect.right)

                # print(b, self.rect.bottom)
                # print(y)
                # print(x)

            if self.mod == 1:
                self.charge = 0
                self.cd = DASH_CD
                self.image = self.imgs[0]

            else:
                if abs(self.charge) > DASH_DISTANS:
                    self.mod = 1
                    self.charge = 0
                    self.cd = DASH_CD
                    self.image = self.imgs[0]
                else:
                    self.charge += x
            self.x_move = x
        elif self.mod == 3:
            self.x_move = 0

    def die(self):
        x, y = pole.respown
        self.rect = pygame.Rect(x, y, 50, 50)
        self.pseudorect = pseudo(self.rect)
        self.mod = 1
        self.x_move = 0
        self.y_move = 0
        self.mod = 0
        self.num = 0
        self.charge = 0
        self.can_dash = True
        self.cd = 0
        self.image = self.imgs[0]
        self.can_doble = True
        for i in pole.effects:
            all_sprites.remove(i)
        pole.effects.clear()

    def next_image(self, mod):
        pass


class Triger(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        triger.add(self)
        self.image = FINISH_IMGS[0]
        self.rect = (*pos, 50, 60)
        self.num = 0

    def update(self):
        self.num += 1
        self.image = FINISH_IMGS[self.num // 10 % 4]


class Button(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, funct, name):
        super().__init__(all_sprites)
        self.funct = funct
        self.rect = pygame.Rect(x1, y1, x2, y2)
        self.arr = [load_image(f'buttons\{name}.png', colorkey=(0, 0, 0))] + [
            load_image(f'buttons\{name}_pressed.png', colorkey=(0, 0, 0))]
        self.image = self.arr[0]

    def dot(self, pos):
        z = self.rect.collidepoint(pos)
        if z:
            self.image = self.arr[1]
        return z

    def unpress(self):
        self.image = self.arr[0]
        self.funct()


class Level:
    def __init__(self, name):

        with open(f'levels\{name}.json', encoding='utf8') as f:
            d = json.load(f)
        self.d = d

    def init(self):
        d = self.d
        arr = []
        respown = ''
        finish = ''
        worlds = []

        for i in d.keys():
            if i == 'plank':
                for j in d[i]:
                    arr.append(Planka(*j))
            elif i == 'respown':
                x, y = d[i]
                respown = (x, y)
            elif i == 'finish':
                x, y = d[i]
                finish = Triger((x, y))
            elif i == "ship":
                for j in d[i]:
                    arr.append(Ship(*j))
            elif i == "nad":
                for j in d[i]:
                    arr.append(Nadps(*j))
        return arr, respown, finish


class Planka(pygame.sprite.Sprite):

    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        all_wals.add(self)
        # sur = pygame.Surface((x2 - x1, y2 - y1))
        self.image = WALL.subsurface(0, 0, x2, y2)
        # drow(self.image, x2, y2)

        # print(WALL)
        self.rect = pygame.Rect(x1, y1, x2, y2)

    def is_killing(self):
        return False


class Ship(Planka):
    def __init__(self, x1, y1, z, nap):
        if nap == 'up':
            y2 = 40
            x2 = z
            super().__init__(x1, y1, x2, y2)
            self.image = SU.subsurface((0, 0, x2, y2))
        elif nap == 'down':
            y2 = 40
            x2 = z
            super().__init__(x1, y1, x2, y2)
            self.image = SD.subsurface((0, 0, x2, y2))
        elif nap == 'left':
            x2 = 40
            y2 = z
            super().__init__(x1, y1, x2, y2)
            self.image = SL.subsurface((0, 0, x2, y2))
        else:
            x2 = 40
            y2 = z
            super().__init__(x1, y1, x2, y2)
            self.image = SR.subsurface((0, 0, x2, y2))

    def is_killing(self):
        return True


class Effect(pygame.sprite.Sprite):
    def __init__(self, x, y, *args):
        super().__init__(all_sprites)
        self.rect = pygame.Rect(x, y, 1, 1)
        self.num = 0
        self.init(x, y, args)

    def init(self, x, y, args):
        pass

    def update(self):
        if self.num == self.limit - 1:
            self.suicide()
            return
        self.image = self.arr[self.num]
        self.num += 1

    def suicide(self):
        pole.effects.remove(self)
        all_sprites.remove(self)


class Dash_Effect(Effect):
    def init(self, x, y, args):
        if args[0] == 1:
            self.limit = 7
            self.arr = DASH_IMGS
            self.image = self.arr[0]
        else:
            self.limit = 14
            self.arr = DASH_IMGS
            self.image = self.arr[7]
            self.num = 7


class Jump_Effect(Effect):
    def init(self, x, y, args):
        self.limit = 11
        self.arr = JUMP_IMGS


class Fall_Effect(Effect):
    def init(self, x, y, args):
        self.limit = 7
        self.arr = FALL_IMGS


class Nadps(pygame.sprite.Sprite):
    def __init__(self, x, y, x1, y1, name):
        super().__init__(all_sprites)
        self.rect = pygame.Rect(x, y, x1, y1)
        self.image = load_image(f'{name}.png', colorkey=(255, 255, 255))


def quit():
    global running
    running = False
    pass


def drow(sur, x, y):
    pygame.draw.rect(sur, (0, 0, 0), (0, 0, x, y), width=1)


def contin():
    with open('save.nhht', encoding='utf8') as f:
        x = json.load(f)['lvl']
    pole.level = x
    pole.update_level()


def new_game():
    d = {}
    d['lvl'] = 1
    with open('save.nhht', 'w', encoding='utf8') as f:
        json.dump(d, f)
    pole.level = 1
    pole.update_level()


def to_menu():
    if True:
        d = {}
        d['lvl'] = pole.level
        with open('save.nhht', 'w', encoding='utf8') as f:
            json.dump(d, f)
    pole.level = "menu"
    pole.update_level()


def new_item():
    a = input('да')
    if a in OBJECTI:
        pole.drowing = True
        pole.obj = a


def creat_obj(a, c):
    global d
    if a == "plank":
        x, y = c[0]
        x2, y2 = c[1]
        pole.arr.append(Planka(x, y, x2 - x, y2 - y))
        z = d.get("plank", [])
        z.append([x, y, x2 - x, y2 - y])
        d["plank"] = z
    elif a == "shipup":
        x, y = c[0]
        x2, y2 = c[1]
        pole.arr.append(Ship(x, y, x2 - x, "up"))
        z = d.get("ship", [])
        z.append([x, y, x2 - x, "up"])
        d["ship"] = z
    elif a == "shipdown":
        x, y = c[0]
        x2, y2 = c[1]
        pole.arr.append(Ship(x, y, x2 - x, "down"))
        z = d.get("ship", [])
        z.append([x, y, x2 - x, "down"])
        d["ship"] = z
    elif a == "shipleft":
        x, y = c[0]
        x2, y2 = c[1]
        pole.arr.append(Ship(x, y, y2 - y, "left"))
        z = d.get("ship", [])
        z.append([x, y, y2 - y, "left"])
        d["ship"] = z
    elif a == "shipright":
        x, y = c[0]
        x2, y2 = c[1]
        pole.arr.append(Ship(x, y, y2 - y, "right"))
        z = d.get("ship", [])
        z.append([x, y, y2 - y, "right"])
        d["ship"] = z

    pole.obj = None
    pole.item_ojc = []


def delete_last():
    a = pole.arr.pop()
    all_wals.remove(a)
    all_sprites.remove(a)
    if a.__class__ == Ship:
        d["ship"] = d["ship"][:-1]
    elif a.__class__ == Planka:
        d["plank"] = d["plank"][:-1]


def savve():
    global d
    with open('1.file', 'w', encoding='utf8') as f:
        json.dump(d, f)


if __name__ == "__main__":

    running = True
    mod = 0
    width, height = 800, 700
    size = width, height
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Игра the game")
    pygame.display.set_icon(load_image('1.png', colorkey=(255,255,255)))
    ZASTAVKA = load_image("ZASTAVKA.png")
    screen.blit(ZASTAVKA, (0, 0))
    pygame.display.flip()

    DASH_SPEED = 10
    DASH_DISTANS = 80
    DASH_CD = 30
    DASH_IMGS = [load_image(f'dash\dash{s + 1}.png', colorkey=(255, 255, 255)) for s in range(14)]
    FINISH_IMGS = [load_image(f'finish\\finish{s + 1}.png', colorkey=(0, 0, 0)) for s in range(4)]
    JUMP_IMGS = [load_image(f'jump\{s + 1}.png', colorkey=(255, 255, 255)) for s in range(11)]
    FALL_IMGS = [load_image(f'fall\{s + 1}.png', colorkey=(255, 255, 255)) for s in range(7)]
    WALL = load_image('wall.png')
    ZAD = [load_image('zadnik.png')]
    SL = load_image('ship_left.png', colorkey=(255, 255, 255))
    SR = load_image('ship_right.png', colorkey=(255, 255, 255))
    SU = load_image('ship_up.png', colorkey=(255, 255, 255))
    SD = load_image('ship_down.png', colorkey=(255, 255, 255))
    OBJECTI = ['plank', 'shipup', 'spawn', 'finish', "shipdown", "shipleft", "shipright"]
    musor = []
    d = {}

    all_sprites = pygame.sprite.Group()
    all_wals = pygame.sprite.Group()
    triger = pygame.sprite.GroupSingle()

    pole = Pole("menu")

    clock = pygame.time.Clock()
    fps = 60
    ticks = 59
    clock.tick(1)
    while running:
        # ticks += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            else:
                pole.event_reaction(event)
        screen.blit(ZAD[0], (0, 0))  # ticks // 60 % 1
        pole.update()
        all_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
