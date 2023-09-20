import random


class TicTacToe:
    FREE_CELL = 0
    HUMAN_X = 1
    COMPUTER_O = 2
    def __init__(self):
        self.pole = tuple([tuple([Cell(0) for _ in range(3)]) for _ in range(3)]) # свободное поле 3х3
        self.step = 0
        self._hum = self.is_human_win
        self._com = self.is_computer_win
        self._dr = self.is_draw

    def __getitem__(self, item):
        if not isinstance(item[0], int) or not isinstance(item[1], int) or not 0 <= item[0] <= 2 or not 0 <= item[1] <= 2:
            raise IndexError('некорректно указанные индексы')
        return self.pole[item[0]][item[1]].value

    def __setitem__(self, item, value):
        if not isinstance(item[0], int) or not isinstance(item[1], int) or not 0 <= item[0] <= 2 or not 0 <= item[1] <= 2:
            raise IndexError('некорректно указанные индексы')
        if bool(self):
            self.pole[item[0]][item[1]].value = value



    def init(self):
        self.pole = tuple([tuple([Cell(0) for _ in range(3)]) for _ in range(3)])
        self.step = 0
        self._hum = False
        self._com = False
        self._dr = False

    def show(self):
        for a in self.pole:
            res = [b.value for b in a]
            print(*res)
        print('\n')

    def human_go(self):
        self.F = True
        while self.F:
            self.hum_cord = list(map(int, input().split()))
            self.i = self.hum_cord[0]
            self.j = self.hum_cord[1]
            if not isinstance(self.i, int) or not isinstance(self.j, int) or not 0 <= self.i <= 2 or not 0 <= self.j <= 2:
                raise IndexError('некорректно указанные индексы')
            elif bool(self.pole[self.i][self.j]):
                self.pole[self.i][self.j].value = self.HUMAN_X
                self.F = bool(self.pole[self.i][self.j])
                self.step += 1

    def computer_go(self):
        self.F = True
        while self.F:
            self.i = random.randint(0, 2)
            self.j = random.randint(0, 2)
            if not isinstance(self.i, int) or not isinstance(self.j, int) or not 0 <= self.i <= 2 or not 0 <= self.j <= 2:
                raise IndexError('некорректно указанные индексы')
            elif bool(self.pole[self.i][self.j]):
                self.pole[self.i][self.j].value = self.COMPUTER_O
                self.F = bool(self.pole[self.i][self.j])
                self.step += 1

    @property
    def is_human_win(self):
        for a in self.pole:
            self.line = [b.value for b in a]
            if self.line.count(self.HUMAN_X) == 3:
                return True
        for i in range(3):
            self.line = [b[i].value for b in self.pole]
            if self.line.count(self.HUMAN_X) == 3:
                return True
        self.line = []
        for i, a in enumerate(self.pole):
            self.line.append(a[i].value)
            if self.line.count(self.HUMAN_X) == 3:
                return True
        self.line = []
        for i, a in enumerate(self.pole):
            self.line.append(a[-1-i].value)
            if self.line.count(self.HUMAN_X) == 3:
                return True
        return False

    @property
    def is_computer_win(self):
        for a in self.pole:
            self.line = [b.value for b in a]
            if self.line.count(self.COMPUTER_O) == 3:
                return True
        for i in range(3):
            self.line = [b[i].value for b in self.pole]
            if self.line.count(self.COMPUTER_O) == 3:
                return True
        self.line = []
        for i, a in enumerate(self.pole):
            self.line.append(a[i].value)
            if self.line.count(self.COMPUTER_O) == 3:
                return True
        self.line = []
        for i, a in enumerate(self.pole):
            self.line.append(a[-1 - i].value)
            if self.line.count(self.COMPUTER_O) == 3:
                return True
        return False

    @property
    def is_draw(self):
        if self.step == 9 and self._hum == False and self._com == False:
            return True
        return False

    def __bool__(self):
        if self.step == 9 or self.is_human_win or self.is_computer_win or self.is_draw:
            return False
        return True




class Cell():
    def __init__(self, *args):
        self.value = 0 if len(args) == 0 else args[0] # 0 - клетка свободна; 1 - стоит крестик; 2 - стоит нолик.

    def __bool__(self):
        if self.value == 0:
            return True
        return False




game = TicTacToe()
game.init()
step_game = 0
while game:
    game.show()

    if step_game % 2 == 0:
        game.human_go()
    else:
        game.computer_go()

    step_game += 1


game.show()

if game.is_human_win:
    print("Поздравляем! Вы победили!")
elif game.is_computer_win:
    print("Все получится, со временем")
else:
    print("Ничья.")