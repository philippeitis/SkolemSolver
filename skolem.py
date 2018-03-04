import itertools

def numpair_validation(k):
    if k%4 == 2 or k%4 == 3:
        return
    return k

def numpair_gen(k):
    
    numpair = []         
    perm_dict = {}
    i = 0
    del_key = []
    key_arr = []

    # generates array of permutatable values
    
    for n in range(1,k+1):
        numpair.append(n)

    # generates all possible orderings of the skolem
    array = itertools.permutations(numpair)

    # uses a dict for convenience
    for perm in array:
        key_arr.append(i)
        perm_dict[i] = perm
        i += 1
        
    perm_arr = list(perm_dict.values())
    
    return perm_arr
    
def skolem_gen(numpair, k):
    
    # generates an empty array of false values.
    
    skolem = [False] * 2 * k

    for i in reversed(numpair):
        for n in range(len(skolem)):
            if n+i < len(skolem):

                # if the values are empty, place an object in there
                
                if skolem[n] == False:
                    if skolem[n+i] == False:
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
         return("No possible skolem pairs exist.")

    # if output is possible, we go ahead and have some fun. well,
    # the computer isn't having fun, but yes.
    
    perm_arr = numpair_gen(k)
    skolem_arr = []

    for perm in perm_arr:
        skolem = skolem_gen(perm, k)
        if skolem:
            if not skolem in skolem_arr:
                skolem_arr.append(skolem)
                skolem_arr.append(skolem[::-1])

    if not skolem_arr:
        return("No possible skolem pairs exist.")

    return len(skolem_arr)

for i in range(1,11):
    print(everything(userinput(i)))
