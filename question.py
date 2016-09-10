#!/usr/bin/python3

def n_choose_k(n,k):
    import math
    return math.factorial(n)/(math.factorial(k)*math.factorial(n-k))

def sum_binom(n):
    sum = 0
    for k in range(n+1):
        sum += n_choose_k(n,k)
    return sum

def question(n):
    return sum_binom(n) == 2**n

def test():

    for i in range(100):
        print(i,sum_binom(i),2**i)
        if not question(i):
            print('Not true for i = {}'.format(i))
            print('\tsum_binom = {}, 2**n = {}'.format(sum_binom(i),2**i))


def main():
    test()

if __name__ == '__main__':
    main()
