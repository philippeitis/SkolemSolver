import itertools
import time
import io
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
    if k%4 == 2 or k%4 == 3 or k < 1:
        return
    return k

# no more performance can really be extracted from here, but this is where our next challenge would lie
def permutation_gen(k):    
    for perm in itertools.permutations(range(1,k+1)):
        if not perm[0]-1 == perm[1]:
            yield list(perm)

def skolem_gen(perm, k):
    pos = 0
    skolem = [False] * 2 * k

    for perm_num in perm:
        try:            
            if skolem[pos+perm_num]:
                return False
             
            skolem[pos] = perm_num
            skolem[pos+perm_num] = perm_num
            
            # This updates the position until an empty value for pos is found
            # any better way to do this?
            
            while pos < 2*k and skolem[pos]:
                pos += 1
                
        except:
            return False
    # this might have to be a call to all, but it seems to work fine now
    return True

def recursive_skolem_gen(perm, k, pos = 0, skolem = None):
    # i avoid using len() to prevent uneeded len calls which make the program slower
    
    # generates a skolem array: doesn't seem to work when it's fed from everything()
    # not sure about why it doesn't work.
    
    if not skolem:
        skolem = [False] * 2 * k

    if perm:
        # call the list element just once to save time
        try:
            perm_num = perm[0]            
            
            if skolem[pos+perm_num]:
                return False
             
            # additionally, is it possible to update more than one element in a list at a time?
            # is it worth trying?
            
            skolem[pos] = perm_num
            skolem[pos+perm_num] = perm_num
            
            # any better way of calling perm and then deleting it in the same step? pop takes longer
            del perm[0]
            
            # Why does this work? Not a question for Peter, just not quite sure either

            if not perm:
                return False
            
            while skolem[pos]:
                pos += 1
            
            recursive_skolem_gen(perm, k, pos, skolem) 
        except:
            return False
    if not perm:
        # can use p_all or regular all, whichever one is faster.
        # this just checks if it's a valid sequence
        return all(skolem)

# this class just handles everything because i wanted to use the return feature

def everything(k, arg = 0):
    
    k = userinput(k)
    
    if not k:
         return 0
    if k == 1:
        return 1
    # these arguments either filter the numbers given or don't.

    x = 0
    if arg == 0:
        for perm in itertools.permutations(range(1,k+1)):
            if not perm[0]-1 == perm[1]:
                if skolem_gen(perm, k):
                    x += 1
        return(x)


    if arg == 1:
        for perm in permutation_gen(k):
            if recursive_skolem_gen(perm, k):
                x += 1
        return(x)


cProfile.run('everything(9,0)')
cProfile.run('everything(9,1)')

for i in range(1,14):
    for arg in range(2):
        time_start = time.time()
        x = everything(i,arg)
        time_elapsed = time.time()-time_start
        file_name = "fastskolem.txt"
        file = open(file_name,"a+")
        if arg == 0:
            print("non recursive: ", end = " ")
            file.write("non recursive:  , ")
        elif arg == 1:
            print("recursive: ", end = "     ")
            file.write("recursive:      , ")
        file.write(str(x) + ", ")
        file.write(str(time_elapsed) + "\n")
        print(x, end = " ")
        print(time_elapsed)
