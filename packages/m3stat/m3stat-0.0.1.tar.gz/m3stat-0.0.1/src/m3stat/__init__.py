
__all__ = ['mean','median','mode']

def mean(arr):
    return sum(arr)/len(arr)

def median(arr):
    mid = len(arr)//2
    if(len(arr)%2!=0):
        return  sorted(arr)[mid]
    else:
        return sum(sorted(arr)[mid-1:mid+1]) / 2


def mode(arr):
    arr = sorted(arr)
    max, maxn, n = arr[0], 1, 1
    for i,j in enumerate(arr[:-1]):
        if(j == arr[i+1]):
            n+=1
        else:
            if(maxn < n):
                max = j
                maxn = n
            n = 1
    return max
