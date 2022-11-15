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
        self.top = True
        self.bottom = True
        self.left = True
        self.right = True

    def index(self,i,j):
        if i < 0 or j < 0 or i > self.rows - 1 or j > self.cols - 1:
            return None
        return j + i * self.cols

    def return_random_neighbour(self,grid):
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
        if bottom and self.row < self.rows - 1 and  not bottom.visited:
            neighbours.append(bottom)
        if left and self.col > 0 and not left.visited:
            neighbours.append(left)

        if len(neighbours) > 0:
            index = random.randint(0,len(neighbours) - 1)
            r = neighbours[index]
            return r
        return None

class Visualizer:

    def __init__(self,width,row,col):
        self.width = width
        self.height = width
        self.row = row
        self.col = col
        self.display = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption('Press \'Space\' to Generate')
        self.grid = [Node(i,j,self.col,self.row) for i in range(self.row) for j in range(self.col)]
        self.run = True
        self.queue = []

    def main(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        thread = threading.Thread(target=self.dfs,args=[self.grid,self.grid[0]])
                        thread.start()
                        
            self.draw(self.display)

        pygame.quit()

    def draw(self,win):
        win.fill((0,0,0))
        for node in self.queue:
            pygame.draw.rect(win,(128,0,128),(node.col * (self.width // self.col),node.row * (self.height // self.row),self.width // self.col,self.height // self.row))
        
        if any(self.queue):
            curr = self.queue[-1]
            pygame.draw.rect(win,(75,0,130),(curr.col * (self.width // self.col),curr.row * (self.height // self.row),self.width // self.col,self.height // self.row))
        for node in self.grid:
            if node.left:
                pygame.draw.line(win,(255,255,255),(node.col * (self.width // self.col),node.row * (self.height // self.row)),(node.col * (self.width // self.col),node.row * (self.height // self.row) + (self.height // self.row)))
            if node.right:
                pygame.draw.line(win,(255,255,255),(node.col * (self.width // self.col) + (self.width // self.col),node.row * (self.height // self.row)),(node.col * (self.width // self.col) + (self.width // self.col),node.row * (self.height // self.row) + (self.height // self.row)))
            if node.top:
                pygame.draw.line(win,(255,255,255),(node.col * (self.width // self.col),node.row * (self.height // self.row)),(node.col * (self.width // self.col) + (self.width // self.col),node.row * (self.height // self.row)))
            if node.bottom:
                pygame.draw.line(win,(255,255,255),(node.col * (self.width // self.col),node.row * (self.height // self.row) + (self.height // self.row)),(node.col * (self.width // self.col) + (self.width // self.col),node.row * (self.height // self.row) + (self.height // self.row)))    
        pygame.display.update()

    def dfs(self,grid,node):
        node.visited = True
        self.queue = [node]
        while self.queue:
            pygame.time.delay(100)
            random_neighbour = node.return_random_neighbour(grid)
            if random_neighbour != None:
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
                random_neighbour.visited = True
                node = random_neighbour
                self.queue.append(node)
            else:
                if self.queue:
                    n = self.queue.pop(len(self.queue) - 1)
                    node = n
                
vis = Visualizer(750,15,15)
vis.main()
