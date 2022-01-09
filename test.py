import concurrent.futures

def squares(i):
   for x in range(i):
      x**i

if __name__ == '__main__':
   with concurrent.futures.ProcessPoolExecutor() as executor:
      processes = [executor.submit(squares, 10_000) for _ in range(24)]