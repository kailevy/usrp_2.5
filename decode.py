import numpy as np
import matplotlib.pyplot as plt 

def decode(fname):
    data = np.fromfile(fname)
    arr1 = data[::2]
    arr2 = data[1::2]
    return (arr1, arr2)

if __name__ == '__main__':
    arr1, arr2 = decode('/home/jwb/bits.txt')
    plt.plot(arr1)
    plt.plot(arr2)
