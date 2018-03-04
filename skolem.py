import itertools
import time
import io
import sys

def numpair_validation(k):
    if k%4 == 2 or k%4 == 3:
        return
    return k

def numpair_gen(k):
    
    numpair = []         
    perm_arr = []
    # generates array of permutatable values
    
    for n in range(1,k+1):
        numpair.append(n)

    # generates all possible orderings of the skolem
    array = itertools.permutations(numpair)

    # uses a dict for convenience
    for perm in array:
        perm_arr.append(perm)
    
    return perm_arr

def numpair_filter(perm_arr):
    
    perm_dict = {}
    i = 0
    key_arr = []
        
    for perm in perm_arr:
        key_arr.append(i)
        perm_dict[i] = perm
        i += 1

    # removes all lists with a value n followed by n-1, as the second term
    # both values would overlap. this prolly saves computing time. i think.
    # maybe.
    
    for key in key_arr:
        
        eval_perm = perm_dict[key]
        
        if len(eval_perm) > 1:
            if eval_perm[0]-1 == eval_perm[1]:
                del perm_dict[key]
        
    perm_arr = list(perm_dict.values())
    
    return perm_arr
        
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

def everything(k, arg = 0):
    if not k:
         return(0)

    # if output is possible, we go ahead and have some fun. well,
    # the computer isn't having fun, but yes.
    
    if arg == 0:
        perm_arr = numpair_filter(numpair_gen(k))

    elif arg == 1:
        perm_arr = numpair_gen(k)

    skolem_arr = []
    x = 0

    for perm in perm_arr:
        skolem = skolem_gen(perm, k)
        if skolem:
            x += 1
    return x

file_path = "executiontime.txt"
arg = 0

for arg in range(2):
    for i in range(1,12):
        time_start = time.time()
        x = everything(userinput(i), arg)
        time_elapsed = time.time()-time_start
        file = open(file_path, "a")
        file.write("\n" + str(arg) + ", " + str(i) + ", " + str(x) + ", " + str(time_elapsed))
        file.close()

