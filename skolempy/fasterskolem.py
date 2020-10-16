import time
import io
import sys
import itertools


# skolem sequences are lists 2*k units long (so a skolem sequence of order 4 looks is 8 elements
# long), with each number, n, from 1 to k, n units apart. One example of a 
# skolem sequence of order 4 would be: 1 1 4 2 3 2 4 3 - note that each number here is n units
# apart (seperated by n-1 units). This program finds all of these values by obversing the order
# the numes appear in these lists: in the previous sequence, the numbers are ordered like so: 
# 1, 4, 2, 3. We generate a series of all possible permutations of these numbers, and then, with
# the assumption that they're all valid, we generate a skolem sequence, and check to see if it itself
# is valid, and if it is, we return the sequence.

# http://www.cemc.uwaterloo.ca/contests/past_contests/2004/2004EuclidContest.pdf : look at problem 10
# on page 5 for further details.


# if k is 2mod4 or 3mod4, there are no skolem sequences, so we can just like, not compute these
def numpair_validation(k):
    return k % 4 not in (2, 3)


# this generates all the possible skolem orderings (eg, 1 then 2 then 3 then 4) - note that this generates
# them one at a time in order to save memory.

def permutations(numpair):
    yield numpair

    if len(numpair) == 1:
        return

    for n in numpair:
        new_list = numpair[:]
        pos = new_list.index(n)
        del (new_list[pos])
        new_list.insert(0, n)
        for resto in permutations(new_list[1:]):
            if new_list[:1] + resto != numpair:
                yield new_list[:1] + resto


# this generates a list of numbers from 1 to k for the permutation function
def numpair_gen(k):
    # generates array of permutatable values
    return list(range(1, k + 1))


# this filters the permutations: if the second term is 1 smaller than the first term,
# the sequence is invalid (eg: 4 3 _ _ 4 & 3 _ _ _ _ - as you can see, 4 and 3 would
# share the same space and thus the sequence can be discarded. this improves performance
# slightly (roughly 4%)
def numpair_check(perm):
    if len(perm) > 1:
        return perm[0] - 1 != perm[1]
    return True


def numpair_filter(perm):
    if len(perm) > 1:
        if perm[0] - 1 == perm[1]:
            return

    return perm


def skolem_gen(numpair, k):
    # generates an empty array of false values, so that we can populate it with the skolem pairings
    ls = 2 * k
    skolem = [0] * ls
    first_empty = 0

    # this goes over each number and places it into the first empty spot
    for i in numpair:
        for n in range(first_empty, ls - i):
            # if the first value is empty, place an object in there (this assumes that the generator
            # has a valid skolem sequence
            if not skolem[n]:
                if skolem[n + i]:
                    return
                first_empty = n + 1
                skolem[n] = i
                skolem[n + i] = i
                break
        else:
            return
    # if any value is false, this is not a valid skolem sequence, so we can discard it. otherwise,
    # we can return a valid sequence    
    return skolem


# if you want to manually chose which number you're ordering or just plug one in, this allows for you to
# do both (if no value for k is provided, it takes a value for k from the user)

def userinput(k=None):
    if not k:
        k = int(input("Skolem Ordering: "))

    if numpair_validation(k):
        return k
    return None


# this just does everything in a function because the return feature is very helpful when you need to
# break loops

def everything(k):
    if not k:
        return 0
    if k == 1:
        return 1 if skolem_gen([1], 1) else 0

    # if output is possible, we go ahead and have some fun. well,
    # the computer isn't having fun, but yes.

    x = 0

    # this goes over each permutation for k, filters it, and generates a skolem sequence. if a sequence
    # is returned, we iterate x. no array is used as this takes up a lot of memory for higher order skolem
    # sequences

    for perm in itertools.permutations(numpair_gen(k)):
        if perm[0] - 1 != perm[1]:
            if skolem_gen(perm, k):
                x += 1
    return x


if __name__ == '__main__':
    file_path = "executiontimef.txt"

    for i in range(1, 13):
        time_start = time.time()

        # you can safely remove i and the program will have you input a number manually from the command line

        x = everything(userinput(i))
        time_elapsed = time.time() - time_start

        # this generates data for mathplotlib (graph.py)
        # it writes which number we're on, the value attained for said time, and the length of time the program
        # has been running for.

        print(str(time_elapsed))
        file = open(file_path, "a")
        file.write("\n" + str(i) + ", " + str(x) + ", " + str(time_elapsed))
        file.close()
