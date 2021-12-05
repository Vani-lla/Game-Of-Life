import pygame
from pygame import *
from random import randint
from threading import Thread
from time import sleep

win = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Game Of Life - John Horton Conway')

render_list = []
rect_size = 100
scale = 1
drag = False
start_x, start_y = 0, 0
vector_x, vector_y = 0, 0
old_vector_x, old_vector_y = 0, 0

def render():
   size = rect_size*scale
   win.fill((13, 59, 80))

   for row in render_list:
      for cell in row:
         cell.render(size)

   pygame.display.update()

class Cell():
   def __init__(self, x, y, ind_x, ind_y, alive):
      self.x = x
      self.y = y

      self.ind_x = ind_x
      self.ind_y = ind_y

      self.alive = alive

   def render(self, size):
      x = int(self.x*scale)+1+vector_x
      y = int(self.y*scale)+1+vector_y
      if x > 0 and x < 1280 and y > 0 and y < 720:
         if self.alive:
            pygame.draw.rect(win, (247, 127, 0), (x, y, size, size))
         else:
            pygame.draw.rect(win, (13, 59, 102), (x, y, size, size))

   def surroundings(self):
      l = []
      for y in range(-1, 2):
         ll = []

         for x in range(-1, 2):
            xi, yi = self.ind_x + x, self.ind_y + y

            if xi >= 0 and yi >= 0 and xi < len(render_list[0]) and yi < len(render_list):
               ll.append(render_list[yi][xi])

         l.append(ll)
      return l

   def surr_sum(self, surroundings):
      s = 0
      for row in surroundings:
         for cell in row:
           s += cell.alive
      return s-1

   def future(self):
      s = self.surr_sum(self.surroundings())

      if self.alive:
         if s < 2:               return 0
         elif s == 2 or s == 3:  return 1
         elif s > 3:             return 0
      else:
         if s == 3:              return 1

      return 0

def tick():
   global render_list
   # cell_check = set()
   # for row in render_list:
   #    for cell in row:
   #       if cell.alive: cell_check.add(cell)

   # for cell in list(cell_check)[:]:
   #    for row in cell.surroundings():
   #       for cell_ in row:
   #          cell_check.add(cell_)

   # cells = list(cell_check)

   size = rect_size*scale

   r = render_list[:]

   for row in r:
      for cell in row:
         cell.alive = cell.future()

for ind_y, y in enumerate(range(0, 500, rect_size)):
   l = []
   for ind_x, x in enumerate(range(0, 500, rect_size)):
      l.append(Cell(x, y, ind_x, ind_y, 0))

   render_list.append(l)
   render()
   sleep(1)

def dragMove():
   global vector_x, vector_y
   while run:
      if drag:
         pos = pygame.mouse.get_pos()

         vector_x = -(start_x - old_vector_x) + pos[0]
         vector_y = -(start_y - old_vector_y) + pos[1]

         render()

def map_print():
   for row in render_list:
      l = []
      for cell in row:
         l.append(cell.alive)
      print(l)
   print()

render_list[2][0].alive = 1
render_list[2][1].alive = 1
render_list[2][2].alive = 1

map_print()

render()

run = True
Thread(target=dragMove).start()
while run:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         run = False
         break

      elif event.type == pygame.KEYDOWN:
         if event.key == pygame.K_ESCAPE:
            run = False
            break

         elif event.key == pygame.K_SPACE:
            tick()
            render()
      
      elif event.type == pygame.MOUSEWHEEL:
         if event.y == 1: 
            if scale < 0.2:  scale += 0.05
            else:             scale += 0.1
         elif event.y == -1 and scale > 0.1:
            if scale < 0.2:  scale -= 0.05
            else:             scale -= 0.1

         scale = round(scale, 3)
         render()

      elif event.type == pygame.MOUSEBUTTONDOWN:
         pos = pygame.mouse.get_pos()
         start_x, start_y = pos[0], pos[1]
         drag = True

      elif event.type == pygame.MOUSEBUTTONUP:
         drag = False
         old_vector_x, old_vector_y = vector_x, vector_y