import time #this is a Python library

def time_execution(code):
   start = time.clock()  # start the clock
   result = eval(code)  # evaluate any string as if it is a Python command
   run_time = time.clock() - start  # find difference in start and end time
   return result, run_time  # return the result of the code and time taken
CUBE_SIZE=4   #length of edge of cube
J3={1,3,5,7,9,10,11,12,14,16,17,18,20,21,23,24,25}
J4={1,4,5,8,9,10,11,12,14,15,16,17,18,19,21,22,25,26,28,30,33,34,36,37,38,39,40,41,42,43,44,45,48,49,52,53,56,59,62}
#the set of joints of the snake
J=J4
directions=[(1,0,0),(0,1,0),(0,0,1),(-1,0,0),(0,-1,0),(0,0,-1)]
initialpos=[(1,0,0),(0,0,0),(1,1,0),(1,1,1)] #possible starting points (without symmetries) on a 4-cube)
L=[initialpos[0]] #List of positions
n=0 #length of iterated snake
d=0 # number of direction
D=[0] #list of directions
j=0 #number of selected initialposition
def in_cube(n):  #to form the cube
    cube=set()
    for i in range(0,n):
        for j in range(0,n):
            for k in range(0,n):
                cube.add((i,j,k))
    return cube

cube= in_cube(CUBE_SIZE)
#print cube, len(cube), J
s=0 #number of solutions
i=0 # number of steps
start = time.clock()

# sum_of: sums two list component wise
def sum_of(a,b):
    return (a[0]+b[0],a[1]+b[1],a[2]+b[2])

#change_initialpos:
#when all possibilities of one initialposition are checked, jump to next one
def change_initialpos(j,Di,di):
    # Why does this function take Di and di as arguments when it
    # doesn't use the values?
    di=0
    Di=[0]
    run_time = time.clock() - start
    print run_time
    print 'New Position'
    if j<3:
        j+=1
        L= [initialpos[j]]
        return (L,Di,di,j)
    else:
        j+=1
        print 'All checked'
        return ([],Di,di,j)

#Lcube, K: the inverse of L in the cube
def Lcube(cube,L):
    SL=set()
    for l in L:
        SL.add(l)
    K=cube-SL
    return K

#pappend: a help procedure to check connectedness
def pappend(K,P):
    # This iterates over P while changing it.  In this case it seems
    # that this works in Python, and it actually works in your favor,
    # but I'm not sure you're actually aware of what's exactly going
    # on.
    #
    # Also, why is P a list?  Aren't we supposed to convert to sets?
    # Of course the iteration probably won't work anymore like this
    # with sets.
    for p in P:
        for e in directions:
            p= sum_of(p,e)
            if p in K and p not in P:
                P.append(p)
    return P

#connected: checks if K is connected, if that is not the case, this path will be abandoned
def connected(K,p):
    if p in K:
        P=[p]
        # You're evaluating pappend twice here, with the same
        # arguments, and what's worse is that pappend is not pure: it
        # modifies P, and then also returns it.  Which also means that
        # the condition in this while will never be true.  The reason
        # your code still works is that, as I mentioned above, you're
        # appending to P while iterating over it, and the iteration
        # continues over the items that you've appended.  But it's
        # very difficult to understand and obscure.
        while P != pappend(K,P):
            P=pappend(K,P)
        return K == set(P)
    else:
        return False

#dead_end: If K has 3 or more dead ends, the path will be abandoned
def dead_end(K,p):
    a=0
    for k in K:
        if k!=p:
            E=[k]

            for e in directions:
                x=sum_of(k,e)
                if x in K:
                    E.append(x)
            if len(E)<3:
                a+=1
                if a>1:
                    return True
    return False

#change direction:
#whenever a step fails, the direction gets changed or the snake steps back (shorten the list L)
def change_direction(Li,Di,di,j):
    #print 'change'

    # Should this really be D, and not Di?
    if D !=[]:
        while (di+1)%6 == Di[-1]:
            Li.pop()
            di=Di.pop()
            #print 'pop'

            if Di==[]:
                return change_initialpos(j,Di,di)

            while len(Li) not in J:
                Li.pop()
                di=Di.pop()
                #print 'pop2'

            else:
                (Li,Di,di,j)= change_direction(Li,Di,di,j)
            return (Li,Di,di,j)
        else:
            # You have random whitespace in your code.  Why is there a
            # space before the + here?
            di = (di +1)%6
            return (Li,Di,di,j)
    else:
        return change_initialpos(j,Di,di)


#steps: either adds one position to the List L (the snake), or removes one, combined with
def steps(Li,Di,di,j): # main procedure
    n=len(Li)

    p=sum_of(Li[-1], directions[di])
    K = Lcube(cube,Li)

    if p in K:# and (n<20 or (not dead_end(K,p) and connected(K,p))):

        Li.append(p)
        Di.append(di)

        if (n+1) in J:
            di= (di+1)%6
    else:
        if n in J:
            (Li,Di,di,j)=change_direction(Li,Di,di,j)
        else:
            #print (Li,Di,di,j)
            while len(Li) not in J:
                Li.pop()
                if Li==[]:
                    return change_initialpos(j,Di,di)
                else:
                    Di.pop()

            (Li,Di,di,j)=change_direction(Li,Di,di,j)
    return (Li,Di,di,j)
#main loop
while n in range(0,CUBE_SIZE**3+1):
    (L,D,d,j)= steps(L,D,d,j)
    n=len(L)
    i +=1
    if i%100000==0:
        print(i)
        run_time = time.clock() - start
        print run_time, run_time*1000/i
        print (L,len(L),D,i,j)
    if len(L)== CUBE_SIZE**3:
        s+=1
        print ('Solution!')
        print s
        print (L,len(L),D,i,j)
        run_time = time.clock() - start
        print run_time, run_time*1000/i

    if j>3:
        print 'All possibilities checked, solutions found:'
        print s
        run_time = time.clock() - start
        print run_time
        break
