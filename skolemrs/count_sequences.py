def powerset(iterable):
    from itertools import chain, combinations

    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def to_skolem(sequence):
    skolem_seq = [0] * 2 * len(sequence)
    start = 0
    for val in sequence:
        for i in range(start, len(skolem_seq)):
            if skolem_seq[i] == 0:
                skolem_seq[i] = val
                skolem_seq[i + val] = val
                start = i + 1
                break
    return skolem_seq


def line_to_arr(line):
    line = line[1:-2]
    line = line.split(",")
    return [int(l) for l in line]


def read_file_to_sequences(skolem=4):
    with open(f"skolem{skolem}.txt", "r") as f:
        lines = f.readlines()
        lines = [line_to_arr(line) for line in lines]
    return lines


if __name__ == '__main__':
    import collections
    # ls = len(sequences)

    # x = {"".join([str(x) for x in s]): "".join([str(x) for x in to_skolem(s)]) for s in sequences}
    # inv_map = {}
    # for k, v in x.items():
    #     if v[::-1] in inv_map:
    #         v = v[::-1]
    #         inv_map[v].append(k)
    #     else:
    #         inv_map[v] = [k]
    # print(inv_map)
    skolem_numbers = [1, 0, 0, 6, 10, 0, 0, 504, 2656, 0, 0, 455936, 3040560, 0, 0, 1400156768, 12248982496, 0, 0,
                      11435578798976, 123564928167168, 0, 0, 204776117691241344, 2634563519776965376, 0, 0]

    import itertools
    # import math
    # for i in range(2, 14):
    #     perms = itertools.permutations(list(range(1, i+1)))
    #     count = 0
    #     for perm in perms:
    #         if perm[0] - 1 != perm[1]:
    #             count += 1
    #     print(math.factorial(i) - count, math.factorial(i))

    # for skolem in [4, 5, 8, 9, 12, 13]:
    #     sequences = read_file_to_sequences(skolem)
    #     print(skolem)
    #     first_symbols = collections.Counter([s[0] for s in sequences])
    #     last_symbols = collections.Counter([s[-1] for s in sequences])
    #     print(first_symbols.most_common(), last_symbols.most_common())
    #     first_last_symbols = collections.Counter([(s[0], s[-1]) for s in sequences])
    #     print(first_last_symbols.most_common())
    #     print(len(first_last_symbols))
        # for s in powerset(first_symbols.most_common()):
        #     if sum([x[1] for x in s]) == len(sequences) // 2:
        #         print("1st Half:", s)
        # for s in powerset(last_symbols.most_common()):
        #     if sum([x[1] for x in s]) == len(sequences) // 2:
        #         print("2nd Half:", s)

    sequences = read_file_to_sequences(9)
    d = {}
    nums = list(itertools.permutations(list(range(1, 10)), 2))
    num_dict = {num: True for num in nums}
    for a, b in nums:
        for s in sequences:
            skolem = to_skolem(s)
            skol_str = str(skolem)
            skol_rev = str(skolem[::-1])
            if skol_rev in d:
                rev = d[skol_rev]
                if (s.index(a) < s.index(b)) == (rev.index(a) < rev.index(b)):
                    num_dict[(a, b)] = False
            else:
                d[skol_str] = s
        # print(s, to_skolem(s), to_skolem(s)[::-1])
    for num in num_dict:
        if num_dict[num]:
            print(num)
    # print(to_skolem(sequences[0]))
    #
    # print(collections.Counter([s[0] for s in sequences]))
    # print(collections.Counter([s[-1] for s in sequences]))
    #
    # print(collections.Counter([s[0] for s in sequences2]))
    # print(collections.Counter([s[-1] for s in sequences2]))
    xlt = 0
    xgt = 0
    size = 4
    for i in itertools.permutations(list(range(1, size + 1))):
        x = 0
        for j in range(1, size):
            x |= (i.index(j) > i.index(j + 1)) << (size - j - 1)
        xlt += 1 if x < 4 else 0
        xgt += 1 if x >= 4 else 0
        print(f"{x:03b}")
    print(xlt == xgt)