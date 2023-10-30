from random import randint
from random import choice


class Ship:
    """Представление кораблей"""
    def __init__(self, length, tp=1,  x=None, y=None,):
        self._x = x # x, y - координаты начала расположения корабля (целые числа)
        self._y = y # x, y - координаты начала расположения корабля (целые числа)
        self._length = length # length - длина корабля (число палуб: целое значение: 1, 2, 3 или 4)
        self._tp = tp # tp - ориентация корабля (1 - горизонтальная; 2 - вертикальная)
        self._is_move = True # Движение корабля
        self._cells = [0 for _ in range(self._length)]  # Палубы корабля
        self.all_coord_x = None
        self.all_coord_y = None

    def set_start_coords(self, x, y): #установка стартовой координаты коробля
        self._x = x
        self._y = y

    def get_start_coords(self): #получение стартовой координаты корабля
        return self._x, self._y

    def move(self, go): #(go = 1 - движение в одну сторону на клетку; go = -1 - движение в другую сторону на одну клетку)
        if self._is_move:
            if self._tp == 1:
                self.set_start_coords(self._x+go, self._y) #cмещение стартовой координаты по горизонтали или вертикали
            else:
                self.set_start_coords(self._x, self._y+go)

    def is_collide(self, ship): #проверка на столкновение с другим кораблем ship
        if self._tp == 1: #создание списка множества Х и У палуб у первого корабля
            self.all_coord_x = set(range(self._x, self._x + self._length))
            self.all_coord_y = set(range(self._y, self._y + 1))
        else:
            self.all_coord_x = set(range(self._x, self._x + 1))
            self.all_coord_y = set(range(self._y, self._y + self._length))
        if ship._tp == 1: #создание списка множества Х и У палуб у второго корабля
            self.two_x = set(range(ship._x, ship._x + ship._length))
            self.two_y = set(range(ship._y, ship._y + 1))
        else:
            self.two_x = set(range(ship._x, ship._x + 1))
            self.two_y = set(range(ship._y, ship._y + ship._length))
        # создание списка множества Х и У палуб у первого корабля СЕЛФ. Создаются три псевдо карабля бутербродом.
        # Создаются координаты основного и двух паралельных с обеих сторон от основного, чтобы засечь пересечение по диагонали.
        self.gran = -1
        while self.gran < 2:
            if self._tp == 1:
                self.one_x = set(range(self._x-1, self._x + self._length + 1))
                self.one_y = set(range(self._y + self.gran, (self._y + self.gran) + 1))
            else:
                self.one_x = set(range(self._x + self.gran, (self._x + self.gran) + 1))
                self.one_y = set(range(self._y-1, self._y + self._length + 1))
            self.gran += 1
            if self.one_x & self.two_x and self.one_y & self.two_y: # Проверка вхождения трех псевдо кораблей от СЕЛФА во второй сравниваемый на пересечения.
                return True
        return False

    def is_out_pole(self, size): #проверка на выход корабля за пределы игрового поля (size - размер игрового поля, обычно)
        if self._x in range(size) and self._y in range(size):    #входит ли стартовая точка поле
            if self._tp == 1:
                if (self._x + (self._length-1)) in range(size):    #нахождения края корабля по горизонтали
                    return False
            else:
                if (self._y + (self._length-1)) in range(size):    #нахождения края корабля по вертикали
                    return False
        return True

    def __getitem__(self, item):
        return self._cells[item]

    def __setitem__(self, key, value):
        self._cells[key] = value

    def __setattr__(self, key, value):
        if key == '_cells' and value == 'X':
            self._is_move = False
        object.__setattr__(self, key, value)


class GamePole:
    """Игровое поле"""
    def __init__(self, size=10):
        self._size = size   #размер поля
        self._ships = []    #список кораблей
        self._pole = [['~' for _ in range(self._size)] for _ in range(self._size)]    #Массив с нулями (матрица) чисто поле

    def init(self): #Инициализатор игры. Создание кораблей
        self._ships = [Ship(4, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)),
                       Ship(2, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2))
                       ]
        for i, a in enumerate(self._ships): #Расставляем корабли на поле
            f = True
            while f:
                a._x = randint(0, 9)
                a._y = randint(0, 9)
                if not a.is_out_pole(self._size):   #Задаем Х У координаты и проверяем выходи за пределы поля или нет.
                    f = False
                else:
                    continue
                for b in self._ships[:i+1]: #Проверяем, не сталкивается ли корабль с уже стоящими на поле
                    if a != b and a.is_collide(b):
                        f = True
                        continue
        self.ship_pole()

    def get_ships(self):    #список кораблей
        return self._ships

    def move_ships(self): #движение всех кораблей
        for a in self._ships:  # Движем по одному кораблю, после движения проверяем не сталкивается ли он или выходит за поле
            f = True
            self.a_x = a._x
            self.a_y = a._y
            i = 0
            while f:
                r = choice([-1, 1])
                a.move(r)
                if self.all_collide():
                    f = False
                    continue
                else:
                    a.set_start_coords(self.a_x, self.a_y)
                i += 1
                if i == 10:
                    f = False
        self.ship_pole()

    def show(self):
        self.ship_pole()
        for a in self._pole:
            # b = ' '.join(a)
            print(*a)

    def get_pole(self):
        self.gp = tuple([tuple(a) for a in self._pole])
        return self.gp

    def all_collide(self): # Проверка всего поля на корректность расстановки кораблей
        for a in self._ships:
            if a.is_out_pole(self._size):   # Не выходит ли корабль за пределы поля
                return False
            for b in self._ships: #Проверяем, не сталкивается ли корабль с другими стоящими на поле
                if a != b and a.is_collide(b):
                    return False
        return True # Если проверки прошли - возвращаем тру

    def ship_pole(self):
        if len(self._ships) > 0 and self._ships[0]._x != None:
            self._pole = [['~' for _ in range(self._size)] for _ in range(self._size)]
        for a in self._ships:
            for i, b in enumerate(a._cells):
                if a._tp == 1:
                    self._pole[(a._y)][(a._x) + i] = b
                else:
                    self._pole[(a._y) + i][(a._x)] = b


class SeaBattle:
    """Играем"""
    def __init__(self):
        self.human_me = GamePole(10) #Поле игрока с кораблями
        self.human_comp = GamePole(10) #Поле для отметок, куда игрок стрельнул в сторону компа
        self.comp = GamePole(10)    #Поле компа с кораблями

    def start_game(self):   #Старт игры
        self.human_me.init() #расставляем корабли человека
        self.comp.init()    #расставляем корабли компа
        game_f = True   #Флаг активной игры
        self.winner = 0 # 0-ничья, 1-человек, 2-комп победил


        while game_f:
            self.show_pole()
            self.shot_human() #выстрел человека
            if self.check_win(self.comp): #Проверка на победу человека
                game_f = False
                self.winner = 1
                continue
            self.shot_comp() #Выстрел компа
            if self.check_win(self.human_me): #Проверка на победу компа
                game_f = False
                self.winner = 2
                continue
            self.human_me.move_ships()
            self.comp.move_ships()
        self.show_pole()
        if self.winner == 1:
            print('Поздравляю тебя, Человек! Ты победил бездушную машину!')
        elif self.winner == 2:
            print('Человечество будет порабощено!!! Компьютер обыграл человека! Человек проиграл!')
        elif self.winner == 0:
            print('Я хз как так вообще.моглл получиться, Но тут ничья!')
        print('Конец игры. можете сыграть еще разок =)')

    def show_pole(self):
        print('\n')
        print('Поле сопернрка')
        self.human_comp.show()
        print('\n')
        print('Мое поле')
        self.human_me.show()
        print('\n')


    def shot_human(self):
        print('Твой ход!')
        input_f = True
        while input_f:
            try:
                print('Введите координаты удара ро оси Х, У (целое числоот 0 до 9)')
                x = input('Ось Х. (целое числоот 0 до 9): ')
                y = input('Ось У. (целое числоот 0 до 9): ')
                x = int(x)
                y = int(y)
            except Exception:
                print('Вы ввели неверные данные. попробуйте еще раз!')
            else:
                if 0 <= x <= 9 and 0 <= y <= 9:
                    input_f = False
                    print('Координаты приняты. Рокета пошла!')
        if self.comp._pole[y][x] != 'X':
            if self.comp._pole[y][x] ==  0:
                self.human_comp._pole[y][x] = 'X'
                print("БУМ! БАХ! ВЫ ПОПАЛИ!")
                self.shot_human()
            else:
                print('МИМО!')
        else:
            while self.comp._pole[y][x] == 'X':
                input_f = True
                while input_f:
                    try:
                        print('Введите координаты удара ро оси Х, У (целое числоот 0 до 9)')
                        x = input('Ось Х. (целое числоот 0 до 9): ')
                        y = input('Ось У. (целое числоот 0 до 9): ')
                        x = int(x)
                        y = int(y)
                    except Exception:
                        print('Вы ввели неверные данные. попробуйте еще раз!')
                    else:
                        if 0 <= x <= 9 and 0 <= y <= 9:
                            input_f = False
                            print('Координаты приняты. Рокета пошла!')
                if self.comp._pole[y][x] != 'X':
                    if self.comp._pole[y][x] == 0:
                        self.human_comp._pole[y][x] = 'X'
                        print("БУМ! БАХ! ВЫ ПОПАЛИ!")
                        self.shot_human()
                    else:
                        print('МИМО!')
                    break
        self.check_shot(x, y, self.comp)

    def shot_comp(self):
        print("Ход компьютера.")
        x = randint(0, 9)
        y = randint(0, 9)
        if self.human_me._pole[y][x] != 'X':
            if self.human_me._pole[y][x] == 0:
                print("БУМ! БАХ! Компьютер в тебя ПОПАЛ!")
                self.shot_comp()
            else:
                print('Компьютер выстрелил МИМО!')
        else:
            while self.human_me._pole[y][x] == 'X':
                x = randint(0, 9)
                y = randint(0, 9)
                if self.human_me._pole[y][x] != 'X':
                    if self.human_me._pole[y][x] == 0:
                        print("БУМ! БАХ! Компьютер в тебя ПОПАЛ!")
                        self.shot_comp()
                    else:
                        print('Компьютер выстрелил МИМО!')
                    break
        self.check_shot(x, y, self.human_me)

    def check_shot(self, x, y, player): # ищем корабль в который попали и меняем значение в списке _cells
        for a in player._ships:
            if a._tp == 1:  # создание списка множества Х и У палуб у первого корабля
                a.all_coord_x = set(range(a._x, a._x + a._length))
                self.all_coord_y = set(range(a._y, a._y + 1))
            else:
                a.all_coord_x = set(range(a._x, a._x + 1))
                a.all_coord_y = set(range(a._y, a._y + a._length))
            if set([x]) & a.all_coord_x and set([y]) & a.all_coord_y:
                if a._tp == 1:
                    ind = list(a.all_coord_x).index(x)
                    a._cells[ind] = 'X'
                    a._is_move = False
                else:
                    ind = list(a.all_coord_y).index(y)
                    a._cells[ind] = 'X'
                    a._is_move = False

    def check_win(self, player):    #проверяем список _cells во всех кораблях. Если нулей нет, значит все подбиты, значит победа игрока.
        win_f = True
        for a in player._ships:
            if 0 in a._cells:
                win_f = False
                return win_f
        return win_f



game = SeaBattle()
game.start_game()
