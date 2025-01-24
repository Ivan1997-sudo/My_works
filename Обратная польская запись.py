class Stack:
    def __init__(self):
        self.items: list = []

    def peek(self) -> str or int or float:
        if len(self.items) == 0:
            return "Вводимая строка пуста"
        if len(self.items) > 1:
            return "Недостаточно операторов"
        if self.items[0] % 1 == 0:
            return int(self.items[0])
        return self.items[0]

    def push(self, item: float) -> None:
        self.items.append(item)

    def pop(self, operator: str) -> None:
        try:
            actions: dict[str, list] = {"+": [self.items[-2] + self.items[-1]], "-": [self.items[-2] - self.items[-1]],
            "*": [self.items[-2] * self.items[-1]], "/": [self.items[-2] / self.items[-1]]}
            self.items = self.items[:-2] + actions[operator]
        except ZeroDivisionError:
            print("Делить на 0 нельзя")

def expression(stack, example: str) -> int or str:
    for i in example.split():
        if i not in "+, -, *, /":
            stack.push(float(i))
            continue
        if len(stack.items) < 2 or (i == "/" and stack.items[-1] == 0):
            return f"Одно из действий не может быть выполнено: {i}"
        else:
            stack.pop(i)
    return stack.peek()

my_stack1 = Stack()
example1: str = "11 2 5 * + 1 3 2 * + 4 - /"
print(expression(my_stack1, example1))

my_stack2 = Stack()
example2: str = "11 2 5 * + 1 3 2 * + 0 - /"
print(expression(my_stack2, example2))

my_stack3 = Stack()
example3: str = "4 + 6 -"
print(expression(my_stack3, example3))

my_stack4 = Stack()
example4: str = " "
print(expression(my_stack4, example4))

my_stack5 = Stack()
example5: str = "11 2 5 *"
print(expression(my_stack5, example5))
