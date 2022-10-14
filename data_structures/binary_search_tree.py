from collections import deque
from queue import Queue

queue = Queue()


class BinarySearchTree:

    class Node:
        def __init__(self, value):
            self.value = value
            self.left = None
            self.right = None

        def __str__(self):
            return f'The Node with value {self.value}'

    def __init__(self, value):
        self.root = self.Node(value)
        self.adjacency_matrix = {}

    def insert(self, value, current_node=None):
        """
        Выполняет вставку узла.

        :param value: значение узла
        :param current_node: текущий узел
        """

        if current_node:
            if value < current_node.value:
                if current_node.left:
                    current_node = current_node.left
                    self.insert(value, current_node)
                else:
                    current_node.left = self.Node(value)
            elif value > current_node.value:
                if current_node.right:
                    current_node = current_node.right
                    self.insert(value, current_node)
                else:
                    current_node.right = self.Node(value)
        else:
            self.insert(value, current_node=self.root)

    def in_order(self, current_node=None) -> list:
        """
        Выполняет обход дерева по порядку.

        :param current_node: текущий узел
        """

        path = []
        if current_node:
            path += self.in_order(current_node.left) if current_node.left else []
            path.append(current_node.value)
            path += self.in_order(current_node.right) if current_node.right else []
        else:
            path += self.in_order(self.root)
        return path

    def pre_order(self, current_node=None) -> list:
        """
        Выполняет прямой обход. Выводит родителя,
        а затем всех его потомков слева на право.

        :param current_node: текущий узел
        """

        path = []
        if current_node:
            path.append(current_node.value)
            path += self.pre_order(current_node.left) if current_node.left else []
            path += self.pre_order(current_node.right) if current_node.right else []
        else:
            path += self.pre_order(self.root)
        return path

    def post_order(self, current_node=None) -> list:
        """
        Выполняет обратный обход двоичного дерева. Выводит потомков, а затем родителя.

        :param current_node: текущий узел
        """

        path = []
        if current_node:
            path += self.post_order(current_node.left) if current_node.left else []
            path += self.post_order(current_node.right) if current_node.right else []
            path.append(current_node.value)
        else:
            path += self.post_order(self.root)
        return path

    def breadth_first_search(self, current_node=None) -> list:
        """
        Выполняет обход дерева в ширину.

        :param current_node: текущий узел
        """

        path = []
        if current_node:
            path.append(current_node.value)
            if current_node.left:
                queue.put(current_node.left)
            if current_node.right:
                queue.put(current_node.right)
            while queue.empty() is False:
                path += self.breadth_first_search(queue.get())
            return path
        else:
            path += self.breadth_first_search(self.root)
        return path

    def make_dict_of_adjacency_matrix(self, current_node=None) -> dict:
        """
        Возвращает матрицу смежности дерева в виде словаря.

        :param current_node: текущий узел
        """

        if current_node:
            self.adjacency_matrix[current_node.value] = []
            if current_node.left:
                self.adjacency_matrix[current_node.value].append(
                    current_node.left.value
                )
                self.make_dict_of_adjacency_matrix(current_node.left)
            if current_node.right:
                self.adjacency_matrix[current_node.value].append(
                    current_node.right.value
                )
                self.make_dict_of_adjacency_matrix(current_node.right)
            return self.adjacency_matrix
        else:
            return self.make_dict_of_adjacency_matrix(self.root)

    def bfs_by_adjacency_matrix(self, adjacency_matrix: dict) -> list:
        """
        Выполняет обход дерева в ширину по матрице смежности.

        :param adjacency_matrix: матрица смежности
        """

        queue = deque(self.root.value)
        path = []
        while queue:
            node_value = queue.popleft()
            path.append(node_value)
            for node_value in adjacency_matrix[node_value]:
                queue.append(node_value)
        return path

    def depth_first_search_by_steck(self, adjacency_matrix: dict) -> list:
        """
        Выпонятет обход дерева в глубину. Выводит родителя,
        а затем всех его потомков справа на лево.

        :param adjacency_matrix: матрица смежности
        """

        stack = [self.root.value]
        path = []
        while stack:
            node_value = stack.pop()
            path.append(node_value)
            for node_value in adjacency_matrix[node_value]:
                stack.append(node_value)
        return path

    def search(self, value) -> bool:
        """
        Проверяет наличие в двоичном дереве узда по его значению.

        :param value: искомое значение узла
        :return: True or False
        """

        return value in self.make_dict_of_adjacency_matrix()


#                 g
#               /   \
#             c       i
#            / \     / \
#           b   e   h   j
#          /   / \       \
#         a   d   f       k

if __name__ == '__main__':
    tree = BinarySearchTree('g')
    tree.insert('c')
    tree.insert('b')
    tree.insert('a')
    tree.insert('e')
    tree.insert('d')
    tree.insert('f')
    tree.insert('i')
    tree.insert('h')
    tree.insert('j')
    tree.insert('k')

    in_order_path = tree.in_order()
    # in_order_path = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']

    pre_order_path = tree.pre_order()
    # pre_order_path = ['g', 'c', 'b', 'a', 'e', 'd', 'f', 'i', 'h', 'j', 'k']

    post_order_path = tree.post_order()
    # post_order_path = ['a', 'b', 'd', 'f', 'e', 'c', 'h', 'k', 'j', 'i', 'g']

    bfs_path = tree.breadth_first_search()
    # bfs_path = ['g', 'c', 'i', 'b', 'e', 'h', 'j', 'a', 'd', 'f', 'k']

    dict_of_adjacency_matrix = tree.make_dict_of_adjacency_matrix()
    # dict_of_adjacency_matrix = {
    #     'g': ['c', 'i'],
    #     'c': ['b', 'e'],
    #     'b': ['a'],
    #     'a': [],
    #     'e': ['d', 'f'],
    #     'd': [],
    #     'f': [],
    #     'i': ['h', 'j'],
    #     'h': [],
    #     'j': ['k'],
    #     'k': []
    # }

    bfs_by_adjacency_matrix_path = tree.bfs_by_adjacency_matrix(
        dict_of_adjacency_matrix
    )
    # bfs_by_adjacency_matrix_path = [
    #   'g', 'c', 'i', 'b', 'e', 'h', 'j', 'a', 'd', 'f', 'k'
    # ]

    depth_first_search_path = tree.depth_first_search_by_steck(
        dict_of_adjacency_matrix
    )
    # depth_first_search_path = [
    #   'g', 'i', 'j', 'k', 'h', 'c', 'e', 'f', 'd', 'b', 'a'
    # ]

    search_g = tree.search('g')  # True
    search_c = tree.search('c')  # True
    search_b = tree.search('b')  # True
    search_a = tree.search('a')  # True
    search_e = tree.search('e')  # True
    search_d = tree.search('d')  # True
    search_f = tree.search('f')  # True
    search_i = tree.search('i')  # True
    search_h = tree.search('h')  # True
    search_j = tree.search('j')  # True
    search_k = tree.search('k')  # True
    search_o = tree.search('o')  # False
    search_p = tree.search('p')  # False

    print('exit')

