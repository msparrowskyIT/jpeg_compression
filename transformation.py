import math

cos_array = [[math.cos((2*i+1)*j * math.pi/16) for j in range(8)] for i in range(8)]
root2_inv = 1 / math.sqrt(2)
block_indexes = [(i,j) for i in range(8) for j in range(8)]

def dct(block_array,u,v):
  r = 0
  for i,j in block_indexes:
    r += block_array[i][j] * cos_array[i][u] * cos_array[j][v]
  if u == 0:
      r *= root2_inv
  if v == 0:
      r *= root2_inv
  r *= 0.25
  return r

def idct(block_array,i,j):
  r = 0
  for u,v in block_indexes:
    c = block_array[u][v] * cos_array[i][u] * cos_array[j][v]
    if u == 0:
        c *= root2_inv
    if v == 0:
        c *= root2_inv
    r += c
  r *= 0.25
  return round(r)

def shiftBy128(c):
  c -= 128
  return c

def unshiftBy128(c):
  c += 128
  if c > 255:
      c = 255
  elif c < 0:
      c = 0
  return c

def encode(block_array, quality_array):
  block_array = [[shiftBy128(c) for c in row] for row in block_array]
  block_array = [[dct(block_array,u,v) for v in range(8)] for u in range(8)]
  block_array = [[round(a/q) for a,q in zip(a,q)] for a,q in zip(block_array, quality_array)]
  return block_array

def decode(block_array, quality_array):
  block_array = [[a*q for a,q in zip(a,q)] for a,q in zip(block_array, quality_array)]
  block_array = [[idct(block_array,i,j) for j in range(8)] for i in range(8)]
  block_array = [[unshiftBy128(c) for c in row] for row in block_array]
  return block_array