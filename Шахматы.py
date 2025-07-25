from abc import ABC, abstractmethod

class ChessPiece (ABC):
    """
    Создание абстрактного класса, которые включает в себя общие методы для шахматных фигур
    """
    def __init__(self, color: str, initial_x: int, initial_y: int) -> None:
        """
        Создание и проверка наличие фигуры заданного цвета на заданных координатах:
        При наличии фигуры выдает пользователю сообщение: "Ожидание хода"
        При отсутствии фигуры выдает пользователю сообщение: "Фигура не определена"

        :param color: str: цвет фигуры, которую нужно передвинуть
        :param initial_x: int: координаты по оси x
        :param initial_y: int: координаты по оси y
        """
        self.color=color
        self.initial_x = initial_x # исходные координаты
        self.initial_y = initial_y # исходные координаты
        self.figure = "Пешка"  # определяем тип фигуры (не всегда правильно, но сходить не даст)
        for figure in ChessBoard.x[self.color]:
            for location in ChessBoard.x[self.color][figure]:
                if location == self.coordinates():
                    self.figure = figure
        if self.figure != 0 and (initial_x, self.initial_y) in ChessBoard.x[self.color][self.figure]:
            print("Ожидание хода")
        else:
            print("Фигура не определена")

    def coordinates(self) -> tuple[int, int]:
        """
        Метод, который возвращает координаты
        :return: tuple[int, int]: Начальные координаты фигуры
        """
        return self.initial_x, self.initial_y

    @abstractmethod
    def current_movements(self) -> None: #к сожалению не учитывает ситуацию, если путь преграждает другая фигура
        """
        Метод Абстрактного класса, который возвращает координаты, куда можно переместить фигуру.
        Выдает пользователю перечень возможных ходов в формате (x, y)
        """
        text: list[tuple[int, int]] = []
        for i in self.get_possible_moves():
            if 1 <= i[0] + self.initial_x <= 8 and 1 <= i[1] + self.initial_y <= 8:
                if (i[0] + self.initial_x, i[1] + self.initial_y) not in [n for i in ChessBoard.x[self.color] for n in ChessBoard.x[self.color][i]]:
                    text.append((i[0] + self.initial_x, i[1] + self.initial_y))
        print(f"Возможные ходы: {", ".join(str(x) for x in text)}")

    @abstractmethod
    def get_possible_moves(self) -> list[int]:
        """
        Метод Абстрактного класса, который возвращает список координат, куда ходит фигура.
        :return: list[int]: список координат, на которые фигура может перемещаться
        """
        pass

    #метод ниже подходит для всего, кроме пешек (для них сделал немного другой)
    @abstractmethod
    def check(self, x: int, y: int) -> None:
        """
        Метод Абстрактного класса, который принимает координаты, куда должна переместиться фигура,
        и отвечает за возможность хода в следующей последовательности:
        1. Определяет, что на введенных координатах не находится фигура такого же цвета
        2. На начальных координатах есть фигура заданного цвета
        3. Начальные и конечные координаты отличаются
        4. Конечные координаты находятся на игровой доске
        5. Выбранная фигура может переместиться на заданные координаты
        При несоблюдении хотя бы 1 пункта выдает сообщение: "Данный ход невозможен"
        Если все пункты выше выполняются, координаты фигуры меняются и происходит следующая проверка:
        1. Если фигура перемещается на пустую ячейку, будет выдано сообщение "Фигура перемещена"
        2. Если на конечной ячейке есть вражеская фигура, она будет уничтожена. Будет выдано сообщение "Фигура уничтожена"
        3. Если уничтоженная фигура вражеский король, будет выдано сообщение: "Игра окончена! Победили {Цвет победителя}"
        :param x: int: координаты по оси x, куда нужно переместить фигуру
        :param y: int: координаты по оси y, куда нужно переместить фигуру
        """
        number_occurrences: int = 0  # определяем, что на ячейке куда нужно встать - не стоит наша фигура
        for figure in ChessBoard.x[self.color]:
            for location in ChessBoard.x[self.color][figure]:
                if location == (x, y):
                    number_occurrences += 1
        if self.color == "Белые":
            enemy: str = "Черные"
        if self.color == "Черные":
            enemy: str = "Белые"
            # доп проверка, что фигурой можно сходить (на начальной ячейке есть такая фигура, на конечной ячейке нет дружественной фигуры, начальная и конечная ячейка не одна и та же, конечное место находится на поле)
        if self.coordinates() in ChessBoard.x[self.color][self.figure] and number_occurrences == 0 and self.coordinates() != (x, y) and 1 <= x <= 8 and 0 <= y <= 8:
            number_steps = (x - self.initial_x, y - self.initial_y)  # вычисляем количество ячеек, на которые сходила фигура
            index = ChessBoard.x[self.color][self.figure].index((self.initial_x, self.initial_y))  # определяем индекс элемента, чтоб потом поменять
            if number_steps in self.get_possible_moves():
                figure_search: str  = " "  # ищем противника!
                for figure in ChessBoard.x[enemy]:
                    for location in ChessBoard.x[enemy][figure]:
                        if location == (x, y):
                            index1 = ChessBoard.x[enemy][figure].index(location)
                            figure_search = ChessBoard.x[enemy][figure][index1]
                            ChessBoard.x[enemy][figure].pop(index1)
                if figure_search != " ":
                    print("Фигура уничтожена")
                    ChessBoard.x[self.color][self.figure][index] = (x, y)  # меняем координаты фигуры
                    if len(ChessBoard.x[enemy]["Король"]) == 0:
                        print(f"Игра окончена! Победили {self.color}")
                else:
                    print("Фигура перемещена")
                    ChessBoard.x[self.color][self.figure][index] = (x, y)  # меняем координаты фигуры
            else:
                print("Данный ход невозможен")
        else:
            print("Данный ход невозможен")

class Pawn(ChessPiece):#пешка
    def get_possible_moves(self):
        #Получается белые пешки идут вверх, а черные пешки расположены сверху и идут вниз. А назад пешки не ходят...
        if self.color == "Белые":
            return ["Ход: (0,1), (0,2). Атака: (1,1), (-1,1)"]
        return ["Ход: (0,-1), (0,-2). Атака: (-1,-1), (1,-1)"]

    def current_movements(self):
        pass

    def check(self, x, y):
        number_occurrences = 0  # определяем, что на ячейке куда нужно встать - не стоит наша фигура
        for figure in ChessBoard.x[self.color]:
            for location in ChessBoard.x[self.color][figure]:
                if location == (x, y):
                    number_occurrences += 1
        if self.color == "Белые":
            enemy = "Черные"
        if self.color == "Черные":
            enemy = "Белые"
        #доп проверка, что фигурой можно сходить (на начальной ячейке есть такая фигура, на конечной ячейке нет дружественной фигуры, начальная и конечная ячейка не одна и та же, конечное место находится на поле)
        if self.coordinates() in ChessBoard.x[self.color]["Пешка"] and number_occurrences == 0 and self.coordinates() != (x, y) and 1<=x<=8 and 0<=y<=8:
            number_steps = (x - self.initial_x, y - self.initial_y) #вычисляем количество ячеек, на которые сходила фигура
            index = ChessBoard.x[self.color]["Пешка"].index((self.initial_x, self.initial_y))#определяем индекс элемента, чтоб потом поменять
            # так как пешки ходят и атакуют по-разному, пытаемся понять правильность хода
            if (self.color == "Белые" and (number_steps == (0,1)) or (self.initial_y == 2 and number_steps == (0,2))) or (self.color == "Черные" and ((number_steps == (0,-1)) or (self.initial_y == 7 and number_steps == (0,-2)))):
                print("Фигура перемещена")
                ChessBoard.x[self.color]["Пешка"][index] = (x, y) # меняем координаты фигуры
            #проверка на ситуацию, когда пешка атакует фигуру противника
            elif (self.color == "Белые" and (number_steps == (1,1) or number_steps == (-1,1))) or (self.color == "Черные" and (number_steps == (-1,-1) or number_steps == (1,-1))):
                figure_search = " " #ищем противника!
                for i in ChessBoard.x[enemy]:
                    for n in ChessBoard.x[enemy][i]:
                        if n == (x, y):
                            index1 = ChessBoard.x[enemy][i].index(n)
                            figure_search = ChessBoard.x[enemy][i][index1]
                            ChessBoard.x[enemy][i].pop(index1)
                if figure_search != " ":
                    print("Фигура уничтожена")
                    ChessBoard.x[self.color]["Пешка"][index] = (x, y) # меняем координаты фигуры
                    if len(ChessBoard.x[enemy]["Король"]) == 0:
                        print(f"Игра окончена! Победили {self.color}")
                else:
                    print("Данный ход невозможен")
            else:
                print("Данный ход невозможен")
        else:
            print("Данный ход невозможен")


class Rook(ChessPiece):#ладья
    def current_movements(self):
        super().current_movements()

    def get_possible_moves(self):
        return [(1,0), (0,1), (-1,0), (0,-1), (2,0), (0,2), (-2,0), (0,-2), (3,0), (0,3), (-3,0), (0,-3),
                (4,0), (0,4), (-4,0), (0,-4), (5,0), (0,5), (-5,0), (0,-5), (6,0), (0,6), (-6,0), (0,-6),
                (7,0), (0,7), (-7,0), (0,-7), (8,0), (0,8), (-8,0), (0,-8)]

    def check(self, x, y):
        super().check(x, y)


class Bishop(ChessPiece):#слон
    def current_movements(self):
        super().current_movements()

    def get_possible_moves(self):
        return [(1, 1), (-1, 1), (1, -1), (-1, -1), (2, 2), (-2, 2), (2, -2), (-2, -2),
                (3, 3), (-3, 3), (3, -3), (-3, -3), (4, 4), (-4, 4), (4, -4), (-4, -4),
                (5, 5), (-5, 5), (5, -5), (-5, -5), (6, 6), (-6, 6), (6, -6), (-6, -6),
                (7, 7), (-7, 7), (7, -7), (-7, -7), (8, 8), (-8, 8), (8, -8), (-8, -8)]

    def check(self, x, y):
        super().check(x, y)


class Horse(ChessPiece):#конь
    def current_movements(self):
        super().current_movements()

    def get_possible_moves(self):
        return [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]

    def check(self, x, y):
        super().check(x, y)


class Queen(ChessPiece):#ферзь
    def get_possible_moves(self):
        return [(1, 1), (-1, 1), (1, -1), (-1, -1), (2, 2), (-2, 2), (2, -2), (-2, -2), (3, 3), (-3, 3), (3, -3),
                (-3, -3), (4, 4), (-4, 4), (4, -4), (-4, -4), (5, 5), (-5, 5), (5, -5), (-5, -5), (6, 6), (-6, 6),
                (6, -6), (-6, -6), (7, 7), (-7, 7), (7, -7), (-7, -7), (8, 8), (-8, 8), (8, -8), (-8, -8), (1,0),
                (0,1), (-1,0), (0,-1), (2,0), (0,2), (-2,0), (0,-2), (3,0), (0,3), (-3,0), (0,-3), (4,0), (0,4),
                (-4,0), (0,-4), (5,0), (0,5), (-5,0), (0,-5), (6,0), (0,6), (-6,0), (0,-6), (7,0), (0,7), (-7,0),
                (0,-7), (8,0), (0,8), (-8,0), (0,-8)]

    def current_movements(self):
        super().current_movements()

    def check(self, x, y):
        super().check(x, y)


class King(ChessPiece):#король
    def get_possible_moves(self):
        return [(1, 1), (-1, 1), (1, -1), (-1, -1), (1,0), (0,1), (-1,0), (0,-1)]

    def current_movements(self):
        super().current_movements()

    def check(self, x, y):
        super().check(x, y)


class ChessBoard:
    """
    В данном классе хранятся шахматные фигуры и их стартовые позиции
    """
    x: dict[str, dict[str, list[tuple]]] = {"Белые":{"Пешка":[(1,2), (2,2), (3,2), (4,2), (5,2), (6,2), (7,2), (8,2)], "Ладья":[(1,1), (8,1)],
        "Слон":[(3,1), (6,1)], "Конь":[(2,1), (8,1)], "Ферзь":[(5,1)], "Король":[(4,1)]},
    "Черные": {"Пешка":[(1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7), (8,7)], "Ладья":[(1,7), (8,7)],
        "Слон":[(3,8), (6,8)], "Конь":[(2,8), (8,8)], "Ферзь":[(5,8)], "Король":[(4,8)]}}

    def info(self) ->None:
        """
        Метод, который выводит оставшиеся шахматные фигуры и их позиции
        При вызове выводит сообщение: "Расположение фигур: " и их координаты
        """
        text: str = "Расположение фигур: "
        for i in self.x:
            text += i + ": "
            for n in self.x[i]:
                text += n + "- "
                for s in self.x[i][n]:
                  text += str(s) + ", "
        print(text[:-2])


#Pawn Пешка   Rook Ладья   Bishop Слон   Horse Сонь   Queen Ферзь   King Король
ChessBoard1 = ChessBoard()
White = Pawn("Белые", 4, 2) # выбираем фигуру, которой хотим сходить
White.check(4, 4) #Прописываем на какие координаты перемещаемся. Белая пешка перемещается с 4:2 на 4:4

black = Pawn("Черные", 4, 7)
black.check(4, 5)

White = Pawn("Белые", 2, 3) # фигура не определена - на данном место нет такой фигуры

White = Pawn("Белые", 2, 2)
White.check(2, 4)

black = Pawn("Черные", 3, 7)
black.check(3, 5)

White = Pawn("Белые", 4, 4)
White.check(3, 5) #убрали черную пешку с (3,5)

black = Horse("Черные", 2, 8)
black.check(4, 7)

White = Bishop("Белые", 3, 1)
White.check(5, 3)

black = Horse("Черные", 4, 7)
black.current_movements()
black.check(3, 5) #убрали белую пешку с (3,5)

White = Bishop("Белые", 5, 3)
White.current_movements()
White.check(3, 5) #убрали черного коня с (3,5)

ChessBoard1.info() #показывает оставшиеся фигуры