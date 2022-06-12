from PIL import Image
import time, sys,random
from collections import deque
from image import *
# -------------------------------------- Getting a reference to the maze image ----------------------------------------------------------------------------
DEFAULT_IMAGE_PATH = "40x40_0.png" # Change this to the path of the image you want to use
# Modify the above constant if you're playing around with the script
# and can't be bothered with using the terminal every time :)
if len(sys.argv) > 1:
    try:
        path = sys.argv[1]
        if len(path) < 4 or path[-4:] != ".png":
            path += ".png"
        img = Image.open(path)
    except:
        print("Incorrect input. Maybe you misspelled the file name?")
        sys.exit(0)
elif DEFAULT_IMAGE_PATH != None:
    try:
        img = Image.open(DEFAULT_IMAGE_PATH)
    except:
        print("Can't load the default file path, make sure the file exists")
else:
    print("You need to pass the image filename for the script to run")
    print("For example: 'maze_solver.py test_maze.png'")
    sys.exit(0)


IMG_WIDTH = img.size[0]
IMG_HEIGHT = img.size[1]
# -------------------------------------- Declaration of classes the script uses ----------------------------------------------------------------------------
class Graph:
    startNode,endNode = None, None
    node_count = 0
    nodes_array = [[None for i in range(IMG_WIDTH)] for i in range(IMG_HEIGHT)]

    def __init__(self,arr):
        # 1. Find start and end nodes
        start,end = GraphNode(0,0), GraphNode(0,0)
        for x in range(1,IMG_WIDTH-1):
            if arr[0][x] == 255:
                start = GraphNode(x,0)
                self.nodes_array[0][x] = start
                break
        for x in range(1,IMG_WIDTH-1):
            if arr[-1][x] == 255:
                end = GraphNode(x,IMG_HEIGHT-1)
                self.nodes_array[-1][x] = end
                break
        self.startNode = start
        self.endNode = end
        # 2. Go from left-top to right-bottom, finding node spots and connecting them together
        # The connecting works by only looking up and left, until it hits a wall
        # Left and right suffice. For example even if node A has node B below it and doesn't look, for node B, A is up, so they get connected
        for y in range(1,IMG_HEIGHT-1):
            for x in range(1,IMG_WIDTH-1):
                left,right,up,down = arr[y][x-1],arr[y][x+1],arr[y-1][x],arr[y+1][x]
                total = left+right+up+down
                if arr[y][x] == 255 and total > 255 and (total > 510 or up != down):
                    # Conditions for a new node explained:
                    # 1. Needs to be a white pixel on the image
                    # 2. Needs to have more than one white tile connected to it (total > 255)
                    # 3. Needs to either have 3+ tiles connected, or be a corner (up != down)
                    g = GraphNode(x,y)
                    self.nodes_array[y][x] = g
                    self.node_count += 1
                    # Checking for nodes to connect to - left of this node
                    x2 = x-1
                    while x2 >= 0:
                        if self.nodes_array[y][x2] != None:
                            self.nodes_array[y][x].connect_to(self.nodes_array[y][x2])
                            break
                        x2 -= 1
                        if arr[y][x2] == 0:
                            break
                    
                    # Checking for nodes to connect to - above this node
                    y2 = y-1
                    while y2 >= 0:
                        if self.nodes_array[y2][x] != None:
                            self.nodes_array[y][x].connect_to(self.nodes_array[y2][x])
                            break
                        y2 -= 1
                        if arr[y2][x] == 0:
                            break
        
        # 3. Connect the end node to the one above it
        # It wasn't connected in the for look because it doesn't scan the last row and only looks up, not down
        y2 = -2
        while self.nodes_array[y2][self.endNode.x] == None:
            y2 -= 1
        self.endNode.connect_to(self.nodes_array[y2][self.endNode.x])

class GraphNode:
    x,y = 0,0
    connected_to = []
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.connected_to = []
    
    def connect_to(self, differentNode):
        self.connected_to.append(differentNode)
        differentNode.connected_to.append(self)
    
    def distance_to(self,differentNode):
        return abs(self.x-differentNode.x) + abs(self.y-differentNode.y)

class AstarQueueItem:
    node,distance_travelled,via = None,0,None

    def __init__(self,node,distance_travelled,via):
        self.node = node
        self.distance_travelled = distance_travelled
        self.via = via # tuple with coords of node it came from (x,y)

    def total_distance(self):
        return self.distance_travelled + abs(self.node.x-END_X) + abs(self.node.y-END_Y)

class AstarQueue:
    queue = []
    finished = {}
    nodes_visited = set([])
    finished_path = []
    found_exit = False
    endNode = None
    def __init__(self,start,end):
        self.endNode = end
        self.queue.append(AstarQueueItem(start,0,start))
        self.queue = deque(self.queue)
        while not self.found_exit:
            self.iterate_astar()
        st = time.time()
        self.construct_path()
        et = time.time()
        print("Constructing path complete, time elapsed:")
        print(et-st,"s")
    
    def construct_path(self):
        path = []
        looking_for = (END_X,END_Y)
        path.append(looking_for)
        while looking_for != (START_X,START_Y):
            looking_for = self.finished[looking_for]
            path.append(looking_for)
        self.finished_path = path
    
    def add_to_queue(self,new_queue_item):
        for i in range(len(self.queue)):
            qi = self.queue[i] # avoids having to go look into the array 4 times
            if new_queue_item.node == qi.node:
                if new_queue_item.distance_travelled < qi.distance_travelled:
                    qi = new_queue_item
                return
            if new_queue_item.total_distance() < qi.total_distance():
                self.queue.insert(i,new_queue_item)
                return
        self.queue.append(new_queue_item)


    def iterate_astar(self):
        first = self.queue.popleft()
        if first.node == self.endNode:
            # reached the goal
            print("A* done")
            self.finished[(END_X,END_Y)] = first.via
            self.found_exit = True
            return
        for connected_node in first.node.connected_to:
            if (connected_node.x,connected_node.y) in self.nodes_visited:
                continue
            aa = AstarQueueItem(connected_node,first.distance_travelled+first.node.distance_to(connected_node),(first.node.x,first.node.y))
            self.add_to_queue(aa)
        self.finished[(first.node.x,first.node.y)] = first.via
        self.nodes_visited.add((first.node.x,first.node.y))

# -------------------------------------- Making a graph representation of the maze ----------------------------------------------------------------------------
start_t = time.time()
array_representation = [[img.getpixel((x,y)) for x in range(IMG_WIDTH)]for y in range(IMG_HEIGHT)]
g = Graph(array_representation)
START_X = g.startNode.x
START_Y = g.startNode.y
END_X = g.endNode.x
END_Y = g.endNode.y

end_t = time.time()
print("Converting array to graph complete, time elapsed:")
print(end_t-start_t,"s")
print("Graph nodes created:",g.node_count)

# -------------------------------------- Running A* ----------------------------------------------------------------------------
start_t = time.time()
a = AstarQueue(g.startNode,g.endNode)
end_t = time.time()
print("A* pathfinding complete, time elapsed:")
print(end_t-start_t,"s")

