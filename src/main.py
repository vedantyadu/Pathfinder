import tkinter as tk
from tkinter import messagebox
import threading
import time


rows = int(input('Enter the width of the maze '))
maze = []


# Make a maze of the desired size.
def makemaze():
    global rows, buttons, maze

    for i in range(0, rows):
        maze.append([])
        for j in range(0, rows):
            maze[i].append(0)


makemaze()

row = len(maze) - 1
col = len(maze[0]) - 1

strt_pos = None
end_pos = None


# Defining a Node.
class Node:
    def __init__(self, parent=None, pos=None):
        # Parent and the position of Node.
        self.parent = parent
        self.pos = pos
        self.length = 0

        # Costs of the Node.
        self.g = 0
        self.h = 0
        # F cost for A-star or length for BFS.
        self.f = 0

    # Check for same position.
    def __eq__(self, other):
        return self.pos == other.pos

    # Check for lower f cost.
    def __lt__(self, other):
        return self.f < other.f


start = None
end = None


def bfs():
    global found, buttons, sec, find

    sec = 0
    find = 0

    found = False

    for btn in buttons:
        if btn.but.cget('bg') != 'purple4':
            btn.but.config(bg='white')

    if speed.get() == 'Fast':
        sec = 0.0
        find = 0

    if speed.get() == 'Slow':
        sec = 0.007
        find = 0.02

    q = [Node(None, strt_pos)]

    # BFS to find the shortest path.
    while not found:

        time.sleep(sec)

        q.sort()

        cur_node = q.pop(0)

        for btn in buttons:
            if btn.row == cur_node.pos[0] + 1 and btn.column == cur_node.pos[1] + 1 \
                    and btn.but.cget('bg') != 'purple4':
                btn.but.config(bg='light sky blue')

        if cur_node == end:

            path = []

            while cur_node.parent is not None:
                path.append(cur_node.pos)
                cur_node = cur_node.parent

            path.append(start.pos)
            path.reverse()

            for point in path:
                time.sleep(find)
                for btn in buttons:
                    if btn.row == point[0] + 1 and btn.column == point[1] + 1:
                        btn.but.config(bg='yellow')

            print('\n{}'.format(path))
            found = True

        for _ in [(1, 0), (-1, 0), (0, 1), (0, -1)]:

            new_pos = (cur_node.pos[0] + _[0], cur_node.pos[1] + _[1])

            if new_pos[0] < 0 or new_pos[0] > len(maze) - 1 or new_pos[1] < 0 or new_pos[1] > len(maze[0]) - 1:
                continue

            if maze[new_pos[0]][new_pos[1]] != 1:
                new_node = Node(cur_node, new_pos)

                if new_node not in q:
                    new_node.f = new_node.f + 1
                    q.append(new_node)
                    for btn in buttons:
                        if btn.row == new_node.pos[0] + 1 and btn.column == new_node.pos[1] + 1 \
                                and btn.but.cget('bg') != 'purple4' and btn.but.cget('bg') != 'light sky blue' \
                                and btn.but.cget('bg') != 'yellow':
                            btn.but.config(bg='light green')


# Start finding the path.
def astar():
    global found, open_list, closed_list, buttons, sec, find

    sec = 0
    find = 0

    # List for potential points.
    open_list = []
    # List for already explored points.
    closed_list = []

    found = False

    for btn in buttons:
        if btn.but.cget('bg') != 'purple4':
            btn.but.config(bg='white')

    if speed.get() == 'Fast':
        sec = 0.0
        find = 0

    if speed.get() == 'Slow':
        sec = 0.007
        find = 0.02

    open_list.append(start)

    while found is False:

        time.sleep(sec)

        try:
            open_list.sort()
            cur_node = open_list[0]

            # Show the explored nod on the grid.
            for btn in buttons:
                if btn.row == cur_node.pos[0] + 1 and btn.column == cur_node.pos[1] + 1 \
                        and btn.but.cget('bg') != 'purple4':
                    btn.but.config(bg='light sky blue')

            # Pop the item from open list and put it in closed list(explored list).
            open_list.pop(0)
            closed_list.append(cur_node)

            # If the current Node is the end.
            if cur_node == end:

                path = []
                current = cur_node

                while current is not None:
                    path.append(current.pos)
                    current = current.parent

                path.reverse()
                print(path)

                # Show the path in GUI.
                for point in path:
                    time.sleep(find)
                    for btn in buttons:
                        if btn.row == point[0] + 1 and btn.column == point[1] + 1:
                            btn.but.config(bg='yellow')

                found = True

            children = []

            # Creating all possible child nodes.
            for new_pos in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                # Neighbour nodes.
                node_pos = (cur_node.pos[0] + new_pos[0], cur_node.pos[1] + new_pos[1])

                # Make sure within range.
                if node_pos[0] > row or node_pos[0] < 0 or node_pos[1] > col or node_pos[1] < 0:
                    continue

                # Wall hit check.
                if maze[node_pos[0]][node_pos[1]] != 0:
                    continue

                # Create new Node.
                new_node = Node(cur_node, node_pos)

                # Adding the children of parent Node to the children list.
                children.append(new_node)

            # Checking the costs of all the children.
            for child in children:

                # Only if child node isn't already known.
                if (child not in closed_list) and (child not in open_list):
                    # f, g, h cost of the child node.
                    # g cost.
                    child.g = cur_node.g + 1
                    # h cost.
                    child.h = (((child.pos[0] - end.pos[0]) ** 2 + (child.pos[1] - end.pos[1]) ** 2) ** 0.5) * 1.41
                    # f cost (g + h).
                    child.f = child.g + child.h

                    # Add the child to the open list
                    open_list.append(child)

                    # Show the nodes in open list on the grid.
                    for btn in buttons:
                        if btn.row == child.pos[0] + 1 and btn.column == child.pos[1] + 1 \
                                and btn.but.cget('bg') != 'purple4' and btn.but.cget('bg') != 'yellow':
                            btn.but.config(bg='light green')

        # No valid path found.
        except IndexError:
            print('no path found')
            tk.messagebox.showinfo('', 'No valid path found!')
            break


# Graphical user interface (GUI).
win = tk.Tk()
win.config(bg = 'grey85')
win.title('A-star pathfinding')
tk.Grid.rowconfigure(win, 0, weight=1)
tk.Grid.columnconfigure(win, 0, weight=1)

# Start and end icons.
s = tk.PhotoImage(file='start.png')
e = tk.PhotoImage(file='end.png')
s_photo = s.subsample(25, 25)
e_photo = e.subsample(25, 25)


# Position (in grid) of the last clicked button.
last = (0, 0)


# Clicking buttons.
def boundary(event):
    global last, strt_pos, end_pos

    # If the start and end position is defined.
    if strt_pos is not None and end_pos is not None:
        for btn in buttons:

            r = btn.row - 1
            c = btn.column - 1

            # Relative position of the pointer wrt window.
            mouse_pos = win.grid_location(win.winfo_pointerx() - win.winfo_rootx(),
                                          win.winfo_pointery() - win.winfo_rooty())

            # If button is not the starting or the ending.
            if btn.but.cget('image') == '' and btn.row == mouse_pos[1] and btn.column == mouse_pos[0]:
                # If the row and column of a button matches with mouse position in grid.
                if btn.row == mouse_pos[1] and btn.column == mouse_pos[0]:
                    # If the button is not the last clicked button.
                    if (btn.column, btn.row) != last:
                        if btn.but.cget('bg') == 'white' or btn.but.cget('bg') == 'light green' \
                                or btn.but.cget('bg') == 'light sky blue' or btn.but.cget('bg') == 'yellow':
                            if maze[r][c] != 1:
                                btn.but.config(bg='purple4')
                                maze[r][c] = 1

                        # If the button is already a wall.
                        else:
                            btn.but.config(bg='white')
                            maze[r][c] = 0

                        # Last clicked button position.
                        last = mouse_pos


# Bind left click and motion to boundary function.
win.bind('<B1-Motion>', boundary)


# Defining buttons.
class button:

    # Add the starting and ending node by clicking.
    def pos(self):
        global strt_pos, end_pos, start, end

        if strt_pos is None and end_pos is None:
            strt_pos = (self.row - 1, self.column - 1)
            self.but.config(image=s_photo)
            # Starting position.
            start = Node(None, strt_pos)
            start.g = start.h = start.f = 0

        elif end_pos is None and strt_pos is not None:
            end_pos = (self.row - 1, self.column - 1)
            self.but.config(image=e_photo)
            # Ending position.
            end = Node(None, end_pos)
            end.g = end.h = end.f = 0

    def __init__(self, rows, columns):
        self.row = rows
        self.column = columns
        self.but = tk.Button(win, bg='white', height=1, width=2, relief='flat',
                             command=lambda: button.pos(self))
        self.but.grid(row=rows, column=columns, sticky='news', padx=1, pady=1)
        tk.Grid.columnconfigure(win, columns, weight=1)
        tk.Grid.rowconfigure(win, rows, weight=1)


# Reset to starting state.
def clear():
    global maze, strt_pos, end_pos, buttons, found, open_list, closed_list

    maze = []
    makemaze()

    found = True

    strt_pos = None
    end_pos = None

    for btn in buttons:
        btn.but.config(bg='white')
        btn.but.config(image='')


def visualize():
    if algo.get() == 'BFS':
        t = threading.Thread(target=bfs)
        t.start()
    if algo.get() == 'A-Star':
        t = threading.Thread(target=astar)
        t.start()


# Automatically create buttons for the GUI.
buttons = [button(i, j) for i in range(1, len(maze) + 1) for j in range(1, len(maze[0]) + 1)]

# Speed of searching.
speed = tk.StringVar()
speed.set('Speed')
select = tk.OptionMenu(win, speed, 'Slow', 'Fast')
select.config(relief='flat', bg='white', width=2, height=1)
select['highlightthickness'] = 0
select.grid(row=row + 2, column=5, columnspan=3, sticky='news', padx=1, pady=1)
tk.Grid.columnconfigure(win, 5, weight=1)
tk.Grid.rowconfigure(win, row + 2, weight=1)

# Algorithm.
algo = tk.StringVar()
algo.set('Algoithm')
sel_alg = tk.OptionMenu(win, algo, 'BFS', 'A-Star')
sel_alg.config(relief='flat', bg='white', width=2, height=1)
sel_alg['highlightthickness'] = 0
sel_alg.grid(row=row + 2, column=8, columnspan=4, sticky='news', padx=1, pady=1)
tk.Grid.columnconfigure(win, 5, weight=1)
tk.Grid.rowconfigure(win, row + 2, weight=1)

# Start button.
srt = tk.Button(win, text='Start', bg='white', relief='flat', command=lambda: visualize())
srt.grid(row=row + 2, column=1, columnspan=2, sticky='news', padx=1, pady=1)
tk.Grid.columnconfigure(win, 1, weight=1)
tk.Grid.rowconfigure(win, row + 2, weight=1)

# Clear button.
clr = tk.Button(win, text='Clear', bg='white', relief='flat', command=lambda: clear())
clr.grid(row=row + 2, column=3, columnspan=2, sticky='news', padx=1, pady=1)
tk.Grid.columnconfigure(win, 3, weight=1)
tk.Grid.rowconfigure(win, row + 2, weight=1)

win.mainloop()
