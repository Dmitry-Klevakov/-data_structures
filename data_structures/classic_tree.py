from collections import defaultdict, deque
from itertools import chain


class MissingNodeException(Exception):
    """
    Исключение возникает если узда с искомым значением не существует.
    """

    def __init__(self, value):
        self.message = f'Дерево не содержит узла со значением "{value}"'

    def __str__(self):
        return self.message


class ClassicTree:

    class Node:
        def __init__(self, value, parent):
            self.value = value
            self.parent = parent
            self.children = []

        def to_dict(self):
            return {
                'value': self.value,
                'parent': self.parent.value,
                'children': [child.id for child in self.children]
            }

    def __init__(self, value):
        self.root = self.Node(value, 'root')

    def insert(self, value, parent):
        """
        Выполняет вставку узла.

        :param value: значение узла
        """

        stack = [self.root]
        while stack:
            node = stack.pop()
            if node.value == parent:
                new_node = self.Node(value, parent)
                node.children.append(new_node)
                return
            for node in node.children:
                stack.append(node)
        raise MissingNodeException(parent)

    def get_adjacency_matrix(self) -> dict:
        """
        Возвращает матрицу смежности дерева в виде словаря.
        """

        adjacency_matrix = defaultdict(list)
        stack = [self.root]
        while stack:
            node = stack.pop()
            if node.children:
                adjacency_matrix[node.value].extend(node.children)
            else:
                adjacency_matrix[node.value]
            for node in node.children:
                stack.append(node)
        return adjacency_matrix

    def depth_first_search_by_steck(self) -> list:
        """
        Выпонятет обход дерева в глубину.
        """

        stack = [self.root]
        path = []
        while stack:
            node = stack.pop()
            path.append(node.value)
            for node in node.children:
                stack.append(node)
        return path

    def breadth_first_search(self) -> list:
        """
        Выполняет обход дерева в ширину.
        """

        queue = deque([self.root])
        path = []
        while queue:
            node = queue.pop()
            path.append(node.value)
            for node in node.children:
                queue.appendleft(node)
        return path

    def search_by_stack(self, value) -> bool:
        """
        Проверяет наличие в двоичном дереве узда по его значению.

        :param value: искомое значение узла
        :return: True or False
        """

        stack = [self.root]
        while stack:
            node = stack.pop()
            if node.value == value:
                return True
            for node in node.children:
                stack.append(node)
        return False

    def search(self, value) -> bool:
        """
        Проверяет наличие в двоичном дереве узда по его значению.

        :param value: искомое значение узла
        :return: True or False
        """

        return value in self.get_adjacency_matrix()

    def get_сhildren_by_adjacency_matrix(self, value: int) -> list:
        """
        Возвращает массив элементов, являющихся дочерними для того элемента,
        чей идентификатор получен в аргументе.

        :param value: int
        :return: ['h', 'm', 'j']
        """

        children = self.get_adjacency_matrix().get(value, None)
        if children:
            return [child.value for child in children]
        else:
            raise MissingNodeException(value)

    def get_сhildren(self, value: int) -> list:
        """
        Возвращает массив элементов, являющихся дочерними для того элемента,
        чей идентификатор получен в аргументе.

        :param value: int
        :return: ['h', 'm', 'j']
        """

        stack = [self.root]
        while stack:
            node = stack.pop()
            if node.value == value:
                return [child.value for child in node.children]
            for node in node.children:
                stack.append(node)
        raise MissingNodeException(value)

    def __get_subtree_by_node(self, node: Node, current_node=None) -> list:
        """
        Возвращает все значения узлов поддерева, корнем которого является узел,
        переданный в качестве аргумента.

        :param node: объект узла
        :return: ['h', 'm', 'j']
        """
        path = []
        if node.children:
            children_values = [child.value for child in node.children]
            path += children_values
            for child in node.children:
                path += list(chain(self.__get_subtree_by_node(child)))
        return path

    def get_subtree_by_value(self, value) -> list:
        """
        Возвращает все значения узлов поддерева, корнем которого является элемент,
        чей идентификатор получен в аргументе.

        :param value: значение узла
        :return: ['h', 'm', 'j']
        """

        stack = [self.root]
        while stack:
            node = stack.pop()
            if node.value == value:
                return self.__get_subtree_by_node(node)
            for node in node.children:
                stack.append(node)
        raise MissingNodeException(value)




#                 g
#              /  |  \
#           c     l     i
#          / \    |   / | \
#         b   e   p  h  m  j
#       /   /  \            \
#      a   d    f            k


# Исходные данные:
if __name__ == '__main__':
    tree = ClassicTree('g')
    tree.insert('c', 'g')
    tree.insert('i', 'g')
    tree.insert('j', 'i')
    tree.insert('e', 'c')
    tree.insert('h', 'i')
    tree.insert('d', 'e')
    tree.insert('f', 'e')
    tree.insert('b', 'c')
    tree.insert('a', 'b')
    tree.insert('l', 'g')
    tree.insert('m', 'i')
    tree.insert('p', 'l')
    tree.insert('k', 'j')

    # tree.insert('q', 'w')

    depth_first_search_by_steck_path = tree.depth_first_search_by_steck()
    # ['g', 'l', 'p', 'i', 'm', 'h', 'j', 'k', 'c', 'b', 'a', 'e', 'f', 'd']

    breadth_first_search_path = tree.breadth_first_search()
    # ['g', 'c', 'i', 'l', 'e', 'b', 'j', 'h', 'm', 'p', 'd', 'f', 'a', 'k']

    search_l = tree.search('l')  # True
    search_m = tree.search('m')  # True
    search_u = tree.search('u')  # False

    search_by_stack_l = tree.search_by_stack('l')  # True
    search_by_stack_m = tree.search_by_stack('m')  # True
    search_by_stack_u = tree.search_by_stack('u')  # False

    children_i = tree.get_сhildren('i')
    # children_i = ['j', 'h', 'm']

    сhildren_by_adjacency_matrix_i = tree.get_сhildren_by_adjacency_matrix('i')
    # сhildren_by_adjacency_matrix_i = ['j', 'h', 'm']

    subtree_i = tree.get_subtree_by_value('i')
    # subtree_i = ['j', 'h', 'm', 'k']

    print('exit')
