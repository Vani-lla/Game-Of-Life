from os import path, makedirs, getcwd
from time import time
from concurrent import futures
from threading import Thread

import cv2 as cv
import numpy as np

def surroundings(ind_x, ind_y, size, grid):
   """
      Returns the sum of surroundings
   """
   s = -255 if grid[ind_y][ind_x] == 255 else 0
   
   for y in range(-1, 2):
      for x in range(-1, 2):
         xi, yi = ind_x+x, ind_y+y

         if xi < size[1] and xi >= 0 and yi < size[0] and yi >= 0:
            s += grid[yi][xi]
   return s

def future(cell, neighborhood):
   """
      Returns future of cell, according to the rules
      https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
   """
   if cell:
      if   neighborhood < 510 : return 0
      elif neighborhood < 1020: return 255
      else:                     return 0

   else:
      if   neighborhood == 765: return 255
      else:                     return 0

def full_surroundings(ind_x, ind_y, size):
   """
      Returns indexes of all surrounding cells
   """

   cells = []
   for y in range(-1, 2):
      for x in range(-1, 2):
         xi, yi = ind_x+x, ind_y+y

         if xi < size[1] and xi >= 0 and yi < size[0] and yi >= 0:
            cells.append((xi, yi))

   return cells

def opt_tick(mini_grid, grid, no, ind_correction, size):
   to_check = set()
   future_grid = np.copy(mini_grid)

   # Selecting cells to check
   for ind_y, row in enumerate(mini_grid):
      if 255 in row:
         for ind_x, cell in enumerate(row):
            if cell==255:
               full = full_surroundings(ind_x, ind_y, size)
               for ind in full:
                  to_check.add(ind)

   to_check = sorted(list(to_check), key=lambda x: x[1])

   # Generating future generation
   for ind_x, ind_y in to_check:
      try:
         future_grid[ind_y][ind_x] = future(grid[ind_y+ind_correction][ind_x], surroundings(ind_x, ind_y+ind_correction, size, grid))
      except IndexError:
         break
   
   return future_grid, no

def tick(n, grid, size):
   # Splitting main grid into n smaller ones
   arrays = np.array_split(np.copy(grid), n)
   next_grid = []

   # Starting a thread for each small grid
   with futures.ProcessPoolExecutor() as executor:
      threads = []

      ind_correction = 0
      for no, array in enumerate(arrays):
         threads.append(executor.submit(opt_tick, array, grid, no, ind_correction, size))
         ind_correction += len(array)

      for thread in futures.as_completed(threads):
         next_grid.append(thread.result())

   # Sorting generated and returning created frame
   next_grid = list(map(lambda x: x[0],sorted(next_grid, key=lambda x: x[1])))
   return np.row_stack(next_grid)

def interupt():
   global run
   while True:
      command = input()
      if command == 'stop':
         run = False
         break
      elif command == 'times':
         print(f'Average time per frame: {sum(times)/len(times):3f}s')
   return

if __name__ == '__main__':
   # Creating an empty directory, if it doesn't already exist
   dir_path = path.join(getcwd(), 'frames')
   if not path.exists(dir_path): makedirs(dir_path)

   # First Frame
   first_frame = cv.imread('start.png')
   *size, _ = first_frame.shape
   grid = np.array([[cell[0] for cell in row] for row in first_frame])
   
   # Creating frames
   Thread(target=interupt).start()

   start, run, n, times = time(), True, 0, []
   while run:
      s_ = time()
      cv.imwrite(f'./frames/frame{n}.png', grid)
      grid = tick(16, grid, size)
      n += 1
      times.append(time()-s_)

   print(f'{time()-start:3f}s')

   input()