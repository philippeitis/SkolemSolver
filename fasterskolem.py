import time
import io
import sys

def numpair_validation(k):
    if k%4 == 2 or k%4 == 3:
        return
    return k

def permutations (numpair):
    if not isinstance(numpair, list):
        numpair = list(numpair)

    yield numpair

    if len(numpair) == 1:
        return

    for n in numpair:
        new_list = numpair[:]
        pos = new_list.index(n)
        del(new_list[pos])
        new_list.insert(0, n)
        for resto in permutations(new_list[1:]):
            if new_list[:1] + resto != numpair:
                yield new_list[:1] + resto

def numpair_gen(k):
    
    # generates array of permutatable values
    numpair = []
    for n in range(1,k+1):
        numpair.append(n)    
    return numpair

def numpair_filter(perm):
          
    if len(perm) > 1:
        if perm[0]-1 == perm[1]:
            return
    
    return perm
        
def skolem_gen(numpair, k):
    # generates an empty array of false values.
    skolem = [False] * 2 * k

    for i in numpair:
        for n in range(len(skolem)):
            if n+i < len(skolem):

                # if the values are empty, place an object in there
                
                if skolem[n] == False:
                    skolem[n] = i; skolem[n+i] = i
                    break
                    
    if not False in skolem:
        return skolem

def userinput(k = None):
    if not k:
        k = int(input("Skolem Ordering: "))

    k = numpair_validation(k)

    return(k)

def everything(k):
    if not k:
         return(0)

    # if output is possible, we go ahead and have some fun. well,
    # the computer isn't having fun, but yes.

    x = 0

    for perm in permutations(numpair_gen(k)):
        perm = numpair_filter(perm)
        if perm:
            skolem = skolem_gen(perm, k)
            if skolem:
                x += 1
    return x

file_path = "executiontimef.txt"

for i in range(1,13):
    time_start = time.time()
    x = everything(userinput(i))
    time_elapsed = time.time()-time_start

    file = open(file_path, "a")
    file.write("\n" + str(i) + ", " + str(x) + ", " + str(time_elapsed))
    file.close()

