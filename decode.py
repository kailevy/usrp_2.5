import numpy as np

def decode(arr1, arr2, fname):
    arr1, arr2 = np.loadtxt(fname, unpack=True).view(complex)

if __name__ == '__main__':
    pass