from collections import defaultdict


class MissingParentException(Exception):
    """
    Исключение возникает при попытке вставить узел в дерево,
    при отсутсвии искомого родителя.
    """

    def __init__(self, parent):
        self.message = f'Дерево не содержит узла с идентификатором {parent}'
        super().__init__(self.message)


class TreeStore:

    class Node:
        def __init__(self, **kwargs):
            self.children = []
            self.id = kwargs['id']
            self.parent = kwargs['parent']
            self.__dict__.update(kwargs)

        def to_dict(self):
            """
            Возвращает словарь с ключами id, parent, type.
            :return: {'id': 7, 'parent': 4, 'type': None}
            """

            return {
                'id': self.id,
                'parent': self.parent,
                'type': self.type if hasattr(self, 'type') else None
            }

    def __init__(self, items):
        self.adjacency_matrix = defaultdict(list)
        for item in items:
            node = self.Node(**item)
            self.adjacency_matrix[item['id']]
            self.adjacency_matrix[item['parent']].append(node)

        self.root = self.adjacency_matrix['root'][0]
        stack = [self.root]
        while stack:
            node = stack.pop()
            node.children = self.adjacency_matrix[node.id]
            for node in node.children:
                stack.append(node)

    def insert(self, node_value: dict) -> None:
        """
        Выполняет вставку узла.

        :param node_value: {'id': 9, 'parent': 8, 'type': 'test'}
        """

        if node_value['parent'] in self.adjacency_matrix:
            new_node = self.Node(**node_value)
        else:
            raise MissingParentException(node_value['parent'])

        stack = [self.root]
        while stack:
            node = stack.pop()
            if node.id == node_value['parent']:
                node.children.append(new_node)
                self.adjacency_matrix[node.id] = node.children
                break
            for node in node.children:
                stack.append(node)

    def get_all(self):
        """
        Возвращает изначальный массив элементов.

        :return: [
            {'id': 1, 'parent': 'root'},
        ]
        """

        return [
            child.to_dict() for children in self.adjacency_matrix.values()
            for child in children
        ]

    def get_all_by_stack(self):
        """
        Возвращает изначальный массив элементов.

        :return: [
            {'id': 1, 'parent': 'root'},
        ]
        """

        result = []
        stack = [self.root]
        while stack:
            node = stack.pop()
            result.append(node.to_dict())
            for node in node.children:
                stack.append(node)
        return result

    def get_item(self, id: int) -> dict:
        """
        Возвращает объект узла, в виде словаря, по его идентификатору.

        :param id: int
        :return: {'id': 7, 'parent': 4, 'type': None} or None
        """

        stack = [self.root]
        while stack:
            node = stack.pop()
            if node.id == id:
                return node.to_dict()
            for node in node.children:
                stack.append(node)

    def get_сhildren(self, id: int) -> list:
        """
        Возвращает массив элементов, являющихся дочерними для того элемента,
        чей идентификатор получен в аргументе.

        :param id: int
        :return: [
            {'id': 7, 'parent': 4, 'type': None},
        ]
        """

        return [child.to_dict() for child in self.adjacency_matrix[id]]

    def get_сhildren_by_stack(self, id: int) -> list:
        """
        Возвращает массив элементов, являющихся дочерними для того элемента,
        чей идентификатор получен в аргументе.

        :param id: int
        :return: [
            {'id': 7, 'parent': 4, 'type': None},
        ] or None
        """

        stack = [self.root]
        while stack:
            node = stack.pop()
            if node.id == id:
                return [child.to_dict() for child in node.children]
            for node in node.children:
                stack.append(node)

    def get_all_parents(self, id) -> list:
        """
        Возвращает массив из цепочки родительских элементов, начиная от самого
        элемента, чей идентификатор был передан в аргументе и до корневого элемента.

        :param id: int
        :return: [
            {'id': 4, 'parent': 2, 'type': 'test'},
        ]
        """

        nodes = {node['id']: node for node in self.get_all()}
        parents = []
        stack = [self.root]
        while stack:
            node = stack.pop()
            if node.id == id:
                break
            for node in node.children:
                stack.append(node)
        node = nodes[node.parent]
        parents.append(node)
        while node['parent'] != 'root':
            node = nodes[node['parent']]
            parents.append(node)
        return parents

        print('exit')


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
    ts.insert({'id': 9, 'parent': 8, 'type': 'test'})  # узел добавлен
    # ts.insert({'id': 11, 'parent': 10, 'type': 'test'})
    # __main__.MissingParentException: Дерево не содержит узла с идентификатором 10

    get_all = ts.get_all()
    # get_all = [
    #     {'id': 2, 'parent': 1, 'type': 'test'},
    #     {'id': 3, 'parent': 1, 'type': 'test'},
    #     {'id': 1, 'parent': 'root', 'type': None},
    #     {'id': 4, 'parent': 2, 'type': 'test'},
    #     {'id': 5, 'parent': 2, 'type': 'test'},
    #     {'id': 6, 'parent': 2, 'type': 'test'},
    #     {'id': 7, 'parent': 4, 'type': None},
    #     {'id': 8, 'parent': 4, 'type': None},
    #     {'id': 9, 'parent': 8, 'type': 'test'}
    # ]

    get_all_by_stack = ts.get_all_by_stack()
    # get_all_by_stack = [
    #     {'id': 1, 'parent': 'root', 'type': None},
    #     {'id': 3, 'parent': 1, 'type': 'test'},
    #     {'id': 2, 'parent': 1, 'type': 'test'},
    #     {'id': 6, 'parent': 2, 'type': 'test'},
    #     {'id': 5, 'parent': 2, 'type': 'test'},
    #     {'id': 4, 'parent': 2, 'type': 'test'},
    #     {'id': 8, 'parent': 4, 'type': None},
    #     {'id': 9, 'parent': 8, 'type': 'test'},
    #     {'id': 7, 'parent': 4, 'type': None}
    # ]


    get_item = ts.get_item(7)
    # get_item = {'id': 7, 'parent': 4, 'type': None}

    get_сhildren = ts.get_сhildren(4)
    # get_сhildren = [
    #     {'id': 7, 'parent': 4, 'type': None},
    #     {'id': 8, 'parent': 4, 'type': None}
    # ]

    get_сhildren_by_stack = ts.get_сhildren_by_stack(2)
    # get_сhildren_by_stack = [
    #     {'id': 4, 'parent': 2, 'type': 'test'},
    #     {'id': 5, 'parent': 2, 'type': 'test'},
    #     {'id': 6, 'parent': 2, 'type': 'test'}
    # ]

    get_all_parents = ts.get_all_parents(7)
    # get_all_parents = [
    #     {'id': 4, 'parent': 2, 'type': 'test'},
    #     {'id': 2, 'parent': 1, 'type': 'test'},
    #     {'id': 1, 'parent': 'root', 'type': None}
    # ]

    # print('exit')
