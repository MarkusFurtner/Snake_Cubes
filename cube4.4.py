import time

CUBE_SIZE = 4  # length of edge of cube
PADDED_SIZE = CUBE_SIZE + 2
J2 = [1,2,3,4,5,6,7,8]
J3b= [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27]
J3 = [1, 3, 5, 7, 9, 10, 11, 12, 14, 16, 17, 18, 20, 21, 23, 24, 25, 27]
J4 = [1, 4, 5, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 21, 22, 25, 26, 28, 30,
      33, 34, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 48, 49, 52, 53, 56, 59, 62,64]
J5 = [1, 4, 5, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 21, 22, 25, 26, 28, 30,
      33, 34, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 48, 49, 52, 53, 56, 59, 62, 64,
      65, 67,68,71,72,73,77,78,82,83,87,88,92,93,97,101,102,105,106,109,110,113,114,117,118,121,122,125]
knots3 = [[[3,4,3],[4,5,4],[3,4,3]],
          [[4,5,4],[5,6,5],[4,5,4]],
          [[3,4,3],[4,5,4],[3,4,3]]]
knots4 = [[[3,4,4,3],[4,5,5,4],[4,5,5,4],[3,4,4,3]],
          [[4,5,5,4],[5,6,6,5],[5,6,6,5],[4,5,5,4]],
          [[4,5,5,4],[5,6,6,5],[5,6,6,5],[4,5,5,4]],
          [[3,4,4,3],[4,5,5,4],[4,5,5,4],[3,4,4,3]]]         
# the set of joints of the snake
if CUBE_SIZE == 3:
    J_list = J3
    knots=knots3
elif CUBE_SIZE == 4:
    J_list = J4
    knots=knots4
elif CUBE_SIZE == 2:
    J_list = J2
elif CUBE_SIZE == 5:
    J_list = J5
else:
    raise(Exception("Error: Cube size not supported"))

def coords_to_index((x,y,z)):
    return (x * PADDED_SIZE + y) * PADDED_SIZE + z

def index_to_coords(i):
    return ((i // (PADDED_SIZE**2)) % PADDED_SIZE, (i // PADDED_SIZE) % PADDED_SIZE, i % PADDED_SIZE)

directions = [(-1, 0, 0), (0, -1, 0), (0, 0, -1),
              (1, 0, 0), (0, 1, 0), (0, 0, 1)]
offset_directions = map(coords_to_index, directions)

# possible starting points (without symmetries) on a 4-cube)
initialpos = map(coords_to_index, [(1, 1, 1), (2, 1, 1), (2, 2, 1), (2, 2, 2)])


start = time.clock()

# sum_of: sums two list component wise
def sum_of((ax, ay, az), (bx, by, bz)):
    return (ax+bx, ay+by, az+bz)

num_steps = 0
def count_step():
    global num_steps
    num_steps += 1
    if num_steps % 1000000 == 0:
        print(num_steps)
        run_time = time.clock() - start
        print run_time, run_time * 1000 / num_steps

def compute_successor_directions(d):
    return [n for n in range(len(directions)) if n != d]

successor_directions = [compute_successor_directions(d) for d in range(len(directions))]

def coords_valid((x,y,z)):
    return x >= 1 and x <= CUBE_SIZE and y >= 1 and y <= CUBE_SIZE and z >= 1 and z <= CUBE_SIZE

# K: the set of free positions
# Li: the list of positions occupied by the snake
# Di: the list of directions taken by the snake
# j: the index into J_list to which to advance in the next step
def recurse(K, Li, Di, j):
    count_step()

    length_so_far = len(Li)
    # if the cube is full, we're done
    if length_so_far == CUBE_SIZE**3:
        print("solution!")
        print(map(index_to_coords, Li), Di, j)
        return

    # which directions do we try next?
    if length_so_far == 1:
        # if we're at the initial position, we try all directions
        next_directions = range(len(directions))
    else:
        # otherwise the directions allowed to come after the last one 
        next_directions = successor_directions[Di[-1]]

    # how many snake elements in this step?
    num_elements = J_list[j] - J_list[j-1]

    for d in next_directions:
        n = 0
        for i in range(num_elements):
            p = Li[-1] + offset_directions[d]
            # FIXME: also check dead_end
            if K[p]:
                # position already occupied - undo
                break
            # occupy the position
            Li.append(p)
            K[p] = True
            Di.append(d)
            n += 1
        if n == num_elements:
            # we got all the way through our elements, so recurse
            recurse(K, Li, Di, j+1)
        # undo the positions we occupied
        for i in range(n):
            p = Li.pop()
            K[p] = False
            Di.pop()

def main():
    for p in initialpos:
        K = [not coords_valid(index_to_coords(i)) for i in range(PADDED_SIZE**3)]
        K[p] = True
        recurse(K, [p], [], 1)

if __name__ == "__main__":
    main()
