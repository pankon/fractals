import math

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class KochNode:
    func = None

    def __init__(self, point: Point, next=None):
        self.point = point
        self.next = next

    def split(self):
        if not self.next and not isinstance(self.next, KochNode):
            return

        self.func()

    def convert_np(self):
        x = []
        y = []

        current = self
        while current:
            x.append(current.point.x)
            y.append(current.point.y)
            current = current.next

        return x, y

    def plot(self, axes):
        arrays = self.convert_np()
        #x = np.linspace(arrays[0][0], arrays[0][0][-1])
        # print(arrays)
        axes.plot(arrays[0], arrays[1])


def split(node: KochNode):
    dy = -(node.point.y - node.next.point.y)
    dx = -(node.point.x - node.next.point.x)
    original_angle = math.atan2(dy, dx)
    magnitude = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
    factor = 3.0
    segment_size = magnitude / factor
    if segment_size <= 0.1:
        return

    last = node.next
    angles = [0, 60, -60, 0]
    new_nodes = []
    current = node
    for angle in angles:
        x = segment_size * math.cos((angle * math.pi / 180) + original_angle) + current.point.x
        y = segment_size * math.sin((angle * math.pi / 180) + original_angle) + current.point.y
        new_node = KochNode(Point(x, y))
        new_nodes.append(new_node)
        current = new_node

    node.next = new_nodes[0]
    node.split()
    for i, node in enumerate(new_nodes[:-1]):
        node.next = new_nodes[i + 1]
        node.split()

    new_nodes[-1].next = last
    new_nodes[-1].split()


if __name__ == "__main__":
    KochNode.func = split

    max_x = 100
    for i in range(0, max_x // 2, 1):
        node = KochNode(Point(i, 0), next=KochNode(Point(max_x - i, 0)))
        node.split()
        node.plot(plt)

    plt.show()
