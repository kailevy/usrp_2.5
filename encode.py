import numpy as np
# import matplotlib.pyplot as plt

def encode(sig, fname):
    tmp = np.zeros(2*len(sig), dtype='float32')
    tmp[::2] = np.real(sig)
    tmp[1::2] = np.imag(sig)
    tmp.tofile(fname)


if __name__ == '__main__':
    fname = 'send.dat'
    tmp = np.append(np.repeat(1, 1000), np.repeat(-1, 1000))
    arr1 = np.tile(tmp, 20)
    arr1 = np.insert(arr1, 0, np.zeros(5000))
    arr1 = np.append(arr1, np.zeros(5000))
    encode(arr1, fname)