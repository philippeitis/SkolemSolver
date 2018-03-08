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

# might be faster than the regular all function, might not be faster.
def p_all(arr):
    for n in arr:
        if not n:
            return False
    return True

# speed gains r here: maybe pregen the skolem false array?

def recursive_skolem_gen(perm, k, pos = 0, skolem = None):
    # i avoid using len() to prevent uneeded len calls which make the program slower
    
    # generates a skolem array: doesn't seem to work when it's fed from everything()
    # not sure about why it doesn't work.
    
    if not skolem:
        skolem = [False] * 2 * k

    if perm:
        # call the list element just once to save time
        perm_num = perm[0]
        
        if pos + perm_num < 2*k:
            
            # is there any way where I can test and run this at the same time to cut
            # down on repeated steps?
            
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
            # This updates the position until an empty value for pos is found
            while skolem[pos]:
                pos += 1
                
            recursive_skolem_gen(perm, k, pos, skolem) 

    if not perm:
        # can use p_all or regular all, whichever one is faster.
        # this just checks if it's a valid sequence
        return all(skolem)

# this class just handles everything because i wanted to use the return feature

def everything(k):
    
    k = userinput(k)
    
    if not k:
         return 0

    # these arguments either filter the numbers given or don't.

    x = 0

    if k == 1:
        return 1
    
    for perm in permutation_gen(k):
        perm = list(perm)
        if not perm[0]-1 == perm[1]:
            if recursive_skolem_gen(perm, k):
                x += 1
    return(x)

file_path = "executiontime.txt"

cProfile.run('everything(9)')

for i in range(1,14):
    time_start = time.time()
    x = everything(i)
    time_elapsed = time.time()-time_start
    print(x, end = " ")
    print(time_elapsed)
