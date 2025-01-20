class Stack:
    def __init__(self):
        self.items: list = []

    def is_empty(self) ->int or float:
        if self.items[0] % 1 == 0:
            return int(self.items[0])
        else:
            return self.items[0]

    def push(self, item: float):
        self.items.append(item)

    def pop(self, operator: str):
        actions: dict[str, list] = {"+": [self.items[-2] + self.items[-1]], "-": [self.items[-2] - self.items[-1]],
        "*": [self.items[-2] * self.items[-1]], "/": [self.items[-2] / self.items[-1]]}
        self.items = self.items[:-2] + actions[operator]


def expression(stack, example: str) -> int:
    for i in example.split():
        if i not in "+, -, *, /":
            stack.push(float(i))
            continue
        stack.pop(i)
    return stack.is_empty()

my_stack = Stack()
example: str = "11 2 5 * + 1 3 2 * + 4 - /"
print(expression(my_stack, example))