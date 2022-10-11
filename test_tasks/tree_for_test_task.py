# ЗАДАНИЕ
# Есть массив объектов, которые имеют поля id и parent, через которые их можно связать в дерево и некоторые произвольные поля.
#
# Нужно написать класс, который принимает в конструктор массив этих объектов и реализует 4 метода:
#   - getAll() Должен возвращать изначальный массив элементов.
#   - getItem(id) Принимает id элемента и возвращает сам объект элемента;
#   - getChildren(id) Принимает id элемента и возвращает массив элементов, являющихся дочерними для того элемента,
#  чей id получен в аргументе. Если у элемента нет дочерних, то должен возвращаться пустой массив;
#   - getAllParents(id) Принимает id элемента и возвращает массив из цепочки родительских элементов,
#  начиная от самого элемента, чей id был передан в аргументе и до корневого элемента,
#  т.е. должен получиться путь элемента наверх дерева через цепочку родителей к корню дерева. Порядок элементов важен!
#
# Требования: максимальное быстродействие, следовательно, минимальное количество обходов массива при операциях,
#  в идеале, прямой доступ к элементам без поиска их в массиве.

from collections import defaultdict
from copy import deepcopy


class TreeStore:
    def __init__(self, items: list):
        self.nodes = {item['id']: item for item in deepcopy(items)}
        self.children = defaultdict(list)
        for item in self.nodes.values():
            if item['parent'] != 'root':
                self.children[item['parent']].append(item)

    def get_all(self) -> list:
        """
        Возвращает изначальный массив элементов.
        :return: [
            {'id': 1, 'parent': 'root'},
        ]
        """

        return list(self.nodes.values())

    def get_item(self, id: int) -> dict:
        """
        Возвращает объект элемента по его идентификатору.
        :param id: int
        :return: {'id': 7, 'parent': 4, 'type': None}
        """

        return self.nodes[id]

    def get_сhildren(self, id: int) -> list:
        """
        Возвращает массив элементов, являющихся дочерними для того элемента,
        чей идентификатор получен в аргументе.
        :param id: int
        :return: [
            {'id': 7, 'parent': 4, 'type': None},
        ]
        """

        return self.children.get(id, [])

    def get_all_parents(self, id) -> list:
        """
        Возвращает массив из цепочки родительских элементов, начиная от самого
        элемента, чей идентификатор был передан в аргументе и до корневого элемента.
        :param id: int
        :return: [
            {'id': 4, 'parent': 2, 'type': 'test'},
        ]
        """

        parents = []
        node = self.nodes[id]
        while node['parent'] != 'root':
            node = self.nodes[node['parent']]
            parents.append(node)

        return parents


# Исходные данные:
if __name__ == '__main__':
    items = [
        {'id': 1, 'parent': 'root'},
        {'id': 2, 'parent': 1, 'type': 'test'},
        {'id': 3, 'parent': 1, 'type': 'test'},
        {'id': 4, 'parent': 2, 'type': 'test'},
        {'id': 5, 'parent': 2, 'type': 'test'},
        {'id': 6, 'parent': 2, 'type': 'test'},
        {'id': 7, 'parent': 4, 'type': None},
        {'id': 8, 'parent': 4, 'type': None}
    ]

    ts = TreeStore(items)

    # Примеры использования:
    get_all = ts.get_all()
    # get_all = [
    #     {'id': 1, 'parent': 'root'},
    #     {'id': 2, 'parent': 1, 'type': 'test'},
    #     {'id': 3, 'parent': 1, 'type': 'test'},
    #     {'id': 4, 'parent': 2, 'type': 'test'},
    #     {'id': 5, 'parent': 2, 'type': 'test'},
    #     {'id': 6, 'parent': 2, 'type': 'test'},
    #     {'id': 7, 'parent': 4, 'type': None},
    #     {'id': 8, 'parent': 4, 'type': None}
    # ]

    get_item = ts.get_item(7)
    # get_item = {'id': 7, 'parent': 4, 'type': None}

    get_сhildren = ts.get_сhildren(4)
    # get_сhildren = [
    #     {'id': 7, 'parent': 4, 'type': None},
    #     {'id': 8, 'parent': 4, 'type': None}
    # ]

    get_all_parents = ts.get_all_parents(7)
    # get_all_parents = [
    #     {'id': 4, 'parent': 2, 'type': 'test'},
    #     {'id': 2, 'parent': 1, 'type': 'test'},
    #     {'id': 1, 'parent': 'root'}
    # ]

    print('exit')
