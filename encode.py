import numpy as np

def encode(arr1, arr2, fname):
    np.savetxt(fname, np.column_stack([
        arr1.view(float).reshape(-1, 2),
        arr2.view(float).reshape(-1, 2),
    ]))


if __name__ == '__main__':
    fname = 'send.dat'
    tmp = np.append(np.repeat(1, 5000), np.zeros(5000))
    arr1 = np.repeat(tmp, 4)
    arr2 = np.zeros(len(arr1))
    encode(arr1, arr2, fname)