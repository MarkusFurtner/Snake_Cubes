import time  # this is a Python library

CUBE_SIZE = 4  # length of edge of cube
J2 = {1,2,3,4,5,6,7,8}
J3b= {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27}
J3 = {1, 3, 5, 7, 9, 10, 11, 12, 14, 16, 17, 18, 20, 21, 23, 24, 25, 27}
J4 = {1, 4, 5, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 21, 22, 25, 26, 28, 30,
      33, 34, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 48, 49, 52, 53, 56, 59, 62,64}
J5 = {1, 4, 5, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 21, 22, 25, 26, 28, 30,
      33, 34, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 48, 49, 52, 53, 56, 59, 62, 64,
      65, 67,68,71,72,73,77,78,82,83,87,88,92,93,97,101,102,105,106,109,110,113,114,117,118,121,122,125}
knots3 = [[[3,4,3],[4,5,4],[3,4,3]],
          [[4,5,4],[5,6,5],[4,5,4]],
          [[3,4,3],[4,5,4],[3,4,3]]]
knots4 = [[[3,4,4,3],[4,5,5,4],[4,5,5,4],[3,4,4,3]],
          [[4,5,5,4],[5,6,6,5],[5,6,6,5],[4,5,5,4]],
          [[4,5,5,4],[5,6,6,5],[5,6,6,5],[4,5,5,4]],
          [[3,4,4,3],[4,5,5,4],[4,5,5,4],[3,4,4,3]]]         
# the set of joints of the snake
if CUBE_SIZE == 3:
    J = J3
    knots=knots3
elif CUBE_SIZE == 4:
    J = J4
    knots=knots4
elif CUBE_SIZE == 2:
    J=J2
elif CUBE_SIZE == 5:
    J=J5
          
else:
    raise(Exception("Error: Cube size not supported"))

directions = [(1, 0, 0), (0, 1, 0), (0, 0, 1),
              (-1, 0, 0), (0, -1, 0), (0, 0, -1)]
# possible starting points (without symmetries) on a 4-cube)
initialpos = [(1, 0, 0), (0, 0, 0), (1, 1, 0), (1, 1, 1)]


def in_cube(n):  # to form the cube
    c = set()
    for i in range(0, n):
        for j in range(0, n):
            for k in range(0, n):
                c.add((i, j, k))
    return c

cube = in_cube(CUBE_SIZE)

start = time.clock()

# sum_of: sums two list component wise

def sum_of((ax, ay, az), (bx, by, bz)):
    return (ax+bx, ay+by, az+bz) 

def free_neighbors(K,p):
    i=0
    for e in directions:
        if sum_of(p,e) in K:
            i +=1
    return i
def position_of(L,p):
    for n in range(0,len(L)):
        if L[n]==p:
            return n
            
def referencelist(K,L):
    for p in K:
        knots[p[0]][p[1]][p[2]]=free_neighbors(K,p)
    for p in L:
        knots[p[0]][p[1]][p[2]]= -1 - position_of(L,p)
    return knots    

print referencelist(cube,[])
print free_neighbors(cube,(1,0,0)) 

def update_referencelist(knots,K,p):
    knots[p[0]][p[1]][p[2]]=free_neighbors(K,p)
    return knots

#print update_referencelist(knots,set(initialpos),(2,0,0))
# change_initialpos:
# when all possibilities of one initialposition are checked, jump to next one
def change_initialpos(j):
    di = 0
    Di = [0]
    print time.clock() - start
    print 'New Position'
    if j < 3:
        j += 1
        L = [initialpos[j]]
        return (L, Di, di, j)
    else:
        j += 1
        print 'All checked'
        return ([], Di, di, j)


# pappend: a help procedure to check connectedness
def transitive(K, initial):
    P = set([initial])
    worklist = [initial]
    for p in worklist:
        for e in directions:
            q = sum_of(p, e)
            if q in K and q not in P:
                P.add(q)
                worklist.append(q)
    return P

# connected: checks if K is connected, if that is not the case, this path
# will be abandoned


def connected(K, p):
    if p in K:
        return K == transitive(K, p)
    else:
        return False
#print transitive (cube-set([(0,0,0),(1,0,0)]),(2,0,0))       
#print connected(cube-set([(1, 0, 0), (1, 1, 0), (1, 2, 0), (1, 2, 1), (1, 2, 2), (1, 1, 2), (1, 0, 2)]),(2,2,0))
# dead_end: If K has 3 or more dead ends, the path will be abandoned


def dead_end(K, p):
    a = 0
    for k in K:
        if k != p:
            num_empty_neighbors = 0
            for e in directions:
                x = sum_of(k, e)
                if x in K:
                    num_empty_neighbors += 1
            if num_empty_neighbors < 2:
                a += 1
                if a > 1:
                    return True
    return False


# change direction:
# whenever a step fails, the direction gets changed or the snake steps
# back (shorten the list L)


def change_direction(Li, Di, di, j):
    
    if Di != []:
        while (di + 1) % 6 == Di[-1]:
            Li.pop()
            di = Di.pop()
            #print 'pop'

            if Di == []:
                return change_initialpos(j)

            while len(Li) not in J:
                Li.pop()
                di = Di.pop()
                #print 'pop2'

            return change_direction(Li, Di, di, j)

        di = (di + 1) % 6
        return (Li, Di, di, j)
    else:
        return change_initialpos(j)


# steps: either adds positions to the List L (the snake), or removes
# one, combined with
def steps(Li, Di, di, j):# main procedure
    n= len(Li)
    
    K = cube - set(Li)
    p = sum_of(Li[-1], directions[di])
    
    #if p in K and not connected(K,p):
     #   print 'isolated'
    #if dead_end(K,p):
     #   print 'deadend'
    if p not in K or dead_end(K,p) or not connected(K,p):
        while n == CUBE_SIZE**3:
            Li,Di,di,j=change_direction(Li, Di, di, j)
            n=len(Li)
         
        #print 'loop1'    
        return change_direction(Li, Di, di, j)
    while p in K:
        Li.append(p)
        Di.append(di)
        K = cube - set(Li)
        if len(Li) in J:
            di = (di + 1) % 6
            #print 'forward'
            return (Li, Di, di, j)
            
        p = sum_of(Li[-1], directions[di])    
        if p not in K:
            while len(Li) >n:
                Li.pop()
                Di.pop()
            #print 'loop3'             
            return change_direction(Li, Di, di, j)
    while len(Li) not in J:
        Li.pop()
        Di.pop()
    return change_direction(Li, Di, di, j)    
            


def main():
    L = [initialpos[0]]  # List of positions
    n = 0  # length of iterated snake
    d = 0  # number of direction
    D = [0]  # list of directions
    j = 0  # number of selected initialposition
    s = 0  # number of solutions
    i = 0  # number of steps

    while n in range(0, CUBE_SIZE**3 + 1):
        (L, D, d, j) = steps(L, D, d, j)
        n = len(L)
        i += 1
        if i % 1000000 == 0:
            print(i)
            run_time = time.clock() - start
            print run_time, run_time * 1000 / i
            print (L, len(L), D, i, j)  
        #if i>100:
         #   break
        if len(L) == CUBE_SIZE**3:
            s += 1
            print ('Solution!')
            print s
            print (L, len(L), D, i, j)
            run_time = time.clock() - start
            print run_time, run_time * 1000 / i

        if j > 3:
            print 'All possibilities checked, solutions found:'
            print s
            run_time = time.clock() - start
            print run_time
            break

if __name__ == "__main__":
    main()
