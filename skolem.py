import itertools
import time
import io
import sys
import cProfile

def userinput(k = None): # usually called only once
    
    if isinstance(k,int):
        return input_validation(k)
    
    while True:
        try:
            k = int(input("Skolem Ordering: "))
            return input_validation(k)
        except ValueError:
            print("Enter a valid integer.")
                  
def input_validation(k):
    if k%4 == 2 or k%4 == 3:
        return
    if k < 1:
        return
    return k

def permutation_gen(k):
    
    perm_initial = list(range(1,k+1))
    perm_arr = []

    # generates all possible orderings of the skolem
    
    for perm in itertools.permutations(perm_initial):
        yield(perm)
    
def permutation_filter(perm_arr):

    if len(perm_arr) == 1:
        return perm_arr
    
    key_arr = list(range(len(perm_arr)))
    perm_dict = dict((key, value) for (key, value) in zip(key_arr, perm_arr))
    
    # removes all lists with a value n followed by n-1, as the second term
    # both values would overlap. this prolly saves computing time. i think.
    # maybe.

    # it removes about (n-1)! * 2n calculations or smth 

    for key in key_arr:

        eval_perm = perm_dict[key]

        if eval_perm[0]-1 == eval_perm[1]:
            del perm_dict[key]

    perm_arr = list(perm_dict.values())

    return perm_arr

def skolem_gen(perm, k):
    
    k2 = 2 * k
    
    # generates an empty array of false values.
    
    skolem = [False] * k2 

    for i in perm:
        for n in range(k2):
            if n+i < (k2):

                # if the values are empty, place an object in there

                if skolem[n] == False:
                    skolem[n] = i; skolem[n+i] = i
                    break

    # essentially, if it's not a valid skolem array, at least one value will be false,
    # thus we can reject the value

    return all(skolem)

def recursive_skolem_gen(perm, k, pos = 0, skolem = None):
    if not skolem:
        skolem = [False] * 2 * k
        
    if perm:
        if pos + perm[0] < 2*k:
            skolem[pos] = perm[0]
            skolem[pos+perm[0]] = perm[0]
            del perm[0]
            
            if not perm:
                return all(skolem)                    

            while skolem[pos]:
                pos += 1
                
            recursive_skolem_gen(perm,k, pos, skolem) 

    return all(skolem)

# this class just handles everything because i wanted to use the return feature

def everything(k, arg = 1):
    
    k = userinput(k)
    
    if not k:
         return 0

    # these arguments either filter the numbers given or don't.

    x = 0

    for perm in permutation_gen(k):
        perm = list(perm)
        if recursive_skolem_gen(perm, k):
            x += 1
            
    return x
file_path = "executiontime.txt"

#cProfile.run('everything(9)')

for arg in range(2):
    for i in range(1,10):
        time_start = time.time()
        x = everything(i, arg)
        time_elapsed = time.time()-time_start
        file = open(file_path, "a")
        file.write("\n" + str(arg) + ", " + str(i) + ", " + str(x) + ", " + str(time_elapsed))
        file.close()
