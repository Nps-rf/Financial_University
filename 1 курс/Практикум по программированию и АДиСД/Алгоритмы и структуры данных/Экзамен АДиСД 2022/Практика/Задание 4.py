import random
from copy import deepcopy


class StackType(object):
    def __init__(self): ...

    def __str__(self): ...

    def __len__(self): ...

    def add(self, element): ...

    def get(self): ...

    def copy(self): ...


class Stack(object):
    """Условие:
    4.	Создать класс стек.
    Использовать способ реализации стека через list.
    Удалить элемент, который находится в середине стека,
    если нечетное число элементов, а если четное, то два средних.
    """
    __data = list()

    def __init__(self, data=None):
        if data is not None:
            self.__data = data

    def __str__(self): return f'Stack object: {str(self.__data)}'

    def __len__(self): return len(self.__data)

    def add(self, element): self.__data.append(element)

    def get(self) -> object: return self.__data.pop(-1)

    def copy(self) -> StackType: return Stack(deepcopy(self.__data))

    def middle_pop(self):
        item = self
        procedural_list = []
        if (cur_len := len(item)) % 2 != 0:
            while len(item) != cur_len // 2:
                procedural_list.append(item.get())
            for elem in reversed(procedural_list[:-1]):
                item.add(elem)
        else:
            while len(item) != cur_len // 2 - 1:
                procedural_list.append(item.get())
            for elem in reversed(procedural_list[:-2]):
                item.add(elem)


def middle_pop(item: Stack) -> Stack:
    item = item.copy()
    procedural_list = []
    if (cur_len := len(item)) % 2 != 0:
        while len(item) != cur_len // 2:
            procedural_list.append(item.get())
        for elem in reversed(procedural_list[:-1]):
            item.add(elem)
    else:
        while len(item) != cur_len // 2 - 1:
            procedural_list.append(item.get())
        for elem in reversed(procedural_list[:-2]):
            item.add(elem)
    return item


if __name__ == "__main__":
    stack = Stack()
    for _ in range(8):
        stack.add(random.randint(0, 20))
    print(stack)
    new_stack = middle_pop(stack)
    stack.middle_pop()
    print(new_stack, stack)
