from glob import glob
from os import getcwd, makedirs, path
from time import asctime, localtime, perf_counter

import cv2 as cv
import numpy as np
from numba import njit, vec
from numba.typed import List

@vectorize([np.])
def future(a, b, c, d, e, f, g, h, cell):
   surroundings = a+b+c+d+e+f+g+h+i+j

   if cell == 255:
      if surroundings != 510 and surroundings != 765:  # 2*255 3*255
            return 0
   else:
      if surroundings == 765:  # 3*255
            return 255

@njit()
def tick(grid: np.array, cells: set, height: int, width: int, n: int):
   future_grid = np.copy(grid)

   f = []
   for ind_x, ind_y in cells:
      surroundings = grid[(ind_y-1) % height, (ind_x-1) % width] + grid[(ind_y-1) % height, ind_x % width] + grid[(ind_y-1) % height, (ind_x+1) % width] + grid[ind_y % height, (ind_x-1) %
      width] + grid[ind_y % height, (ind_x+1) % width] + grid[(ind_y+1) % height, (ind_x-1) % width] + grid[(ind_y+1) % height, ind_x % width] + grid[(ind_y+1) % height, (ind_x+1) % width]

      f.append(surroundings)

      if grid[ind_y % height, ind_x % width] == 255:
         if surroundings != 510 and surroundings != 765:  # 2*255 3*255
               future_grid[ind_y % height, ind_x % width] = 0
      else:
         if surroundings == 765:  # 3*255
               future_grid[ind_y % height, ind_x % width] = 255

   return future_grid

def new_cells(grid, cells, width, height):
   cells = list((ind_x, ind_y) for ind_x, ind_y in cells if grid[ind_y % height, ind_x % width] == 255)
   future_cells = set()

   for ind_x, ind_y in cells:
      for y in range(-1, 2):
         for x in range(-1, 2):
               future_cells.add((ind_x+x, ind_y+y))

   return future_cells


if __name__ == '__main__':
   # Creating an empty directory, if it doesn't already exist
   dir_path = path.join(getcwd(), 'frames')
   if not path.exists(dir_path):
      makedirs(dir_path)

   dir_path = path.join(getcwd(), 'logs')
   if not path.exists(dir_path):
      makedirs(dir_path)

   frames = [path for path in sorted(
      glob('frames/frame*.png'), key=lambda path: int(path[12:].split('.')[0]))]
   resume = input(
      f"Do you want to resume from the last frame? ({len(frames)-1}) (y/n) ") if len(frames) else 0

   # First Frame
   if not resume == 'y':
      first_frame = cv.imread('start_.png')
      height, width, _ = first_frame.shape
      grid = np.array([[cell[0] for cell in row]
                     for row in first_frame], dtype='int16')
      n, start_num = 0, 0
   else:
      first_frame = cv.imread(frames[-1])
      height, width, _ = first_frame.shape
      grid = np.array([[cell[0] for cell in row]
                     for row in first_frame], dtype='int16')
      n, start_num = len(frames), len(frames)

   del frames

   # Selecting cells
   cells = set()

   for ind_y, row in enumerate(grid):
      if 255 in row:
         for ind_x, cell in enumerate(row):
               if cell == 255:
                  for y in range(-1, 2):
                     for x in range(-1, 2):
                           # All cells surranding, including the central one
                           cells.add((ind_x+x, ind_y+y))

   # print(grid, len(grid), width, height, len(cells))

   start = perf_counter()
   cv.imwrite(f'frames/frame{0}.png', grid)
   grid = tick(grid, List(cells), height, width, 1)
   cells = new_cells(grid, cells, width, height)
   print(perf_counter()-start)

   start = perf_counter()
   for n in range(1, 10):
      cv.imwrite(f'frames/frame{n}.png', grid)
      grid = tick(grid, List(cells), height, width, 1)
      cells = new_cells(grid, cells, width, height)
   print(perf_counter()-start)
