import pygame
import random
import threading

class Node:

    def __init__(self,row,col,cols,rows):
        self.row = row
        self.col = col
        self.cols = cols
        self.rows = rows
        self.visited = False
        self.start = False
        self.end = False
        self.top = True
        self.bottom = True
        self.left = True
        self.right = True

    def index(self,i,j):
        if i < 0 or j < 0 or i > self.rows - 1 or j > self.cols - 1:
            return None
        return j + i * self.rows

    def return_neighbours(self,grid):
        neighbours = []

        top_index = self.index(self.row - 1,self.col)
        bottom_index = self.index(self.row + 1,self.col)    
        right_index = self.index(self.row,self.col + 1)
        left_index = self.index(self.row,self.col - 1)
        top = grid[top_index] if top_index != None else None
        bottom = grid[bottom_index] if bottom_index != None else None
        left = grid[left_index] if left_index != None else None
        right = grid[right_index] if right_index != None else None
        
        if top and self.row > 0 and not top.visited:
            neighbours.append(top)
        if right and self.col < self.cols - 1 and not right.visited:
            neighbours.append(right)
        if bottom and self.row < self.rows - 1 and not bottom.visited:
            neighbours.append(bottom)
        if left and self.col > 0 and not left.visited:
            neighbours.append(left)

        if len(neighbours) > 0:
            return neighbours
        return None

class Visualizer:

    def __init__(self,width,row,col):
        self.IDLE_THREAD_COUNT = threading.active_count()
        self.width = width
        self.height = width
        self.row = row
        self.col = col
        self.display = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption('Press \'Space\' to Generate')
        self.grid = [Node(i,j,self.col,self.row) for i in range(self.row) for j in range(self.col)]
        self.run = True
        self.start = None
        self.end = None
        self.generated = False
        self.maze_node = self.grid[0]
        self.queue = []
        self.path = []
        self.bfs_queue = []
        self.visited = []

    def main(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if threading.active_count() <= self.IDLE_THREAD_COUNT:
                        key = pygame.mouse.get_pressed()
                        x,y = pygame.mouse.get_pos()
                        if 0 < x < self.width and 0 < y < self.height:
                            row,col = (y // (self.height // self.row),x // (self.width // self.col))
                            index = col + row * self.col
                            if key[0] and self.generated:
                                if self.start is None and index != self.end:
                                    self.start = index
                                    self.grid[index].start = True
                                elif self.end is None and index != self.start:
                                    self.end = index
                                    self.grid[index].end = True
                            elif key[2] and self.generated:
                                if self.grid[index].start:
                                   self.grid[index].start = False
                                   self.start = None
                                elif self.grid[index].end:
                                    self.grid[index].end = False
                                    self.end = None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not self.generated:
                            self.generated = True
                            thread = threading.Thread(target=self.dfs,args=[self.grid])
                            thread.start()
                        else:
                            if self.start != None and self.end != None:
                                thread = threading.Thread(target=self.bfs,args=[self.grid,self.start,self.end])
                                thread.start()
                    elif event.key == pygame.K_r:
                        self.__init__(self.width,self.row,self.col)
                    elif event.key == pygame.K_c:
                        self.visited.clear()
                        self.path.clear()
                            
            self.draw(self.display)

        pygame.quit()

    def return_neighbours(self,grid):
        neighbours = {}
        for i in range(self.row):
            for j in range(self.col):
                index = j + i * self.col
                neighbours[index] = []
                if not grid[index].top:
                    neighbour_index = j + (i - 1) * self.col
                    neighbours[index].append(neighbour_index)
                if not grid[index].bottom:
                    neighbour_index = j + (i + 1) * self.col
                    neighbours[index].append(neighbour_index)
                if not grid[index].left:
                    neighbour_index = (j - 1) + i * self.col
                    neighbours[index].append(neighbour_index)
                if not grid[index].right:
                    neighbour_index = (j + 1) + i * self.col
                    neighbours[index].append(neighbour_index)
        return neighbours

    def draw(self,win):
        win.fill((0,0,0))
        '''for node in self.queue:
            pygame.draw.rect(win,(128,0,128),(node.col * (self.width // self.col),node.row * (self.height // self.row),self.width // self.col,self.height // self.row))'''
        if self.generated:
            row,col = self.maze_node.row,self.maze_node.col
            pygame.draw.rect(win,(0,255,0),(col * (self.width // self.col),row * (self.height // self.row),self.width // self.col,self.height // self.row))
        for index in self.visited:
            node = self.grid[index]
            pygame.draw.rect(win,(255,255,0),(node.col * (self.width // self.col),node.row * (self.height // self.row),self.width // self.col,self.height // self.row))
        for index in self.path:
            node = self.grid[index]
            pygame.draw.rect(win,(175,0,175),(node.col * (self.width // self.col),node.row * (self.height // self.row),self.width // self.col,self.height // self.row))
        for index in self.bfs_queue:
            node = self.grid[index]
            pygame.draw.rect(win,(0,255,0),(node.col * (self.width // self.col),node.row * (self.height // self.row),self.width // self.col,self.height // self.row))
        if self.maze_node and not self.generated:
            row,col = self.maze_node.row,self.maze_node.col
            pygame.draw.rect(win,(0,0,0),(col * (self.width // self.col),row * (self.height // self.row),self.width // self.col,self.height // self.row))
        for node in self.grid:
            if node.start:
                pygame.draw.rect(win,(255,0,0),(node.col * (self.width // self.col),node.row * (self.height // self.row),self.width // self.col,self.height // self.row))
            elif node.end:
                pygame.draw.rect(win,(0,0,255),(node.col * (self.width // self.col),node.row * (self.height // self.row),self.width // self.col,self.height // self.row))
            if node.left:
                pygame.draw.line(win,(255,255,255),(node.col * (self.width // self.col),node.row * (self.height // self.row)),(node.col * (self.width // self.col),node.row * (self.height // self.row) + (self.height // self.row)),1)
            if node.right:
                pygame.draw.line(win,(255,255,255),(node.col * (self.width // self.col) + (self.width // self.col),node.row * (self.height // self.row)),(node.col * (self.width // self.col) + (self.width // self.col),node.row * (self.height // self.row) + (self.height // self.row)),1)
            if node.top:
                pygame.draw.line(win,(255,255,255),(node.col * (self.width // self.col),node.row * (self.height // self.row)),(node.col * (self.width // self.col) + (self.width // self.col),node.row * (self.height // self.row)),1)
            if node.bottom:
                pygame.draw.line(win,(255,255,255),(node.col * (self.width // self.col),node.row * (self.height // self.row) + (self.height // self.row)),(node.col * (self.width // self.col) + (self.width // self.col),node.row * (self.height // self.row) + (self.height // self.row)),1)    
        
        
        pygame.display.update()

    def bfs(self,grid,start,end):
        predecessorNodes = {}
        self.bfs_queue.append(start)
        neighbours = self.return_neighbours(grid)
        while self.bfs_queue:
            pygame.time.delay(30)
            if end in self.visited:
                self.bfs_queue.clear()
                self.visited.clear()
                break
            pygame.time.delay(10)
            node = self.bfs_queue.pop(0)
            for neighbour in neighbours[node]:
                if neighbour not in self.visited:
                    self.visited.append(neighbour)
                    self.bfs_queue.append(neighbour)
                    predecessorNodes[neighbour] = node
        currentNode = end
        while currentNode != start:
            currentNode = predecessorNodes[currentNode]
            if currentNode != start and currentNode != end:
                self.path.append(currentNode)
                pygame.time.delay(5)

    def dfs(self,grid):
        self.maze_node.visited = True
        self.queue = [self.maze_node]
        while self.queue:
            key = pygame.key.get_pressed()
            if key[pygame.K_s]:
                pygame.time.Clock().tick(5)
            else:
                pygame.time.Clock().tick(60)
            neighbours = self.maze_node.return_neighbours(grid)
            if neighbours:
                random_neighbour = random.choice(neighbours)
                random_neighbour.visited = True
                self.removeWall(grid,self.maze_node,random_neighbour)
                self.queue.append(self.maze_node)
                self.maze_node = random_neighbour
            else:
                if self.queue:
                    n = self.queue.pop(len(self.queue) - 1)
                    self.maze_node = n

    @staticmethod
    def removeWall(grid,node,random_neighbour):
        if node.row == random_neighbour.row + 1:
            grid[node.index(node.row,node.col)].top = False
            grid[random_neighbour.index(random_neighbour.row,random_neighbour.col)].bottom = False
        elif node.row == random_neighbour.row - 1:
            grid[node.index(node.row,node.col)].bottom = False
            grid[random_neighbour.index(random_neighbour.row,random_neighbour.col)].top = False
        elif node.col == random_neighbour.col + 1:
            grid[node.index(node.row,node.col)].left = False
            grid[random_neighbour.index(random_neighbour.row,random_neighbour.col)].right = False
        elif node.col == random_neighbour.col - 1:
            grid[node.index(node.row,node.col)].right = False
            grid[random_neighbour.index(random_neighbour.row,random_neighbour.col)].left = False
                
vis = Visualizer(750,25,25)
vis.main()
