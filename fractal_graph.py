"""
fractal_graph.py
"""
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

class FractalNode:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.children = []
        self.next = None

    def split(self, func, depth):
        if not depth:
            return self

        segments = func(self.start, self.end)
        self.children = [FractalNode(segment[0], segment[1]).split(func, depth - 1) for segment in segments]

        n_segs = len(self.children)
        for i in range(n_segs - 1):
            current = self.children[i]

            if i < n_segs - 1:
                current.next = self.children[i + 1]
            else:
                current.next = self.next

        # for current in self.children:
        #    current.split(func, depth - 1, parent=self)
            

        #self.next = None
        #self.prev = None

        return self
    
    def __str__(self):
        return str(self.start) + str(self.end) + str([str(child) for child in self.children])

    def get_all_lowest_children(self):
        if not self.children:
            return [self]

        children = []
        for child in self.children:
            children.extend(child.get_all_lowest_children())
        
        return children

    def get_list(self):
        x = []
        y = []
        #lowest = self.children[0]
        #while lowest.children:
        #    lowest = lowest.children[0]

        #current = lowest

        for current in self.get_all_lowest_children():
            x.append(current.start[0])
            x.append(current.end[0])
            y.append(current.start[1])
            y.append(current.end[1])

            current = current.next
        
        return x, y

    def plot(self, axes):
        x = np.linspace(self.start[0], self.end[0])
        y = x ** 2
        arrays = self.get_list()
        # print(arrays)
        axes.plot(arrays[0], arrays[1])


if __name__ == "__main__":
    node = FractalNode((0, 0), (100, 0))

    def split(start, end):
        dy = int((end[0] - start[0]) / 10.0)
        dx = int((end[1] - start[1]) / 10.0)
        for i in range(start[0], end[0], dx):
            for j in range(start[1], end[1], dy):
                yield [(i, j), (i + dx, j + dy)]

    def koch_split(start, end):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        #print(start, end)
        size = math.sqrt(dx ** 2 + dy ** 2) / 3.0
        if not dx:
            angle = 0
        else:
            angle = math.atan(dy / dx)
            #print(angle)

        angles = [
            0, #(size * math.cos(angle), size * math.sin(angle)),
            (math.pi / 3.0), #(size * math.cos(angle + (math.pi / 3.0)), size * math.sin(angle + (math.pi / 3))),
            -(math.pi / 3.0), #(size * math.cos(angle - (math.pi / 3.0)), size * math.sin(angle - (math.pi / 3))),
            0, #(size * math.cos(angle), size * math.sin(angle))
        ]

        current = start
        for current_angle in angles:
            offset = (size * math.cos(angle + current_angle), size * math.sin(angle + current_angle))
            next_pt = (current[0] + offset[0], current[1] + offset[1])
            yield [current, next_pt]
            current = next_pt

        yield [current, end]


    ranges = (1, 7)
    fig, axes = plt.subplots(ranges[0], ranges[1] - 1)
    for depth in range(*ranges):
        node.split(koch_split, depth)
        #print(list(node.get_list()))
        node.plot(axes[depth - 1])
        print("done")
    plt.show() 


            