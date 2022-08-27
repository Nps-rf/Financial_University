class Stack(object):
    """Условие:
    Создать класс стек.
    Использовать способ реализации стека через list.
    Поменять местами первый и последний элементы стека.
    """
    __data = list()

    def __str__(self): return f'Stack object: {str(self.__data)}'

    def add(self, element): self.__data.append(element)

    def get(self) -> object: return self.__data.pop(-1)


stack = Stack()
stack.add(1)
stack.add(2)
a = stack.get()
b = stack.get()
stack.add(a)
stack.add(b)
print(stack)
